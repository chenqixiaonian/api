#-*- coding:utf8 -*-
#update api data from swagger

from common.scripts.gen_code_swagger import Print
from common.conf.conf import root_path
import os, difflib

#以下三个字段为参数...

url = 'http://qaecm-finance-accounting.soa.yeshj.com/swagger.json' #swagger地址
base_name = 'Finance' #服务名称 会作为对象和文件的名的一部分出现
service_file = 'sub_service_3' #接口文件数据对应的文件夹名

#根据以上参数拉取swagger上接口生成对象文件和现有的对象文件做对比，如不一致则打印不一致之处并做更新

target_file_path = root_path + '/{service_file}/api/product_template'.format(service_file=service_file)
update_file_path = root_path + 'common/scripts/temp_file'


#开始拉取swagger上内容生成文件
p = Print(url=url, base_name=base_name)
p.analyze_test_data()

def file_name(file_dir):

    all_file = list()
    for root, dirs, files in os.walk(file_dir):
        print ('root_dir:', root)
        print ('sub_dir:', dirs)
        print ('files:', files)
        all_file.extend(files)

    return all_file

def diff_file(a_path, b_path):
    a = open(a_path, 'r').readlines()
    b = open(b_path,'r').readlines()
    diff = difflib.Differ()
    diff_list = list(diff.compare(a,b))
    print("\033[033m',{},'\033[0m".format("===========比较结果如下=========="))
    is_diff = False
    for line in diff_list:
        if line[0] in ['-', '+']:
            is_diff = True
            print line
    return is_diff

target_file_names = file_name(target_file_path)
update_file_names = file_name(update_file_path)

#开始对比文件
for update_file_name in update_file_names:
    update_file = update_file_path + "/" + update_file_name
    target_file = target_file_path + "/" + update_file_name

    if update_file_name not in target_file_names:
        add_str = '新增了接口文件{}'.format(update_file_name)
        print ("\033[036m {} \033[0m".format(add_str))

    else:
        is_diff = diff_file(update_file, target_file)
        if is_diff is True:
            #替换文件
            pass
