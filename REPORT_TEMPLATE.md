# Project Report: Bandwidth Measurement and Analysis

## 1. Problem statement

The goal of this project is to measure and compare bandwidth across different SDN network configurations using Mininet and a Ryu OpenFlow controller. The project focuses on throughput measurement with `iperf`, latency observation with `ping`, and OpenFlow rule behavior through switch flow tables.

## 2. Tools used

- Mininet
- Ryu controller
- Open vSwitch
- `iperf`
- `ping`

## 3. Topologies tested

### Star topology

- Single switch
- Four hosts
- 100 Mbps host links

### Linear topology

- Two switches
- Four hosts
- One 20 Mbps bottleneck link between switches

### Tree topology

- Three switches
- Four hosts
- 60 Mbps core links and 40 Mbps edge links

## 4. Testing method

1. Start the Ryu controller.
2. Launch each topology from the automation script.
3. Use `ping` to measure RTT between the first and last host.
4. Use `iperf` to measure TCP throughput.
5. Dump switch flow tables using `ovs-ofctl`.
6. Store all results in CSV and log files.

## 5. Result table

Fill this from `results/bandwidth_results.csv`.

| Topology | Avg ping (ms) | Throughput (Mbits/sec) | Observation |
|---|---:|---:|---|
| Star |  |  |  |
| Linear |  |  |  |
| Tree |  |  |  |

## 6. Analysis

- The topology with the highest throughput should be the star topology because it has no inter-switch bottleneck.
- The linear topology should show the lowest throughput because the 20 Mbps switch-to-switch link constrains the path.
- The tree topology should perform better than linear but below star because of additional switching and lower core/edge capacities.
- Flow-table logs show how the controller dynamically installs rules after `packet_in` events.

## 7. Conclusion

This project demonstrates SDN controller-switch interaction, explicit OpenFlow rule installation, and performance measurement across multiple topologies. The experimental results show how link bandwidth, hop count, and topology shape affect network throughput and latency.
