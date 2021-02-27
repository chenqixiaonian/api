__author__ = 'Administrator'
#coding=utf8

import numpy as np
import pandas as pd
import copy

rules = list()

def add_rule(c, target_c, func):
    rule = Rule()
    rule.c_map =[c, target_c]
    rule.rule = func
    rules.append(rule)

def to_equal(c_value):
    return str(c_value)

class Rule(object):
    def __init__(self):
        self.c_map = []
        self.rule = None

class DataUtil(object):
    def __init__(self):
        self.file_path = '/Users/yinyuting/Desktop/test.xlsx'
        self.df = None
        self.index = None #默认index为None，生成序号list('01234..')
        self.column = list('ABCD')

    def excel_to_df(self, path):
        self.df = pd.read_excel(path)

    def add_series(self):
        self.df = pd.Series([1,3,5,np.nan,6,8])

    def create_datetime_index(self, start=2013010):
        self.index = pd.date_range(start, periods=6)

    def create_data(self):
        self.df = pd.DataFrame(np.random.random(6,4),index = self.index,columns=self.column)

    def create_customize_data(self, data=dict()):
        self.df = pd.DataFrame(dict(A=1.,B=pd.Timestamp('20130102'),C=pd.Series(1, index=list(range(4)),dtype='float32'),
                                    D=np.array([3]*4, dtype='int32'),
                                    E=pd.Categorical(["test", "train", "test", "train"]),
                                    F='foo'),)

    def show_df(self):
        print "========表内容======="
        print self.df
        print "==========self.df.dtypes()========="
        print self.df.dtypes
        print "==========self.df.head(1)打印第一行数据========"
        print self.df.head(n=1)
        print "============self.df.tail(1)========"
        print self.df.tail(1)
        print "========self.df.index========"
        print self.df.index
        print "==========self.df.columns======"
        print self.df.columns
        print "==========self.df.tonumpy()打印表数据内容不包含行头和序号，返回列表========="
        print self.df.to_numpy()
        print "==========self.df.sort_index(axis=1, ascending=False)排序=========="
        print "============self.df.sort_values(by=\'B\')排序"
        print self.df.sort_index(axis=1, ascending=False)
        print self.df.sort_values(by='B')
        #取单独的列
        print self.df['A']
        print self.df[0:2]
        print self.df['20130102':"20130104"] #取序号20130102到序号20130104的数据
        #通过label取
        print self.df.loc['2']
        print self.df.loc[:,['A','B']] #行切片，列名字列表
        print self.loc["20130102":"20130104",['A','B']]
        print self.loc['20130104', ['A','B']]

        #取一个特定的值
        print self.df.loc['20130104', 'A']
        print self.df[self.df.A>0]

    def set_value(self):
        """
        设置值
        df.at[dates[0], 'A']=0
        df.iat[0,1] =0
        df.loc[:,'D']=np.array([5]*len(df))

        """
        pass

    def del_nan(self):
        """
        处理空情况
        df1.droppa(how='any') 删除掉任何有空的行
        df1.fillna(value=5) 填充所有的空为某个值
        :return:
        """

    def go_excel(self, df=None):
        df = df if df else self.df
        df.to_excel(self.file_path)

    def go_csv(self):
        self.df.to_csv(self.file_path)

    def to_other_excel(self, target_excel_path, rules):
        target_columns = pd.read_excel(target_excel_path).columns
        origin_index = self.df.index
        target_df = pd.DataFrame('', index=list(range(len(origin_index))),
                                 columns=list(target_columns))
        for rule in rules:
            origin_c, target_c = rule.c_map
            func = rule.rule
            origin_c_values = self.df[origin_c]
            target_values = copy.deepcopy(target_df.loc[:,[target_c]])
            target_df.loc[:,target_c]=np.array([target_values.iat[index, 0]+func(v)for index, v in enumerate(origin_c_values)])
            target_df.to_excel(target_excel_path)

#添加规则
add_rule('序号', '序号', to_equal)
add_rule('数字', '年龄', to_equal)
add_rule('数字2', '年龄', to_equal)
add_rule('数字3', '年龄', to_equal)
add_rule('字符', '班级', to_equal)
add_rule('字符2', '班级', to_equal)

data=DataUtil()
data.excel_to_df("/Users/yinyuting/Documents/test_script/origin_file.xlsx")
data.to_other_excel("/Users/yinyuting/Documents/test_script/origin_file.xlsx", rules=rules)

