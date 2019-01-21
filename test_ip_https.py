from bs4 import BeautifulSoup
from random import choice
import requests


def proxy_changer():
    """
    Func use data from files and generate random combination of proxy and User-Agent
    :return: random combination proxy and useragent
    """
    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/proxies.txt', 'r') as f:
        proxies = f.read().split('\n')

    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/useragents.txt', 'r') as f:
        useragents = f.read().split('\n')

    useragent = {'User-Agent': choice(useragents)}
    proxy = {'https': 'https://' + choice(proxies)}
    return proxy, useragent


def get_ip_https(html):
    soup = BeautifulSoup(html, 'lxml')
    ip_https = soup.find('div', class_="client__desc").text.strip()
    print('ip_https:', ip_https)


def main():
    proxy, useragent = proxy_changer()
    url_test_ip_https = 'https://yandex.ua/internet/ru'
    try:
        test_ip_https_r = requests.get(url_test_ip_https, proxies=proxy)
    except requests.exceptions.ConnectionError as e:
        print(e.response)

    respons_for_ip_https = test_ip_https_r.text
    get_ip_https(respons_for_ip_https)


if __name__ == '__main__':
    main()
