#-*- coding:utf8 -*-
import configparser, os
#from common.log.Logger import log

conf_path = os.path.dirname(os.path.abspath(__file__))

root_path = os.path.dirname(conf_path)

def get_conf(path):
    conf = configparser.ConfigParser()
    conf.read(path, encoding='utf-8')

    return conf

def _host_conf():
    conf =get_conf(path=os.path.join(conf_path, 'api_host.ini'))
    return conf

def _db_conf():
    conf = get_conf(path=os.path.join(conf_path, 'mysql.ini'))
    return conf

def get_host(host):
    section = 'host'
    conf = _host_conf()
    return conf.get(section, host)


db_conf = _db_conf()
host_conf = _host_conf()

def init_engine_key(db_type='postgresql', section_name='db_product'):
    """
    初始化数据库引擎的链接字符串
    :param db_type: postgresql or oracle
    :param section_name: conf.conf中的mysql.ini section name
    :return:
    """
    engine_str = "{db_type}://{user}:{pw}@{host}:{port}/{db}"
    engine_str = engine_str.format(user=db_conf.get(section_name,'user'),
                                   pw=db_conf.get(section_name, 'pw'),
                                   host=db_conf.get(section_name, 'host'),
                                   port=db_conf.get(section_name, 'port'),
                                   db=db_conf.get(section_name, 'db'),
                                   db_type=db_type)