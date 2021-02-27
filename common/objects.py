#-*- coding:utf8 -*-
class BaseObj(object):
    def __init__(self, **kwargs):
        self.update_value(**kwargs)

    def set_doc(self, doc):
        self.__doc__ = doc

    def doc(self):
        return self.__doc__

    def update_value(self, **kwargs):
        if kwargs:
            for attribute_name in kwargs.keys():
                setattr(self, attribute_name, kwargs.get(attribute_name))

    def get_value(self, name, default=None):
        """
        获取对象的属性值
        :param name: 属性名
        :param default: 如果没有返回的默认值
        :return:
        """
        value = getattr(self, name, default)
        if value is None:
            return default
        else:
            return value

    def clear_value(self):
        for k, v in vars(self).items():
            setattr(self, k, None)

class AttrDict(dict):
    """
    usage:
    JOIN = attrdict(
    INNER = 'INNER',
    LEFT_OUTER = 'LEFT OUTER',
    RIGHT_OUTER = 'RIGTH OUTER',
    FULL = 'FULL',
    FULL_OUTER = 'FULL OUTER',
    CROSS = 'CROSS'
    NATURAL = 'NATURAL')

    """
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        self[attr] = value

    def __iadd__(self, rhs):
        self.update(rhs)
        return self

    def __add__(self, rhs):
        d = AttrDict(self)
        d.update(rhs)
        return d

    def get(self, key, none_default=None, default=None):
        """

        :param key:
        :param none_default:如果不存在key或取值为空则取默认值
        :param default: 如果不存在key则为空
        :return:
        """
        if none_default and default:
            raise NameError('不能同时使用none_default 和default两个字段')
        value = super().get(key, default)
        if value is not None:
            return value
        elif default is not None:
            return default
        elif none_default is not None:
            return none_default

    def has_key(self, key):
        if key in self:
            return True
        else:
            return False

class BaseAttribute(object):
    def __init__(self):
        self.value = [self]
        self.name = None
        self.key = None

class Pagination(BaseObj):
    def __init__(self, **kwargs):
        self.page_size = None
        self.page_num = None
        super(Pagination, self).__init__(**kwargs)

class DefiningObj(object):
    def __init__(self):
        pass
