
import re
import sys
import time
import datetime
import threading
import random
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


def send_request(url="", proxies=None):
    user_agent_list = [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
        "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "",
               "User-Agent": random.choice(user_agent_list),
               }
    get_result = requests.get(url, headers=headers, proxies=proxies)
    print(get_result.text)


# send_request("https://www.baidu.com", proxies={"http": "45.221.79.134:53281"})

for ip in get_proxy_ips():
    str_ip=ip[0]+":"+ip[1]
    print(str_ip)
    send_request("https://www.baidu.com", proxies={"http": str_ip})
