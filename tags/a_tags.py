from tags.base import LOG
from tags.base import Tags, BaseAttribute


class ATags(Tags):

    RULE = r'<a.+?>.+?</a>'

    def findall_with_(self, attrs=[]):
        LOG.info('开始获取标签及属性：%s' % attrs)
        data = self._get()
        href_attr = BaseAttribute(self.url, data, attrs)
        res_list = href_attr.get_attr()
        return res_list