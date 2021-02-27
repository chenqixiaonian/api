#-*- coding:utf8 -*-
#该脚本依赖WIKI格式，目前已弃用

import string, requests, sys

from bs4 import BeautifulSoup

class GetData(object):
    def __init__(self):
        self.urls = ['http://wiki.yeshj.com/pages/viewpage.action?pageId=43230375']

    def test(self):
        result = []
        for url in self.urls:
            html = self.send_request(url)
            result.append(self.deal_info(html))

        return result

    def deal_info(self, html):
        soup = BeautifulSoup(html)
        title_string = soup.title.string
        desc = title_string.split(' ')[0]

        url=''

        if soup.find(text='GET'):
            url = soup.find(text='GET').parent.nextSibling
        if soup.fin(text='Get'):
            url = soup.find(text='Get').parent.nextSibling
        if soup.fin(text='get'):
            url = soup.find(text='get').parent.nextSibling
        if soup.fin(text='POST'):
            url = soup.find(text='POST').parent.nextSibling
        if soup.fin(text='Post'):
            url = soup.find(text='Post').parent.nextSibling
        if soup.fin(text='post'):
            url = soup.find(text='post').parent.nextSibling
        if soup.fin(text='PUT'):
            url = soup.find(text='PUT').parent.nextSibling
        if soup.fin(text='Put'):
            url = soup.find(text='Put').parent.nextSibling
        if soup.fin(text='put'):
            url = soup.find(text='put').parent.nextSibling
        url_text = url.strip()

        if '>get<' in html or '>Get<' in html or '>GET<' in html:
            method = 'GET'
        if '>post<' in html or '>Post<' in html or '>POST<' in html:
            method = 'POST'
        if '>put<' in html or '>Put<' in html or '>PUT<' in html:
            method = 'PUT'

        url = url_text[1:] if url_text[0]=='/' else url_text
        class_name = self.gen_class_name(url)
        class_name_obj = self.gen_class_name_obj(url)
        function_name = self.gen_function_name(url)

        args=[]

        for tr in soup.find('table').find('tbody').findAll('tr'):
            td = tr.find('td')
            if td and self.is_chinese(td.text) is False:
                k = td.text
                args.append(k)
        return dict(class_name=class_name, desc=desc,url=url, args_list=args,
                    method=method, function_name= function_name, class_name_obj = class_name_obj)


    def gen_class_name_obj(self, url):
        name = ''
        for s in url.split('/'):
            if '?' in s:
                s = s.split('?')[0]
            if s[0] == '{':
                s = s[1:-1]
            if s[0]=='(' or s[0] =='（':
                s = ''
            elif s[-1]==')':
                s = s[:-1]
            name = name + s +'_'
        return name[:-1]

    def gen_function_name(self, url):
        return 'request_'+ self.gen_class_name_obj(url)

    def gen_class_name(self, url):
        name = ''
        for s in url.split('/'):
            if '?' in s:
                s = s.split('?')[0]
            if s[0] == '{':
                s = s[1:-1]
            if s[0]=='(' or s[0] =='（':
                s = ''
            elif s[-1]==')':
                s = s[:-1]
            name = name + s.capitalize()
        return name

    def send_request(self, url):
        cookies = {
            'dbtoolsauth':'0001ec35de.91c85bbe830548dabaeef219ce17f3f2',
            'ClubAuth':'99A1D24D277CFA2B078BD62182B651B64A52098F59984A42C4F353FDE19565B4456B3B97BBEABDDCAB9E5B2001A4F797DE81F10698ABE06ED4C33CABA4D5D49A544AD53CB8B70BFB90D04B8FA22DF86EB07341866E802C413C60C535ECCABD0E39B236369720548BB4A4F13FE800B9F6AF4337E42E5BFB5F30C56C270EC01336A4224A97B3E9E5C55A6E140A88332F97C00F2657CF18460AD6980AABDF6BF2D7AB93EF68',
            'hj_token':'s_1e339d1eb04dd1e8dddf53e1483a7cb5|M2Qx0GQ0Yg==',
            'JSESSIONID':'275321836D6DDF891903E9F9035EBA8E'
        }
        headers = dict(Cookie='seraph.confluence=38241931%3A1f8e23558cd13dab1182243fdf0ee77859b5a375;dbtoolsauth=0001ec35de.91c85bbe830548dabaeef219ce17f3f2; ClubAuth=99A1D24D277CFA2B078BD62182B651B64A52098F59984A42C4F353FDE19565B4456B3B97BBEABDDCAB9E5B2001A4F797DE81F10698ABE06ED4C33CABA4D5D49A544AD53CB8B70BFB90D04B8FA22DF86EB07341866E802C413C60C535ECCABD0E39B236369720548BB4A4F13FE800B9F6AF4337E42E5BFB5F30C56C270EC01336A4224A97B3E9E5C55A6E140A88332F97C00F2657CF18460AD6980AABDF6BF2D7AB93EF68;hj_token=s_1e339d1eb04dd1e8dddf53e1483a7cb5|M2Qx0GQ0Yg==;ClubAuth_DEV=98D63412C3F380F5050BB62057A4721D2AEFFAE64BF8625564F6EB4D16B283C3DEFD9F9E483D5DC817083286572756351693823916414A5A03FC3E50EEB6BC181A05772986830422AABBBAEF0D5C9BEC3573B97E2C0D0B2DF834A34CBCB45B4CD54EF9820110752D8B67516C4F814F55874DADB43FFF7E6F7FB25550B69408D870A9E91064D579163CA7C899369BBA1E1C1BFB1FF20FF98E7787A884;JSESSIONID=275321836D6DDF891903E9F9035EBA8E;crowd.token_key=0dZ8Yux0sd0X31d8HqjJDw00;mywork.tab.tasks=False')
        result = requests.get(url=url, cookies=cookies, headers=headers)
        return result.text

    def is_chinese(self, uchar):
        '''
        判断一个unicode是否汉字
        '''
        if uchar>='\\u4e00' and uchar<='\\u9fa6':
            return True
        else:
            return False

    def is_number(self,uchar):
        if uchar>='/u0030' and uchar<='/u0039':
            return True
        else:
            return False

    def is_alphabet(self,uchar):
        if (uchar>='/u0041' and uchar<='/u005a') or (uchar >='/u0061' and uchar<='/u007a'):
            return True
        else:
            return False

    def is_other(self,uchar):
        if not (self.is_chinese(uchar) or self.is_number(uchar) or self.is_alphabet(uchar)):
            return True
        else:
            return False

    def B2Q(self, uchar):
        """
        半角转全角
        :param uchar:
        :return:
        """
        inside_code = ord(uchar)

        if inside_code<0x0020 or inside_code>0x7e: #不是半角字符就返回原来的字符
            return uchar
        if inside_code ==0x0020: #除了空格其他的全角半角的公式为：半角=全角-0xfee0

            inside_code = 0x3000

        else:
            inside_code+=0xfee0
        return chr(inside_code)

    def Q2B(self, uchar):
        inside_code = ord(uchar)


        if inside_code ==0x3000: #除了空格其他的全角半角的公式为：半角=全角-0xfee0

            inside_code = 0x0020

        else:
            inside_code+=0xfee0
        if inside_code<0x0020 or inside_code>0x7e: #转完之后不是半角字符返回原来的字符
            return uchar
        return chr(inside_code)

    def string2List(self, ustring):
        '''
        将USTING按照中文，字母，数字分开
        :param ustring:
        :return:
        '''
        retList = []
        utmp=[]

        for uchar in ustring:
            if self.is_other(uchar):
                if len(utmp)==0:
                    continue
                else:
                    retList.append(''.join(utmp))
                    utmp=[]
            else:
                utmp.append(uchar)

            if len(utmp)!=0:
                retList.append(''.join(utmp))
            return retList

class CodeGeneratorBackend(object):

    def begin(self, tab='\t'):
        self.code=[]
        self.tab = tab
        self.level = 0

    def end(self):
        return ''.join(self.code)

    def write(self, string):
        self.code.append(self.tab*self.level+string)

    def indent(self):
        self.level = self.level +1

    def dedent(self):
        if self.level == 0:
            raise  SyntaxError('internal error in code generator')
        self.level = self.level - 1

class CodeGeneratorResp(object):
    '''
    对返回值中嵌套的dict，list中dict、嵌套多层的dict自动在结构位置生成一个子类
    子类名称为大写的字段名，如字段名以s结尾，则去除s，如字段名为detailProducts,生成的类名为DetailProduct
    使用方法：
    初始化类，调用gen_code()方法
    '''
    def __init__(self, resp, root_name='Root', keep_value=False):
        '''
        :param resp: json格式内容
        :param root_name: 生成的类名，默认为Root
        :param keep_value: 是否依照resp给生成的类属性赋值默认，默认为False，即生成的类属性值均为None
        :return:
        '''
        self.resp = resp
        self.root_name = root_name
        self.keep_value = keep_value

    def gen_code(self):
        out = []
        tab = 4
        out.append('class %s(object):' % self.root_name)
        out.append(' '*tab + 'def __init__(self):')
        if isinstance(self.resp, list):
            out.append(' '*(tab+4)+'self.root=[]')
            out.append('\r')
            out.append(' '*tab + "class Root(object):")
            out.append(' '*(tab+4)+'def __init__(self):')
            out += self._gen_dict(self.resp[0], tab = (tab+8))

        elif isinstance(self.resp, dict):
            out += self._gen_dict(self.resp, tab = 8)

        for line in out:
            print line
        return out

    def _gen_dict(self, src_dict, tab):
        out = []
        multi = []
        for k,v in list(dict(src_dict).items()):
            if self.keep_value is True and isinstance(v, (dict, list)) is False:
                if isinstance(v, str):
                    v = '''"%s"''' % v
                out.append(' '*tab + "self.%s = %s" %(k,v))
            else:
                out.append(' '*tab +"self."+k+"=None")
            if isinstance(v, (dict, list)):
                multi.append(k)

        out.sort()
        tab -=4

        for k in multi:
            v = src_dict.get(k)
            out.append('\r')
            out.append(' '*tab + 'class '+ str(k[0].upper()+k[1:]).rstrip('s')+'(object):')
            out.append (" "*(tab+4)+'def __init__(self):')
            if isinstance(v, dict):
                out += self._gen_dict(v, tab=tab+8)
            if isinstance(v, list) and len(v)>0 and isinstance(v[0], dict):
                out += self._gen_dict(v[0], tab=tab+8)
        return out

if __name__ == '__main__':
    resp = {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhdXRoMCIsImV4cCI6MTU2OTEyMTg4NywiZGV2aWNlSWQiOiI1MTBFQTc5QS0zMUMwLTQzMDAtQjVDNC1BNzgxRDg4RkU4QjEiLCJ1c2VySWQiOiI4ZmQ2NDcwMmNjY2I0ODNkYmY5OTYwOGJiYzAyODcwNiJ9.1b0v1UvTZua4kQuW6CrAhZYdqzYJHu-eaVME2-U2NDw",
  "userId": "964c93af-dd5f-49cb-a0e6-f76219dea097_8911",
  "globalUserId": "8fd64702cccb483dbf99608bbc028706",
  "userType": None,
  "userChannelType": None,
  "version": "1",
  "deviceId": "510EA79A-31C0-4300-B5C4-A781D88FE8B1",
  "preMobile": "13523456789",
  "uNumber": "liyi1",
  "realname": "李一（经租BD）",
  "data": {
    "userId": "964c93af-dd5f-49cb-a0e6-f76219dea097_8911",
    "name": "",
    "preStatus": "3",
    "businessType": 1,
    "pageSize": 20,
    "pageNum": 1
  }
}
    root_name = 'Resp'
    gen = CodeGeneratorResp(resp=resp, root_name=root_name, keep_value=False).gen_code()