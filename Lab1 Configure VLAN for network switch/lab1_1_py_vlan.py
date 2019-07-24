#coding=utf-8
#导入模块
import paramiko
import time
#getpass模块是python内建模块，无需pip安装即可使用，用于交互式提示输入密码
import getpass

#提示输入用户名，明文
username = raw_input('Username:')
#getpass输入密码是不可见的，安全性高
password = getpass.getpass('Password:')


#因为交换机IP是连续的，用for循环遍历列表[201,202,203,204,205], i是整数，需要str(i)转换成字符串
for i in range(201,206):
    ip = "192.168.213." + str(i)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password)
    print "Successfully connect to ", ip
    command = ssh_client.invoke_shell()
    command.send("enable\n")
    command.send("configure terminal\n")

#为了创建vlan10-20，配合一个简单的内嵌for循环,每创建一个vlan之间需要1秒间隔
    for n in range(10,21):
        print "Creating VLAN" + str(n)
        command.send("vlan " + str(n) + "\n")
        command.send("name Python_VLAN " + str(n) + "\n")
        time.sleep(1)


#最后保存配置, 间隔2秒打印回显内容并关闭SSH
    command.send("end\n")
    command.send("wr mem\n")
    time.sleep(2)
    output = command.recv(65535)
    print output

ssh_client.close