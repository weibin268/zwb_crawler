
import re
import random
import sys
import time
import datetime
import threading
from random import choice
import requests
import bs4


def get_proxy_ips(page_no=1, type="all"):
    result = list([])
    url = "http://www.xicidaili.com/nn/"+str(page_no)
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "http://www.xicidaili.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
               }

    get_result = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(get_result.text, 'html.parser')
    tr_data = list(soup.table.find_all("tr"))
    del tr_data[0]

    if(type != "all"):
        def type_filter(tr):
            if r"<td>" + type.upper()+r"</td>" in str(tr):
                return True
            else:
                return False
        tr_data = list(filter(type_filter, tr_data))

    re_ip = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  # 匹配IP
    re_port = re.compile(r'<td>(\d+)</td>')  # 匹配端口

    for tr in tr_data:
        ip = re.findall(re_ip, str(tr))
        port = re.findall(re_port, str(tr))
        result.append((ip[0], port[0]))

    return result


# get_proxy_ips(2)
ips = get_proxy_ips(type="http")

for ip in ips:
    print(ip[0]+":"+ip[1])

print(len(ips))
