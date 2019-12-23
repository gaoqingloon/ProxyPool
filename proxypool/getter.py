from .utils import get_page
from pyquery import PyQuery as pq
from lxml import etree
import re


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        """
        国内高匿代理: https://www.kuaidaili.com/free/inha/
        :return:
        """
        for page in range(1, 4):

            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            ip_address = re.compile(
                '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
            )
            re_ip_address = ip_address.findall(str(html))
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        """
        西刺代理: http://www.xicidaili.com/wt/
        :return:
        """
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile(
                '<td class="country"><img src="//fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(str(html))
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                html = etree.HTML(html)
                tr_list = html.xpath('//table/tr')
                for i in range(2, len(tr_list)):
                    ip = tr_list[i].xpath('./td[1]/text()')[0]
                    port = tr_list[i].xpath('./td[2]/text()')[0]
                    yield ':'.join([ip, port])

    # def crawl_data5u(self):
    #     for i in ['gngn', 'gnpt']:
    #         start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
    #         html = get_page(start_url)
    #         ip_address = re.compile(
    #             ' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>'
    #         )
    #         # \s * 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(str(html))
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')
    #
    # def crawl_kxdaili(self):
    #     for i in range(1, 4):
    #         start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
    #         html = get_page(start_url)
    #         ip_address = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
    #         # \s* 匹配空格，起到换行作用
    #         re_ip_address = ip_address.findall(str(html))
    #         for address, port in re_ip_address:
    #             result = address + ':' + port
    #             yield result.replace(' ', '')
    #
    # def crawl_premproxy(self):
    #     for i in ['China-01', 'China-02', 'China-03', 'China-04', 'Taiwan-01']:
    #         start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(
    #             i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address = re.compile('<td data-label="IP:port ">(.*?)</td>')
    #             re_ip_address = ip_address.findall(str(html))
    #             for address_port in re_ip_address:
    #                 yield address_port.replace(' ', '')
    #
    # def crawl_xroxy(self):
    #     for i in ['CN', 'TW']:
    #         start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             ip_address1 = re.compile("title='View this Proxy details'>\s*(.*).*")
    #             re_ip_address1 = ip_address1.findall(str(html))
    #             ip_address2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
    #             re_ip_address2 = ip_address2.findall(html)
    #             for address, port in zip(re_ip_address1, re_ip_address2):
    #                 address_port = address + ':' + port
    #                 yield address_port.replace(' ', '')

