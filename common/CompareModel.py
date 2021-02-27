#-*- coding:UFT-8 -*-

#check模型
from common.log.Logger import log

tables= [] #存储需要对比的表名

class AssertObj(object):
    def __init__(self, attrs=[]):
        """
        需要对比的对象模型
        """
        self._init_attrs(attrs)

    def _init_attrs(self, attrs):
        for attr in attrs:
            setattr(self, attr, list())

    def reload(self, pw):
        """
        重新拉取数据库中的各表信息
        :param pw:
        :return:
        """
        del_attr = ["error_list"]
        for attri in self.__dict__.keys():
            if str(attr).startswith("_") or attri in del_attr:
                pass
            else:
                log.info("开始reload{}的数据库数据".format(attri))
                f = getattr(pw, attri)
                setattr(self, attri, f(is_normal_obj=True))

class CompareModel(object):
    def __init__(self, business_info=None, tables=[], pw=None):
        super(CompareModel, self).__init__()
        self.business_info = business_info #业务对象模型
        self.expect_obj = AssertObj(tables)
        self.actual_obj = AssertObj(tables)
        self.pw = pw #数据库
        self.exclude = list() #需要排除的字段列表

    def init_info(self, **kwargs):
        """
        初始化业务对象
        :param activity_obj: 创建活动request_obj
        :param generate_obj: 生成兑换码批次和码request_obj
        :param receive_obj: 领取兑换码request_obj
        :return:
        """
        pass
        return self

    def add_tables(self, table_names:list):
        for table_name in table_names:
            self.add_table(table_name_key = table_name)

    def add_table(self, table_name_key, **kwargs):
        """
        根据表名请求计算的表结构和值，同时请求数据库中的值，用于后面对比
        :param table_name_key:
        :param kwargs:
        :return:
        """
        exp_func = getattr(self.business_info, table_name_key)
        actual_func = getattr(self.pw, table_name_key)

        exp_order = exp_func(**kwargs)
        act_order = actual_func(**kwargs)
        setattr(self.expect_obj, table_name_key, exp_order)
        setattr(self.actual_obj, table_name_key, act_order)

    def do(self, ex=None):
        self.exclude.extend(ex) if ex else  self.exclude
        log.step('开始对比如下数据:{}'.format(self.actual_obj.__dict__.keys()))
        from common.ObjAssert import ObjAssert
        check = ObjAssert()
        check.is_equal(exp_obj = self.expect_obj,
                       act_obj = self.actual_obj,
                       is_toggle = False,
                       ex = self.exclude)

    def reload_actual_order(self):
        """
        重新从数据库拉取表信息
        :return:
        """
        self.actual_obj.reload(self.pw)