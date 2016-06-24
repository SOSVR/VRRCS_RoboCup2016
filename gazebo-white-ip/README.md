### Adding a White-Ip list for Gazebo Server

In a gazebo plugin like the `code.py` here, we use sockets and TCP/IP connections to share data between systems.
After the socket is set up, the subscriber should ask for data from server.
There we get his IP and check if his IP is valid.
For this reason, for now we use an array of IPs (`whiteIpList` here) and search for the IP in the list.

With the code `address = socket.accept()` we get the IP of the subscriber and check if it is registered 
in the `whiteIpList` array.


###Complete Code
You can view the complete plugin code [https://github.com/taherahmadi/VRRCS_RobotCup2016/gazebo_white_ip/code.py](here).

###Using IPTables
Another option is to use IPTables of the OS.

If you want to allow arbitrary ranges rather than entire subnets, you can use the 'iprange' iptables module:

iptables -P INPUT DROP

iptables -A INPUT -m iprange —src-range 192.168.1.30-50 -j ACCEPT

for example, will allow traffic coming from all machines with addressess between 192.168.1.30 and 192.168.1.50.

If you want to allow incoming and outgoing traffic to the same range of IP's, I'd suggest that you create a specific chain allowing that IPs and targeting all the input and output target to it:

—define the default policies to drop everithing:

iptables -P INPUT DROP

iptables -P OUTPUT DROP

—create the new chain:

iptables -N allowed_ips

—if the source is part of the allowed range, accept

iptables -A allowed_ips -m iprange —src-range 192.168.1.30-50 -j ACCEPT

—if not, return to the caller chain to continue processing

iptables -A allowed_ips -j RETURN

—make all traffic entering and leaving the machine go through our new chain

iptables -A INPUT -j allowed_ips

iptables -A OUTPUT -j allowed_ips

and that's it! of course you may need aditional rules, such as one allowing all traffic from/to the lo interface, etc.