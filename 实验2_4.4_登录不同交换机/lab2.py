#coding=utf-8
import paramiko
import time
#from ... inport...函数，目的是不需要再输入getpass.
from getpass import getpass

username = raw_input('Username: ')
password = getpass('password: ')

#用open()函数打开之前我们创建号的ip文档ip_list.txt, 通过for循环遍历readlines()方法返回列表中的每个元素
f = open("ip_list.txt",'r')
for line in f.readlines():
    ip = line.strip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password)
    print "Successfully connect to ", ip

#登录每台打印机，将回显内容打印出来
    remote_connection = ssh_client.invoke_shell()
    remote_connection.send("enable\n")
    remote_connection.send("conf t\n")
    remote_connection.send("router eigrp 1\n")
    remote_connection.send("end\n")
    remote_connection.send("wr mem\n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    print output

#脚本结束前close()关掉文档并关闭SSH连接
f.close()
ssh_client.close
