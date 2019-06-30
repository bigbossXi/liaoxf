'''
====================
 数据请求和处理部分
====================
'''
import datetime
import random

import requests

from tags import tags_router
from utils import BASE_DIR
from utils.commons import get_now_and_four_randint
from utils.log import get_logger

LOG = get_logger('core')

class BaseRequest(object):

    def __init__(self):
        self.r = requests

    def decode_str(self, data):
        try:
            LOG.info('开始解码...')
            data = data.decode('utf-8')
        except Exception as e:
            LOG.warn('尝试使用utf-8解码失败，开始使用GBK解码...')
            try:
                data = data.decode('GBK')
            except Exception as e:
                LOG.error('解码失败,数据输出到文件...')
                filename = BASE_DIR + '/%s' % get_now_and_four_randint()
                try:
                    with open('%s' % filename, 'w') as f:
                        f.write(data)
                except Exception as e:
                    LOG.error('写入到文件失败...')
                else:
                    LOG.info('写入到文件成功，文件目录：%s' % filename)
                data = ''
        return data

    def _req_res(self, url):
        '''
        请求获取数据
        :param url: 资源路径
        :return: 资源数据json/str
        '''
        try:
            res = self.r.get(url)
        except Exception as e:
            LOG.error('请求数据失败，详情：%s' % e)
            return ''
        try:
            res = res.json()
        except Exception as e:
            LOG.info('数据并非json格式，按照二进制字符流处理...')
            res = self.r.get(url).content
            if isinstance(res, bytes):
                res = self.decode_str(res)
        return res

    def get(self, url, tags=[], attrs=[], rules='',  **kwargs):
        '''
        入口函数
        :param url: 请求资源路径
        :param tags: 想要提取的标签
        :param rules: 自定义规则
        :param kwargs: 其他参数
        :return: 数据列表
        '''
        if not tags and not rules:
            msg = '请选择标签或者输入规则'
            LOG.warn(msg)
            return msg
        self._data = self._req_res(url)
        self._res_data = {}
        for params in tags:
            handler = tags_router.get(params)
            if handler:
                if attrs:
                    self._res_data[params] = handler(url, self._data).findall_with_(attrs)
                else:
                    self._res_data[params] = handler(url, self._data).findall()
        if rules:
            if attrs:
                self._res_data['spec'] = tags_router['base'](self._data).findall_with_(attrs)
            else:
                self._res_data['spec'] = tags_router['base'](self._data).findall()

        return self._res_data

if __name__ == '__main__':
    ba = BaseRequest()
    ret = ba.get('https://www.aimeishishang.com/duanqunmeinv/mm3764/', ['a'], ['href'])
    print(ret)
