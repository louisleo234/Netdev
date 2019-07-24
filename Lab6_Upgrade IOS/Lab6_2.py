#coding=utf-8
#导入模块
import paramiko
import time
import getpass
import sys
import re
import socket

username=raw_input("Username: ")
password=getpass.getpass("Password: ")
iplist=open('ip_list.txt', 'r+')

#创建4个空列表统计多少交换机已经成功升级，哪些没有升级、哪些因为TACACS或不可达无法登录,配合for循环ssh登录交换机
switch_upgraded=[]
switch_not_upgraded=[]
switch_with_tacacs_issue=[]
switch_not_reachable=[]

for line in iplist.readlines()
    try:
        ip_address=line.strip()
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address,username=username,password=password)
        print "Successfully connect to ", ip_address

#因为涉及show flash: | in c2960的输出，调整paramiko回显宽度
        command=ssh_client.invoke_shell(width=300)

#重启交换机后show ver | b SW ver查看当前IOS版本, 再用正则式匹配12.2(55)SE12, 15.2(2)E8, 15.0(2)SE11三个IOS
#匹配到就将IP放置到switch_upgraded列表, 匹配不到就将交换机IP放到switch_not_reachable列表
#再用for循环将switch_upgraded和switch_not_reachable元素打印出来
        command.send("show ver | in b SW Version\n")
        time.sleep(0.5)
        output=command.recv(65535)
        print out
        ios_version=re.search(r'\d{2}.\d\(\d{1,2}\)\w{2,4}',output)
        if ios_version.group()=='12.2(55)SE12':
            switch_upgraded.append(ip_address)
        elif
            ios_version.group()=='15.2(2)E8'
            switch_upgraded.append(ip_address)
        elif ios_version.group()=='15.0(2)SE11':
            switch_upgraded.append(ip_address)
        else:
            switch_not_upgraded.append(ip_address)

except  paramiko.ssh_exception.AuthenticationException:
print   "TACACS is not working for " + ip_address + "."
        switch_with_tacacs_issue.append(ip_address)

except socket.error:
        print ip_address + " is not reachable."
        switch_not_reachable.append(ip_address)

iplist.close()
ssh_client.close

print '\nTACACS is not working for below switches: '
for i in switch_with_tacacs_issue:
    print i

print '\nBelow switches are not reachable: '
for i in switch_not_reachable:
    print i

print '\nBelow switches IOS version are up-to-date: '
for i in switch_upgraded:
    print i

print '\nBelow switches IOS version are not updated yet: '
for i in switch_not_upgraded:
    print i
