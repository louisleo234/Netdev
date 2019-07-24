#coding=utf-8
import paramiko
import time
import getpass
import sys
#为了处理网络不可达模块引起的socket.error,需要导入socket内建模块
import socket

username=raw_input('Username:')
password=getpass.getpass('password:')

#创建两个变量ip_file和cmd_file,分别对应sys.argv[1]和sys.argv[2]
#argv是argument variable简写,该变量返回的是列表
#argv找不到变量时可以尝试python lab4_test.py ip_list.txt cmd.txt去定义元素列表的序列
ip_file=sys.argv[1]
cmd_file=sys.argv[2]


#创建两个空列表，作用用于统计for循环里的哪些设备因为认证无法登录和哪些设备身份不可达无法登录
switch_with_authentication_issue=[]
switch_not_reachable=[]


'''
在for循环使用try except异常处理语句. ssh登录如果用户名/密码不正确，python会报paramiki.ssh_exception.AuthenticationException,
所以我们用exceptparamiko.ssh_exception.AuthenticationException来应对异常.
'''
iplist=open(ip_file, 'r')
for line in iplist.readlines():
    try:
        ip=line.strip()
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=username, password=password)
        print "You have successfully connect to ", ip
        command = ssh_client.invoke_shell()
        cmdlist = open(cmd_file, 'r')
        cmdlist.seek(0)
        for line in cmdlist.readlines():
            command.send(line + "\n")
        time.sleep(2)
        cmdlist.close()
        output = command.recv(65535)
        print output
    except paramiko.ssh_exception.AuthenticationException:
        print "User authentication failed for " + ip + "."
        switch_with_authentication_issue.append(ip)
    except socket.error:
#failed to respond打印 is not reachable,然后将出现该错误的交换机管理IP用append()方法放入switch_not_reachable列表中
        print ip + " is not reachable."
        switch_with_authentication_issue.append(ip)

iplist.close()
ssh_client.close

#for循环打印switch_with_authentication_issue和switch_not_reachable两个列表的元素，这样就能知道哪些交换机验证失败，哪些不可达
print '\nUser authentication failed for below switches:'
for i in switch_with_authentication_issue:
    print i

print '\nBelow switches are not reachable: '
for i in switch_not_reachable:
    print i
