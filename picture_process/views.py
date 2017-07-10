#coding=utf8
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from models import FrontConfig
import uuid
import traceback
from base_ps_action import BasePsAction
from PIL import Image, ImageDraw, ImageFont
import traceback
base_dir = r'/home/yxy/workspace/pymagic/picture_process/static/picture_process'
logger = logging.getLogger("django")

def fill_information(request):
    """
    填写资料页面
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
        context["index"] = index
        info = front_config.info
        info_json = json.loads(info)
        base_file_name = info_json["base_file_name"]
        context["base_file_name"] = base_file_name
        base_file_url = '%s/image/%s' % ("http://www.a4tiku.com/static/picture_process", base_file_name)
        context["base_file_url"] = base_file_url
        input_tags = info_json["input_tags"]
        context["input_size"] = len(input_tags)
        context["input_span"] = range(0, len(input_tags))
        context["input_tags"] = info_json["input_tags"]
        logger.info(context)
        return render(request, "ps_template.html", context)
    return None

def show_index(request):
    """
    前端索引页面(无弹窗关注)
    :param request:
    :return:
    """
    try:
        logger.info("into front_index")
        front_config_arr = FrontConfig.objects.all().order_by("id").reverse()
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

def show_index2(request):
    """
    前端索引页面,(弹窗关注)
    :param request:
    :return:
    """
    try:
        logger.info("into front_index2")
        front_config_arr = FrontConfig.objects.all().order_by("id").reverse()
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
        return render(request, "index2.html", context)
    except Exception as err:
        traceback.print_stack()
        return None

def show_pic(request):
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
        logger.info("...............")
        logger.info(ps_points)
        ps_info["coordinate_info"] = []
        for key in ps_points.keys():
            pos_info = ps_points.get(key)
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
        logger.info(ps_info)
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


def _get_post_data(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

