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
iplist=open('ip_list.txt','r+')

#创建4个空列表统计多少交换机已经成功升级，哪些没有升级、哪些因为TACACS或不可达无法登录,配合for循环ssh登录交换机
switch_upgraded=[]
switch_not_upgraded=[]
switch_with_tacacs_issue=[]
switch_not_reachable=[]

for line in iplist.readlines():
    try:
        ip_address=line.strip()
        ssh_client=paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip_address,username=username,password=password)
        print "Successfully connect to ",ip_address

#因为涉及show flash: | in c2960的输出，调整paramiko回显宽度
        command=ssh_client.invoke_shell(width=300)

#从show inventory回显用正则表达式来匹配他们
#有3种交换机型号,我们也用正则表达式匹配
#有3种引导路径,也用正则表达式匹配
        command.send("show inventory | in PID:WS\n")
        time.sleep(0.5)
        command.send("show flash: | in c2960\n")
        time.sleep(0.5)
        command.send("show boot | in BOOT path\n")
        time.sleep(0.5)
        output=command.recv(65535)
        command.send("wr mem\n")
        switch_model=re.search(r'WS-C2960\W?-\W{4,5}-L',output)
        ios_version=re.search(r'c2960\w?-\w{8,10}\d-mz.\d{3}-\d{1,2}.\w{2,4}(.bin)?',output)
        boot_system=re.search(r'flash:.+mz.\d{3}-\d{1,2}\.\w{2,4}\.bin',output)

#if语句配合and和or逻辑运算判断,如果交换机型号是2960-24pc-l且IOS为2960-lanbasek9-mz.122-55.SE12.bin
#并且引导路径为flash:c2960-lanbasek9-mz.122-55.SE12.bin,那么交换机IP地址加入switch_upgraded列表
        if switch_model.group()=="WS-C2960-24PC-L" and ios_version.group()=="c2960-lanbasek9-mz.122-55.SE12.bin" and boot_system.group()=='flash:c2960-lanbasek9-mz.122-55.SE12.bin' or boot_system.group()=='flash:/c2960-lanbasek9-mz.122-55.SE12.bin':
            switch_upgraded.append(ip_address)
        elif switch_model.group()=="WS-2960S-F24PS-L" and ios_version.group()=="c2960-universalk9-mz.150-2.SE11.bin" and boot_system.group()=='flash:c2960s-universalk9-mz.150-2.SE11.bin' or boot_system.group()=='flash:/c2960s-universalk9-mz.150-2.SE11.bin':

        elif switch_model.group()=="WS-C2960X-24PS-L" and ios_version.group()=="c2960x-universalk9-mz.152-2.E8.bin" and boot_system.group()=='flash:c2960x-universalk9-mz.152-2.E8.bin' or boot_system.group()=='flash:/c2960x-universalk9-mz.152-2.E8.bin':
            switch_upgraded.append(ip_address)
#如果没有匹配的则将ip加入到switch_not_upgraded
        else:
            switch_not_upgraded.append(ip_address)

#最后将switch_upgraded和switch_not_upgraded两个列表打印出来,方便查看哪些已经升级，哪些没有升级
        except paramiko.ssh_exception.AuthenticationException:
            print "TACACS is not working for " + ip_address + "."
            switch_with_tacacs_issue.append(ip_address)
    except socket.error:
            print ip_address + " is not reachable."
            switch_not_reachable.append(ip_address)

iplist.close()
ssh_client.close