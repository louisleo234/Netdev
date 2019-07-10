#coding=utf-8

import paramiko
import time
import re

#datatime内建模块是显示时间用的.
from datetime import datetime
import socket
import getpass

#raw_input()和getpass.getpass()提示用户输入用户名密码. datetime.now()方法记录当前时间,年、月、日赋值给date,
# 时、分、秒复制给time_now
username = raw_input('Enter your SSH username: ')
password = getpass.getpass('Enter your SSH password: ')
now = datetime.now()
date = "%s-%s-%s" % (now.month, now.day, now.year)
time_now = "%s:%s:%s" % (now.hour, now.minute, now.second)


#创建switch_with_tacacs_issue和switch_not_reachable来统计哪些是TACACS失败或交换机不可达信息
#total_number_of_up_port设置初始值为0,统计交换机为up的端口总数
switch_with_tacacs_issue = []
switch_not_reachable = []
total_number_of_up_port = 0


#open()函数打开脚本1创建的reachable_ip.txt,用readlines()将内容以列表返回. 配合len()函数得到可达交换机数量
#本例子每交换机为16口，所以交换机数量*16我们可以得到端口总数(不论端口是否up)
iplist = open('reachable_ip.txt')
number_of_switch = len(iplist.readlines())
total_number_of_ports = number_of_switch * 16


#上面open()函数打开过reachable_ip.txt，所以我们需要seek(0)回到文件起始位.
#注意用来应对交换机登录失败的问题,异常处理语句try要写在for循环下面. 剩下就是使用paramiko配合for循环并进入命令行的代码.
iplist.seek(0)
for line in iplist.readlines():
    try:
        ip = line.strip()
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=username, password=password)
        print "\nYou have successfully connect to", ip
        command = ssh_client.invoke_shell()

#sh ip int brief回显内容比较长,先用term len 0完整显示所有回显内容, sleep延迟1秒再通过recv(65535)将回显保存到output
        command.send('term len 0\n')
        command.send('show ip int b | in up\n')
        time.sleep(1)
        output = command.recv(65535)
        #print output

#我们只想统计Eth端口是UP, 用正则式findall()方法精确匹配Et,将findall返回的列表赋值给变量number_of_port
#通过len(serach_up_port)得到up端口的数量,再将数量赋值给变量number_of_port,再打印出多少UP的端口
#因为定义了变量total_number_of_up_port,并赋予了整数0.通过total_number_of_up_port += number_of_up_port将UP的端口累加
        search_up_port = re.findall(r'Ethernet', output)
        number_of_up_port = len(search_up_port)
        print ip + " has " + str(number_of_up_port) + " ports up."
        total_number_of_up_port += number_of_up_port

    except paramiko.ssh_exception.AuthenticationException:
        print "TACACS is not working for " + ip + "."
        switch_with_tacacs_issue.append(ip)

    except socket.error:
        print ip + " is not reachable."
        self.switch_not_reachable.append(ip)

    iplist.close()

#除了打印统计信息,再创建另外一个文件,通过f=open(date+txt,a)将运行脚本日期用作脚本名，将统计信息写进去,可以清晰看到哪天运行的脚本
#用日期做脚本名只要运行时间不同脚本会自动创建新文件.
    print "\n"
    print "There are totally " + str(total_number_of_ports) + " ports available in the network."
    print str(total_number_of_up_port) + " ports are currently up."
    print "Port up rate is %.2f%%" % (total_number_of_up_port / float(total_number_of_ports) * 100)
    print '\nTACACS is not working for below switches:'
    for i in switch_with_tacacs_issue:
        print i

    print '\nBelow switches are not reachable: '

    for i in switch_not_reachable:
        print i
    f = open(date + ".txt", "a+")
    f.write('As of' + date + " " + time_now)
    f.write("\n\nThere are totally " + str(total_number_of_ports) + " ports available in the network.")
    f.write("\n" + str(total_number_of_up_port) + " ports are currently up.")
    f.write("\nPort up rate is %.2f%%" % (total_number_of_up_port /float(total_number_of_ports) * 100))
    f.write("\n**********************************************************************************\n\n")

    f.close()