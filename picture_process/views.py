#coding=utf8
from django.shortcuts import render
import json
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from models import FrontConfig
import uuid
import traceback

logger = logging.getLogger("django")
base_dir = r'/home/yxy/workspace/pymagic/picture_process/static/picture_process'

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
            coordinate_info = self._ps_info.get("coordinate_info")
            ori_pic_url = self._ps_info.get("ori_pic_url")
            dest_pic_url = self._ps_info.get("dest_pic_url")
            base_file = "%s/image/%s" %(base_dir, ori_pic_url)
            dest_file = "%s/result/%s"  %(base_dir, dest_pic_url)
            base_img = Image.open(base_file)
            draw = ImageDraw.Draw(base_img)
            for element in coordinate_info:
                logger.info(element)
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

def front_ps(request):
    """
    前端页面
    :param request:
    :return:
    """
    index = request.GET.get("index")
    logger.info(index)
    front_config = FrontConfig.objects.get(index=index)
    tpl_type = front_config.tpl_type
    info = front_config.info
    if tpl_type == 1:
        """
        #1模版
        """
        context = {}
        logger.info(info)
        logger.info(type(info))
        info_dict = json.loads(info)
        context = {}
        context["title"] = info_dict["title"]
        context["text_name"] = info_dict["text_name"]
        context["index"] = index
        info = front_config.info
        info_json = json.loads(info)
        base_file_name = info_json["base_file_name"]
        context["base_file_name"] = base_file_name
        base_file_url = '%s/image/%s' % ("http://www.a4tiku.com/static/picture_process", base_file_name)
        context["base_file_url"] = base_file_url
        return render(request, "ps_template.html", context)
    return None

def front_index(request):
    """
    前端索引页面
    :param request:
    :return:
    """
    try:
        logger.info("front_index")
        front_config_arr = FrontConfig.objects.all()
        logger.info(type(front_config_arr))
        result = []
        for row in front_config_arr:
            info = row.info
            info_json = json.loads(info)
            index = row.index
            name = info_json["title"]
            base_file_name = '%s/image/%s' % ("http://www.a4tiku.com/static/picture_process", info_json["base_file_name"])
            target_url = "http://www.a4tiku.com/zb/front/?index=%d" %(int(index))
            obj = {}
            obj["name"] = name
            obj["base_file_name"] = base_file_name
            obj["target_url"] = target_url
            obj["index"] = row.index
            result.append(obj)
        logger.info(result)
        context = {}
        context["result"] = result
        return render(request, "index.html", context)
    except Exception as err:
        traceback.print_stack()
        return None


def data_ps_get(request):
    """
    返回ps后的图片地址
    :param request:
    :return:
    """
    try:
        logger.info(request.GET)
        index = request.GET.get("index")
        logger.info("index:" + index)
        front_config = FrontConfig.objects.get(index=index)
        info = front_config.info
        info_json = json.loads(info)

        ps_info = {}
        base_file_name = info_json["base_file_name"]
        ps_info["ori_pic_url"] = base_file_name

        dest_file_name = "%s.jpeg" % (uuid.uuid1())
        ps_info["dest_pic_url"] = dest_file_name

        ps_points = info_json["points"]
        logger.info(ps_points)
        for key in ps_points.keys():
            pos_info = ps_points.get(key)
            ps_info["coordinate_info"] = []
            obj = {}
            obj["p_x"] = pos_info["p_x"]
            obj["p_y"] = pos_info["p_y"]
            obj["text"] = pos_info["text"]
            if request.GET.get(key) != None:
                obj["text"] = request.GET.get(key)
                logger.info("key:" + key)
                logger.info(obj["text"])
            font_file_name = pos_info["font"]
            logger.info(font_file_name)
            font_size = int(pos_info["font_size"])
            logger.info(font_size)
            base_font = '%s/font/%s' % (base_dir, font_file_name)
            m_font = ImageFont.truetype(base_font, size=font_size)
            obj["font"] = m_font
            obj["color"] = pos_info["color"]
            ps_info["coordinate_info"].append(obj)
        logger.info("finished")
        action = BasePsAction(ps_info)
        action.run()
        data = {}
        data['url'] = '%s/result/%s' % ("http://www.a4tiku.com/static/picture_process", dest_file_name)
        logger.info(data)
        return render(request, "pic_show.html", data)
    except Exception as err:
        logger.error(err)
        traceback.print_stack()
        return None


@csrf_exempt
def data_ps(request):
    """
    返回ps后的图片地址
    :param request:
    :return:
    """
    try:
        logger.info(request.POST)
        index = request.POST.get("index")
        logger.info("index:" + index)
        front_config = FrontConfig.objects.get(index=index)
        info = front_config.info
        info_json = json.loads(info)

        ps_info = {}
        base_file_name = info_json["base_file_name"]
        ps_info["ori_pic_url"] = base_file_name

        dest_file_name = "%s.jpeg" % (uuid.uuid1())
        ps_info["dest_pic_url"] = dest_file_name

        ps_points = info_json["points"]
        logger.info(ps_points)
        for key in ps_points.keys():
            pos_info = ps_points.get(key)
            ps_info["coordinate_info"] = []
            obj = {}
            obj["p_x"] = pos_info["p_x"]
            obj["p_y"] = pos_info["p_y"]
            obj["text"] = pos_info["text"]
            if request.POST.get(key) != None:
                obj["text"] = request.POST.get(key)
                logger.info(obj["text"])
            font_file_name = pos_info["font"]
            logger.info(font_file_name)
            font_size = int(pos_info["font_size"])
            logger.info(font_size)
            base_font = '%s/font/%s' % (base_dir, font_file_name)
            m_font = ImageFont.truetype(base_font, size=font_size)
            obj["font"] = m_font
            obj["color"] = pos_info["color"]
            ps_info["coordinate_info"].append(obj)
        logger.info("finished")
        action = BasePsAction(ps_info)
        action.run()
        data = {}
        data['url'] = '%s/result/%s' % ("http://www.a4tiku.com/static/picture_process", dest_file_name)
        logger.info(data)
        return _get_post_data(data)
    except Exception as err:
        logger.error(err)
        traceback.print_stack()
        return None

@csrf_exempt
def query_base_url(request):
    """
    获取index对应的ps底图
    :param request:
    :return:
    """
    index = request.POST.get("index")
    logger.info(index)
    front_config = FrontConfig.objects.get(index=index)
    info = front_config.info
    info_json = json.loads(info)
    base_file_name = info_json["base_file_name"]
    data = {}
    data["url"] = '%s/image/%s' % ("http://www.a4tiku.com/static/picture_process", base_file_name)
    return _get_post_data(data)

@csrf_exempt
def query_index_data(request):
    """
    获取索引列表的数据
    :param request:
    :return:
    """
    front_config_arr = FrontConfig.objects.all()
    logger.info(type(front_config_arr))
    data = {}
    data["status"] = 0
    return _get_post_data(data)


def _get_post_data(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

