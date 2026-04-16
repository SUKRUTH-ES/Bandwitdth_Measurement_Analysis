from mininet.topo import Topo


class StarTopology(Topo):
    def build(self):
        switch = self.addSwitch("s1")
        for index in range(1, 5):
            host = self.addHost(f"h{index}")
            self.addLink(host, switch, bw=100, delay="2ms", loss=0)


class LinearTopology(Topo):
    def build(self):
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")

        self.addLink(h1, s1, bw=80, delay="2ms", loss=0)
        self.addLink(h2, s1, bw=80, delay="2ms", loss=0)
        self.addLink(s1, s2, bw=20, delay="8ms", loss=0)
        self.addLink(h3, s2, bw=80, delay="2ms", loss=0)
        self.addLink(h4, s2, bw=80, delay="2ms", loss=0)


class TreeTopology(Topo):
    def build(self):
        core = self.addSwitch("s1")
        edge_left = self.addSwitch("s2")
        edge_right = self.addSwitch("s3")

        self.addLink(core, edge_left, bw=60, delay="4ms", loss=0)
        self.addLink(core, edge_right, bw=60, delay="4ms", loss=0)

        for host_name, edge_switch in [("h1", edge_left), ("h2", edge_left), ("h3", edge_right), ("h4", edge_right)]:
            host = self.addHost(host_name)
            self.addLink(host, edge_switch, bw=40, delay="2ms", loss=0)


TOPOLOGIES = {
    "star": StarTopology,
    "linear": LinearTopology,
    "tree": TreeTopology,
}
