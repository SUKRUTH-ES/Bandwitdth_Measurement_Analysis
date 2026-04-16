#!/usr/bin/env python3
import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController

from topology.bandwidth_topologies import TOPOLOGIES


def parse_ping_avg(ping_output):
    match = re.search(r"rtt min/avg/max/mdev = [^/]+/([^/]+)/", ping_output)
    return float(match.group(1)) if match else None


def parse_iperf_throughput(iperf_output):
    lines = [line.strip() for line in iperf_output.splitlines() if "Mbits/sec" in line]
    if not lines:
        return None
    summary = lines[-1]
    match = re.search(r"([0-9.]+)\s+Mbits/sec", summary)
    return float(match.group(1)) if match else None


def dump_flows(net, topology_name, timestamp, results_dir):
    flow_dir = results_dir / "flow_tables"
    flow_dir.mkdir(parents=True, exist_ok=True)
    for switch in net.switches:
        output = switch.cmd(f"ovs-ofctl -O OpenFlow13 dump-flows {switch.name}")
        file_path = flow_dir / f"{timestamp}_{topology_name}_{switch.name}.log"
        file_path.write_text(output)


def run_single_test(topology_name, duration, controller_ip, controller_port, results_dir):
    topo = TOPOLOGIES[topology_name]()
    controller = lambda name: RemoteController(name, ip=controller_ip, port=controller_port)
    net = Mininet(
        topo=topo,
        controller=controller,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True,
        build=False,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    flow_warmup_seconds = 2
    result = {
        "timestamp": timestamp,
        "topology": topology_name,
        "source_host": "",
        "destination_host": "",
        "ping_avg_ms": "",
        "throughput_mbps": "",
        "notes": "",
    }

    try:
        net.build()
        net.start()
        time.sleep(flow_warmup_seconds)

        hosts = sorted(net.hosts, key=lambda host: host.name)
        src = hosts[0]
        dst = hosts[-1]
        result["source_host"] = src.name
        result["destination_host"] = dst.name

        ping_output = src.cmd(f"ping -c 4 {dst.IP()}")
        result["ping_avg_ms"] = parse_ping_avg(ping_output) or ""

        dst.cmd("pkill -f 'iperf -s' || true")
        dst.cmd("iperf -s -D")
        time.sleep(1)
        iperf_output = src.cmd(f"iperf -c {dst.IP()} -t {duration} -f m")
        dst.cmd("pkill -f 'iperf -s' || true")
        result["throughput_mbps"] = parse_iperf_throughput(iperf_output) or ""

        logs_dir = results_dir / "raw_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        (logs_dir / f"{timestamp}_{topology_name}_ping.log").write_text(ping_output)
        (logs_dir / f"{timestamp}_{topology_name}_iperf.log").write_text(iperf_output)

        dump_flows(net, topology_name, timestamp, results_dir)

        if result["throughput_mbps"] == "":
            result["notes"] = "iperf output could not be parsed"

    finally:
        net.stop()

    return result


def write_results(results, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    file_exists = output_file.exists()
    with output_file.open("a", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "timestamp",
                "topology",
                "source_host",
                "destination_host",
                "ping_avg_ms",
                "throughput_mbps",
                "notes",
            ],
        )
        if not file_exists:
            writer.writeheader()
        for row in results:
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description="Run bandwidth tests across Mininet topologies.")
    parser.add_argument(
        "--topologies",
        nargs="+",
        default=["star", "linear", "tree"],
        choices=sorted(TOPOLOGIES.keys()),
        help="Topologies to test.",
    )
    parser.add_argument("--duration", type=int, default=10, help="iperf duration in seconds.")
    parser.add_argument("--controller-ip", default="127.0.0.1", help="Ryu controller IP.")
    parser.add_argument("--controller-port", type=int, default=6653, help="Ryu controller port.")
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "results" / "bandwidth_results.csv"),
        help="CSV file for test results.",
    )
    args = parser.parse_args()

    setLogLevel("warning")
    output_file = Path(args.output)
    results = []

    for topology_name in args.topologies:
        print(f"Running topology: {topology_name}")
        result = run_single_test(
            topology_name=topology_name,
            duration=args.duration,
            controller_ip=args.controller_ip,
            controller_port=args.controller_port,
            results_dir=output_file.parent,
        )
        results.append(result)
        print(
            f"Completed {topology_name}: avg_ping={result['ping_avg_ms']} ms, "
            f"throughput={result['throughput_mbps']} Mbits/sec"
        )

    write_results(results, output_file)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    if os.geteuid() != 0:
        raise SystemExit("Run this script with sudo because Mininet requires root.")
    main()
