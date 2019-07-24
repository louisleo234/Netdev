#coding=utf-8
import paramiko
import time
#from ... inport...函数，目的是不需要再输入getpass.
from getpass import getpass

username=raw_input('Username:')
password=getpass('password:')

#用open()函数打开之前我们创建好的ip文档ip_list.txt, 通过for循环遍历readlines()方法返回列表中的每个元素
f = open("ip_list.txt",'r')
for line in f.readlines():
    ip = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip,username=username,password=password,allow_agent=False,look_for_keys=False)
    print "Successfully connect to ", ip

#登录每台机器，将回显内容打印出来
    remote_connection = ssh_client.invoke_shell()
    remote_connection.send("ping 10.129.16.1\n")
    time.sleep(5)
    remote_connection.send("sh mac add | in a44c.c821.998f\n")
    time.sleep(2)
    remote_connection.send("quit\n")
    time.sleep(3)
    output = remote_connection.recv(65535)
    print output

#脚本结束前close()关掉文档并关闭SSH连接
f.close()
ssh_client.close