import datetime
import json
from urllib import request
from urllib.parse import urlencode

from client.core import infocollection
from cmdb import settings


class ArgvHandler(object):
    def __init__(self, args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        '''分析参数，如果有参数指定的功能，则执行该功能，在这里即“collect_data”，“report_data”
        如果没有，打印帮助说明。'''

        if len(self.args) > 1 and hasattr(self, self.args[1]):
            func = getattr(self, self.args[1])
            func()
        else:
            self.help_msg()

    @staticmethod
    def help_msg():
        '''帮助说明'''

        msg = '''
        collect_data    收集硬件信息
        report_data     收集硬件信息并汇报
        '''
        print(msg)

    @staticmethod
    def collect_data():
        '''收集硬件信息,用于测试！'''

        info = infocollection.InfoCollect()
        asset_data = info.collect()
        print(asset_data)

    @staticmethod
    def report_data():
        '''收集硬件信息，然后发送到服务器。'''

        # 收集信息
        info = infocollection.InfoCollect()
        asset_data = info.collect()

        # 将数据打包到一个字典内，并转换为json格式
        data = {'asset_data': json.dumps(asset_data)}

        # 根据settings中的配置，构造url
        url = "http://%s:%s%s" % (settings.PARAMS['server'], settings.PARAMS['port'], settings.PARAMS['url'])
        print('正在将数据发送至： [%s]  ......' % url)
        try:
            data_encode = urlencode(data, encoding='utf-8')
            requ = request.Request(url=url, data=data_encode.encode(), method='POST')
            with request.urlopen(requ, timeout=settings.PARAMS['request_timeout']) as resp:
                print('发送成功！')
                message = '成功:%s' % resp.read().decode()
                print('返回结果：%s' % message)
        except Exception as e:
            message = '失败:%s' % e
            print('发送失败：%s' % message)

        # 记录日志
        with open(settings.LOGPATH, mode='ab') as fh:
            string = '发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n' % (
                datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), url, message)
            fh.write(string.encode())
            print('日志记录成功!')
