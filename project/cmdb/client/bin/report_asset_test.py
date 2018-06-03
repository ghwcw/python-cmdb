# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-03-28
    Project : cmdb
   FileName : report_asset_test.py
Description : 
-------------------------------------------------------------
"""
import datetime
import json
import os
import sys
from urllib import request
from urllib.parse import urlencode

from cmdb import settings

BASE_DIR = os.path.dirname(os.getcwd())
# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)


def report_data_test(data):
    """
    创建测试用例
    """
    # 将数据打包到一个字典内，并转换为json格式
    data = {'asset_data': json.dumps(data)}

    # 根据settings中的配置，构造url
    url = "http://%s:%s%s" % (settings.PARAMS['server'], settings.PARAMS['port'], settings.PARAMS['url'])
    print('正在将测试数据发送至： [%s]  ......' % url)
    try:
        data_encode = urlencode(data, encoding='utf-8')
        requ = request.Request(url=url, data=data_encode.encode(), method='POST')
        with request.urlopen(requ, timeout=settings.PARAMS['request_timeout']) as resp:
            print('测试发送成功！')
            message = '成功:%s' % resp.read().decode()
            print('测试返回结果：%s' % message)
    except Exception as e:
        message = '测试失败:%s' % e
        print('测试发送失败：%s' % message)

    # 记录日志
    with open(settings.LOGPATH, mode='ab') as fh:
        string = '测试发送时间：%s \t 测试服务器地址：%s \t 测试返回结果：%s \n' % (
            datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), url, message)
        fh.write(string.encode())
        print('测试日志记录成功!')


# 构建测试数据并测试
if __name__ == '__main__':
    windows_data = {
        "os_type": "Windows",
        "os_release": "server2008 64bit  6.1.7601 ",
        "os_distribution": "Microsoft",
        "asset_type": "storagedevice",
        "cpu_count": 8,
        "cpu_model": "Intel(R) Core(TM) i7-2300 CPU @ 2.80GHz",
        "cpu_core_count": 32,
        "ram": [
            {
                "slot": "A1",
                "capacity": 16,
                "model": "Physical Memory",
                "manufacturer": "kingstone ",
                "sn": "456"
            },

        ],
        "manufacturer": "Intel",
        "model": "P67X-UD3R-B3",
        "wake_up_type": 6,
        "sn": "00426-OEM-8992662-666666-test",
        "physical_disk_driver": [
            {
                "iface_type": "unknown",
                "slot": 0,
                "sn": "3830414130423230343234362020202020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 1024
            },
            {
                "iface_type": "SATA",
                "slot": 1,
                "sn": "383041413042323023234362020102020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 2048
            },

        ],
        "nic": [
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "[00000011] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "name": 11,
                "ip_address": "192.168.1.113",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "0A:01:27:00:00:00",
                "model": "[00000013] VirtualBox Host-Only Ethernet Adapter",
                "name": 13,
                "ip_address": "192.168.56.13",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "[00000017] Microsoft Virtual WiFi Miniport Adapter",
                "name": 17,
                "ip_address": "",
                "net_mask": ""
            },
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "Intel Adapter",
                "name": 17,
                "ip_address": "192.1.1.3",
                "net_mask": ""
            },


        ]
    }


    linux_data = {
        "asset_type": "storagedevice",
        "manufacturer": "innotek GmbH",
        "sn": "00003-test",
        "model": "VirtualBox",
        "uuid": "E8DE611C-4279-495C-9B58-502B6FCED099",
        "wake_up_type": "Power Switch",
        "os_distribution": "RedHat",
        "os_release": "RedHat 6.04.3 LTS",
        "os_type": "Linux",
        "cpu_count": "4",
        "cpu_core_count": "16",
        "cpu_model": "Intel(R) Core(TM) i5-2300 CPU @ 2.80GHz",
        "ram": [
            {
                "slot": "A1",
                "capacity": 32,
            }
        ],
        "ram_size": 3.858997344970703,
        "nic": [],
        "physical_disk_driver": [
            {
                "model": "VBOX HARDDISK",
                "size": "50",
                "sn": "VBeee1ba73-09085309"
            }
        ]
    }

    report_data_test(windows_data)
    report_data_test(linux_data)

