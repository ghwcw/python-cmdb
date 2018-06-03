import platform
import sys

from client.plugins.linux import linuxsysinfo
from client.plugins.win import winsysinfo


def linux_sys_info():
    return linuxsysinfo.collect()


def win_sys_info():
    return winsysinfo.collect()


class InfoCollect(object):
    def collect(self):
        # 收集平台信息
        # 首先判断当前平台，根据平台的不同，执行不同的方法
        try:
            func = getattr(self, platform.system())     # platform.system返回“Linux”或“Windows”，
            info_data = func()                          # 然后执行“Linux()”或“Windows()”方法
            formated_data = self.build_report_data(info_data)
            return formated_data
        except AttributeError:
            sys.exit("不支持当前操作系统： [%s]! " % platform.system())

    def Linux(self):

        return linux_sys_info()

    def Windows(self):
        return win_sys_info()

    def build_report_data(self, data):
        return data
