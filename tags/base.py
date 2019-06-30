import re

from utils.log import get_logger

LOG = get_logger('tags')

class Tags(object):
    '''标签的基类'''

    def __init__(self, url, data):
        self._data = data
        self.url = url

    def _deal_data(self, data=None):
        '''
        将网页数据转换为以行为单位的字符串列表
        :param data: 请求的得到的响应数据
        :return: 标签字符串列表
        '''
        data = data if data else self._data
        if isinstance(data, str):
            LOG.info('将字符数据转换为切割为列表')
            str_list = re.split(r'\r\n|\n|\r', data)
        else:
            str_list = []
        return str_list

    @classmethod
    def _change_str_dict(cls, key, value):
        return {key : value}

    @classmethod
    def _get_content(cls, data):
        RULE = r'<.*?>(.*)</.*?>'
        LOG.debug('获取标签的内容')
        res = re.search(RULE, data, re.S)
        if res:
            res = res.group(1)
        return res

    def _get_tag_result(self, data=None):
        '''
        标签提取方法，使用制定的规则提取指定的标签数据
        :param data: 标签字符串
        :return: 标签列表
        '''
        data = data if data else self._data
        res_list = re.findall(self.RULE, data, re.S)
        ret_list = []
        LOG.debug('开始组成数据，添加标签和标签属性')
        for item in res_list:
            item = self._change_str_dict('tag', item)
            item['content'] = self._get_content(item.get('tag'))
            ret_list.append(item)
        return ret_list

    def _get(self):
        '''
        标签获取的入口，调度，拿到标签列表
        :return: 标签列表
        '''
        res_list = []
        for str_item in self._deal_data():
            res_list.extend(self._get_tag_result(str_item))
        for res_item in res_list:
            ret = self._get_tag_result(res_item.get('tag')[2:-3])
            if ret:
                res_list.extend(ret)
        return res_list

    def findall(self):
        '''
        数据输出的出口
        :return: 标签列表
        '''
        return self._get()


class BaseAttribute(object):
    '''属性的基类'''

    def __init__(self, url=None, data=None, attrs=[]):
        self.url = url
        self._data = data
        self._attrs = attrs
        self._res_list = []

    def _get_res(self, data, RULE, attr):
        '''根据规则提取对应的属性'''
        for data_item in data:
            res = re.search(RULE, data_item.get('tag'), re.S)
            if res:
                res = res.group(2)
                if not res.startswith('http'):
                    LOG.debug('地址不完整尝试完善地址')
                    if res.startswith('./'):
                        res = res[1:]
                    if self.url.endswith('/') and res.startswith('/'):
                        res = res[1:]
                    if not self.url.endswith('/') and res.startswith('/'):
                        res = '/' + res
                    res = self.url + res
                data_item[attr] = res
            self._res_list.append(data_item)
        return data

    def get_attr(self, data=None):
        '''分别提取不同的属性'''
        data = data if data else self._data
        for attr in self._attrs:
            rule_name = '_get_%s' % attr
            LOG.info('开始提取%s属性' % attr)
            RULE = getattr(self, rule_name)()
            self._get_res(data, RULE, attr)
        return self._res_list

    def _get_href(self):
        '''属性的规则方法'''
        return r'href\s*?=\s*(\'|\")(\S+?)(\'|\")'