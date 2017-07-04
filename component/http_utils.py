#!coding=utf8
#!/usr/bin/env python
'''
Copyright: Copyright (c) 2017
@description:
@author xiaoyun.yang
@date 2017年06月30日
@version 1.0
'''

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

class QiNiuManager():
    def __init__(self):
        access_key="6GFM0mpIBfX4YF4fhuF2jnQvE10i1Vi-HLblbmIm"
        secret_key="-C56VUYOxf4mFKPvax4T7hoGkTontg7v9rjtVcHq"
        self._bucket_name = "pymagic"
        self._q = Auth(access_key, secret_key)

    def upload(self, ori_file_path, dest_file_name):
        """
        将文件上传到七牛
        :param ori_file_path: 原始文件的路径
        :param dest_file_name: 上传到七牛后的名字
        :return:
        """
        #获取token，可指定过期时间
        token = self._q.upload_token(self._bucket_name, dest_file_name, 3600)
        ret, info = put_file(token, dest_file_name, ori_file_path)
        print ret
        print type(ret)
        print info
        print type(info)

if __name__=="__main__":
    manager = QiNiuManager()
    ori_file_path = '/home/yxy/workspace/pymagic/picture_process/static/picture_process/result/fda.jpeg'
    dest_file_name = 'fda1.jpeg'
    manager.upload(ori_file_path, dest_file_name)


