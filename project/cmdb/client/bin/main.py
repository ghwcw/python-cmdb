#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from ..core import handler


BASE_DIR = os.path.dirname(os.getcwd())

# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    """
    以模块的形式执行python -m；
    执行方法，在terminal进入目录cmdb，输入：python -m client.bin.main 方法名；
    注意：此处文件路径用圆点“.”代替斜杠“/”。
    """
    handler.ArgvHandler(sys.argv)
