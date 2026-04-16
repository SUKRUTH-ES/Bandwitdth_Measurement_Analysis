# Bandwidth Measurement and Analysis Using SDN Mininet

## Project objective

This project measures and compares bandwidth across multiple SDN network configurations using Mininet and a Ryu OpenFlow controller. It satisfies the guideline requirements by providing:

- Mininet-based topology creation
- A Ryu controller with explicit flow-rule installation through `packet_in` handling
- Multiple topology comparisons
- `ping` latency measurement
- `iperf` throughput measurement
- Flow-table logging for proof of execution
- Result analysis from collected CSV/log files

## Topologies compared

1. `star`
   One switch with four hosts. All hosts connect directly to one switch with 100 Mbps links.
2. `linear`
   Two switches connected by a 20 Mbps bottleneck link. This is expected to show lower throughput.
3. `tree`
   A three-switch hierarchy with 60 Mbps core links and 40 Mbps host-edge links.

## Project structure

```text
bandwidth_measurement_analysis/
├── controller/
│   └── bandwidth_controller.py
├── results/
├── scripts/
│   ├── run_bandwidth_tests.py
│   └── summarize_results.py
├── topology/
│   └── bandwidth_topologies.py
└── README.md
```

## What the controller does

- Uses OpenFlow 1.3
- Installs a table-miss flow entry
- Learns source MAC addresses from `packet_in`
- Installs match-action flow rules for known destinations
- Logs flow installation events

This directly addresses the rubric points around controller-switch interaction and flow-rule design.

## What the experiment collects

For each topology:

- `ping` average latency between the first and last host
- `iperf` throughput in Mbits/sec
- OpenFlow flow tables from each switch
- Raw command logs for proof of execution

Output files are written to:

- `results/bandwidth_results.csv`
- `results/raw_logs/`
- `results/flow_tables/`

## Installation commands

If Mininet is already installed, only install the missing Python dependency support.

```bash
curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py --break-system-packages
~/.local/bin/pip3 install --user --break-system-packages eventlet msgpack netaddr oslo.config ovs routes six tinyrpc webob
```

This project already includes a vendored Ryu source tree under `vendor/ryu-src`, so you do not need a global `ryu-manager` install.

## How to run the project

Open terminal 1:

```bash
cd ~/Downloads/bandwidth_measurement_analysis
python3 scripts/run_ryu_manager.py controller/bandwidth_controller.py
```

Open terminal 2:

```bash
cd ~/Downloads/bandwidth_measurement_analysis
sudo python3 scripts/run_bandwidth_tests.py --duration 10
```

Generate a quick summary after the tests finish:

```bash
cd ~/Downloads/bandwidth_measurement_analysis
python3 scripts/summarize_results.py
```

## Optional manual Mininet cleanup

If a previous Mininet run was not cleaned up:

```bash
sudo mn -c
```

## Expected analysis

You should observe:

- `star` topology giving the highest throughput because there is no inter-switch bottleneck
- `linear` topology giving the lowest throughput because the 20 Mbps link limits end-to-end performance
- `tree` topology performing between `star` and `linear`
- Higher latency in topologies with more switch hops and larger configured delay


