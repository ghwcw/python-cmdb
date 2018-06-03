# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------------------
    Creator : 汪春旺
       Date : 2018-03-26
    Project : cmdb
   FileName : winsysinfo.py
Description : 本模块基于windows操作系统，依赖wmi和win32com库
-------------------------------------------------------------
"""
import json
import platform

import win32com
import win32com.client
import wmi


class Win32Info(object):
    def __init__(self):
        # 固定用法，更多内容请参考模块说明
        self.wmi_obj = wmi.WMI()
        self.wmi_service_obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        self.wmi_service_connector = self.wmi_service_obj.ConnectServer(".", "root\cimv2")

    def get_cpu_info(self):
        """获取CPU的相关数据，这里只采集了三个数据"""
        data = {}
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores
        cpu_model = cpu_lists[0].Name  # CPU型号（所有的CPU型号都是一样的）
        data["cpu_count"] = len(cpu_lists)  # CPU个数
        data["cpu_model"] = cpu_model
        data["cpu_core_count"] = cpu_core_count  # CPU总的核数
        return data

    def get_ram_info(self):
        """收集内存信息"""
        data = []
        # 这个模块用SQL语言获取数据
        ram_collections = self.wmi_service_connector.ExecQuery("Select * from Win32_PhysicalMemory")
        for item in ram_collections:  # 主机中存在很多根内存，要循环所有的内存数据
            ram_size = int(int(item.Capacity) / (1024 ** 3))  # 转换内存单位为GB
            item_data = {
                "slot": item.DeviceLocator.strip(),
                "capacity": ram_size,
                "model": item.Caption,
                "manufacturer": item.Manufacturer,
                "sn": item.SerialNumber,
            }
            data.append(item_data)  # 将每条内存的信息，添加到一个列表里
        return {"ram": data}  # 再对data列表封装一层，返回一个字典，方便上级方法的调用

    def get_motherboard_info(self):
        """获取主板信息"""
        computer_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = dict()
        data['manufacturer'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        return data

    def get_disk_info(self):
        """硬盘信息"""
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():  # 每块硬盘都要获取相应信息
            item_data = dict()
            iface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type'] = iface
                    break
            else:
                item_data['iface_type'] = 'unknown'
            item_data['slot'] = disk.Index
            item_data['sn'] = disk.SerialNumber
            item_data['model'] = disk.Model
            item_data['manufacturer'] = disk.Manufacturer
            item_data['capacity'] = int(int(disk.Size) / (1024 ** 3))
            data.append(item_data)
            return {'physical_disk_driver': data}

    def get_nic_info(self):
        """网卡信息"""
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = dict()
                item_data['mac'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ip_address'] = nic.IPAddress[0]
                    item_data['net_mask'] = nic.IPSubnet
                else:
                    item_data['ip_address'] = ''
                    item_data['net_mask'] = ''
                data.append(item_data)
        return {'nic': data}


def collect():
    data = {
        'os_type': platform.system(),
        'os_release': "%s %s  %s " % (platform.release(), platform.architecture()[0], platform.version()),
        'os_distribution': 'Microsoft',
        'asset_type': 'server'
    }

    # 分别获取各种硬件信息
    win32obj = Win32Info()
    data.update(win32obj.get_cpu_info())
    data.update(win32obj.get_ram_info())
    data.update(win32obj.get_motherboard_info())
    data.update(win32obj.get_disk_info())
    data.update(win32obj.get_nic_info())

    return data


# ---------测试------------
if __name__ == '__main__':
    coll = collect()
    # 装成json
    coll_json = json.dumps(coll)
    print(coll_json)
