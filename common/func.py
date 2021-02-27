#-*- coding:utf8 -*-
import copy, socket
import csv
import datetime
import math
import time
import calendar
import decimal
import json
import random
import re, hashlib,operator
from tabulate import tabulate
from common.objects import BaseObj, Pagination
from common.log.Logger import log

def obj_to_real_obj(obj):
    for k, v in obj.__dict__.items():
        v_obj = over_obj(v)
        setattr(obj, k, v_obj)

def over_obj(v):
    if isinstance(v, dict):
        v_obj = json_to_obj(v)
        return v_obj
    elif isinstance(v, list) or isinstance(v, tuple):
        for index, item in enumerate(v):
            v[index] = over_obj(item)
        return v
    else:
        return v

def json_to_obj(json_content):
    from easy.base.model_base import ModelBase
    obj = json.loads(json.dumps(json_content, ensure_ascii=False), object_hook=ModelBase.to_model)

    return obj

def jsons_to_objs(jsons_list):
    for index, item in enumerate(jsons_list):
        jsons_list[index] = json_to_obj(item)
    return jsons_list

def merge_objs(*objs, ex=[], suffix=None):
    """
    合并对象
    :param objs:
    :param ex: 排除掉的字段
    :param suffix: 如果有重复字段则加这个作为后缀
    :return:
    """
    r = BaseObj()
    for obj in objs:
        for k, v in vars(obj).items():
            if not hasattr(r, k):
                setattr(r, k, v)
            elif k in ex:
                continue
            elif suffix:
                setattr(r, k+str(suffix), v)

    return r

def random_str(title='公共自动化商品', is_special_char=False):
    if is_special_char:
        title = title + '@#$~!#^&$**$^@%'
    return title + str(random.randint(0, 100000))

def random_only():
    return random.randint(0,1)

def random_amount():
    return round(random.random(), 2)

def random_from_list(items):
    index = random.randint(0, len(items))
    return items[index]

def random_boolen():
    return random.choice([True, False])

def random_float(n=2):
    return round((random.uniform(0, 10), n))

def random_int(start=0, end=99):
    return random.randint(start, end)

def long_str(n=10):
    s = '超长字段longstr'
    return s*n
def increase_str_time():
    return datetime.datetime.now().strftime('%m%d%H%M%S%f')

def str_convert_to_camel(one_string, space_character):
    #one_string: 输入的字符串； space_character:字符串的间隔符，以其作为分隔标志
    string_list = str(one_string).split(space_character) #将字符串转化为list
    first = string_list[0].lower()
    others = string_list[1:]

    others_capital = [word.capitalize() for word in others] #str.capitalize():将字符串的首字母转化为大写

    others_capital[0:0] =[first]
    



