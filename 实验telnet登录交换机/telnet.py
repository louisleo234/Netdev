import telnetlib

host = "192.168.213.201"
user = "python"
password = "123"

tn = telnetlib.Telnet(host)
tn.read_until("Username:")
tn.write(user +"\n")
tn.read_until("Password:")
tn.write(password + "\n")

tn.write("ena\n")
tn.write("123\n")
tn.write("conf t\n")
tn.write("int loopback 1\n")
tn.write("ip address 1.1.1.1 255.255.255.255\n")
tn.write("end\n")
tn.write("exit\n")

print tn.read_all()
