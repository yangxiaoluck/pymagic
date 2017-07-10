#!coding=utf8
#!/usr/bin/env python
'''
Copyright: Copyright (c) 2017
@description:
@author xiaoyun.yang
@date 2017年07月10日
@version 1.0
'''
import logging
from PIL import Image, ImageDraw, ImageFont
import traceback
base_dir = r'/home/yxy/workspace/pymagic/picture_process/static/picture_process'
logger = logging.getLogger("django")

class BasePsAction():

    def __init__(self, ps_info):
        self._ps_info = ps_info

    def validate(self):
        if "ori_pic_url" not in self._ps_info.keys()\
                or "dest_pic_url" not in self._ps_info.keys():
            return False
        return True

    def run(self):
        try:
            if False == self.validate():
                logger.error("params error, _ps_info:%s"%(str(self._ps_info)))
                return
            logger.info("coordinate_info")
            coordinate_info = self._ps_info.get("coordinate_info")
            logger.info(coordinate_info)
            ori_pic_url = self._ps_info.get("ori_pic_url")
            dest_pic_url = self._ps_info.get("dest_pic_url")
            base_file = "%s/image/%s" %(base_dir, ori_pic_url)
            dest_file = "%s/result/%s"  %(base_dir, dest_pic_url)
            base_img = Image.open(base_file)
            draw = ImageDraw.Draw(base_img)
            for element in coordinate_info:
                logger.info("---------------")
                logger.info(element)
                logger.info("---------------")
                point = (int(element.get("p_x")), int(element.get("p_y")))
                logger.info(point)
                text = element.get("text")
                logger.info(type(text))
                font = element.get("font")
                color = element.get("color")
                draw.text(point, text, font=font, fill=color)
            base_img.save(dest_file, 'jpeg')
            return 0
        except Exception as e:
            traceback.print_stack()
            return -1