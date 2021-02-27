#-*- coding:utf-8 -*-
from common.log import Logger
log = Logger()

class ObjAsser(object):
    def __init__(self):
        """
        所有pw结果带id的必须自行加上id
        :return:
        """
        self.error_list = [] #todo rename error_list

    def error_print(self, title=None):
        if self.error_list:
            log.error(title)
            for error in self.error_list:
                print('\n')
                log.error(msg = error)
            self.print_order_id_diff() #query 比较开关
            print('=====================END=============')

    def is_equal(self, exp_obj, map=None, is_update_api=False, is_toggle=True,
                 is_assert=True, ex=[], external_msg="", act_obj=None):
        """
        对比接口与peewee返回的结果
        :param exp_obj: 期望结果对象，结构要与实际结果一致
        :param map:
        :param is_update_api: 这个传True，会排除掉传入的request或者返回的response中为空，但数据库中有值得数据，
        主要用于更新的这类接口，需求：如果数据库有值而传入的值为空，则不更新数据库
        :param is_toggle: 是否要在对比过程中将act_obj中的驼峰字段名转换成下划线类型字段名，默认True转换
        :param is_assert:
        :param ex:
        :param external_msg:
        :param act_obj:
        :return:
        """
        if act_obj is None:
            act_obj = self
            self.for_obj(act_obj=act_obj, exp_obj=exp_obj, map=map, is_toggle=is_toggle, ex=ex)

        if is_update_api and self.error_list:
            error_list_tmp = self.error_list.copy()
            #加入是更新类的api 则数据库中有值， 传入值为空， 判断为正确， 从错误列表中排除
            for item in error_list_tmp:
                if item.get('act_value') is None:
                    self.error_list.remove(item)
            self.error_print("====================Update API Strip None========")

        if is_assert:
            self.error_print("=========Assert Error Msg{}==========".format(external_msg))
            check_equal(act_v=self.error_list, exp_v=[], err_msg='API Test Fail!!!!')

        else:
            return self.error_list

