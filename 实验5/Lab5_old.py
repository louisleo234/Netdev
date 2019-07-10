#coding=utf-8

#导入pyping/os模块，记得主机安装pip install pyping

import pyping
import os

'''不希望每次运行脚本1后,不希望保留上一次脚本生成的reachable_ip文件,可以用os模块下os.path.exists()方法判断文件是否存在,
存在的话用os.remove()方法删除文件，这样可以保证每次运行脚本1时 reachable_ip这个文件只包含本次运行脚本后的所有可达交换机
'''
if os.path.exists('reachable_ip.txt'):
    os.remove('reachable_ip.txt')


#开头两个地址段不变,第三位,第四位我们可以使用range创建两个整数列表来囊括ip第三,四位，为后面两个for循环做准备
third_octet = 213
last_octet = range(1,255)


#通过两个循环,依次从192.168.213.1遍历到254,然后配合pyping.ping()来依次ping这些IP
for ip3 in third_octet:
    for ip4 in last_octet:
        ip = '192.168.' + str(ip3) + '.' + str(ip4)
        ping_result = pyping.ping(ip)

#如果目标可达,pyping ret_code属性会返回整数0, 不可达则返回非0的整数,这里将所有可达IP已追加模式写入reachable_ip文件
#另外pyping模块运行中不显示任何回显内容,我们通过Print分别打印机出目标IP是否可达的信息.

        f=open('reachable_ip.txt','a')
        if ping_result.ret_code == 0:
            print ip + ' is reachable. '
            f.write(ip + "\n")

        else:
            print ip + ' is not reachable. '

#关闭reachable_ip.txt文件
f.close()