from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI


class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
                Topo.__init__(self, **opts)
					
                # Add your logic here ...
						
				switch1 = self.addSwitch('C1')
				
				for i in range(1,3):
					switch2 = self.addSwitch('A%s' %(i))
					self.addLink(switch1,switch2,**linkopts1)
					for j in range(i*2-1,i*2+1):
						switch3 = self.addSwitch('E%s' %j)
						self.addLink(switch2,switch3,**linkopts2)
						for k in range(j*2-1,j*2+1):
							host = self.addHost('h%s' %k) 
							self.addLink(host,switch3,**linkopts3)
							
				
#Function used to "test/verify" your topo
def perfTest():
   "Create network and run simple performance test"
   #"--- core to aggregation switches"
   linkopts1 = {'bw':50, 'delay':'5ms'}
   #"--- aggregation to edge switches"
   linkopts2 = {'bw':30, 'delay':'10ms'}
   #"--- edge switches to hosts"
   linkopts3 = {'bw':10, 'delay':'15ms'}
   topo = CustomTopo(linkopts1 , linkopts2 , linkopts3 , fanout= 2)
   net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
   net.start()
   CLI(net)
   net.stop()

topos = { 'custom': ( lambda: CustomTopo() ) }

#Main function used to conduct the test
if __name__ == "__main__":
 setLogLevel('info')
 perfTest()

