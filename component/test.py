#!coding=utf8
#!/usr/bin/env python
'''
Copyright: Copyright (c) 2017
@description:
@author xiaoyun.yang
@date 2017年06月30日
@version 1.0
'''
import json
import os
import sys

str = "{\"title\":\"雅思成绩单\",\"text_name\":\"姓名\"}"
dt = json.loads(str)
print dt['text_name']