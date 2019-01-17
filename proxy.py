import requests
from bs4 import BeautifulSoup
from random import choice, uniform


def get_html(url, useragent=None, proxy=None):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.text


def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    useragent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(useragent)


def main():
    url = 'http://sitespy.ru/my-ip'
    with open('useragents.txt', 'r') as ua_file:
        useragents = ua_file.read().split('\n')

    with open('proxies.txt', 'r') as proxy_file:
        proxies = proxy_file.read()

    for i in range(10):

        proxy = {'http': 'http://' + choice(proxies)}
        useragent = {'User-Agent': choice(useragents)}
        try:
            html = get_html(url, useragent, proxy)
        except:
            continue

    get_ip(html)


if __name__ == '__main__':
    main()


    # def get_proxy(self):
    #     for proxy in self.proxi_list:
    #         url = 'http://' + proxy
    #         try:
    #             r = requests.get('http://google.com', proxies={'http': url})
    #             if r.status_code == 200:
    #                 return url
    #         except requests.exceptions.ConnectionError:
    #             continue
