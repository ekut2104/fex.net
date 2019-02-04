import requests
import os
import time
from random import choice, uniform
from bs4 import BeautifulSoup
from requests.exceptions import InvalidProxyURL
import concurrent.futures


def get_token():
    with open(os.getcwd() + '/DB.txt', 'r') as f:
        last_line = f.readlines()[-1].split(' ')[0]
        return int(last_line)


def get_ip(html):
    """
    Func for parsing http://sitespy.ru/my-ip.
    We parse our new ip ---> for monitor/control it
    :param html: html data from request http://sitespy.ru/my-ip
    :return: None/ print our new ip and User-Agent
    """
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    useragent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(useragent)


def test_ip_http(proxy, useragent):
    url_test_ip = 'http://sitespy.ru/my-ip'
    # Test our ip by parsing http://sitespy.ru/my-ip via HTTP
    test_ip_r = requests.get(url_test_ip, headers=useragent, proxies=proxy)
    respons_data_for_ip = test_ip_r.text
    get_ip(respons_data_for_ip)


def get_ip_https(html):
    """
    Func for parsing https://yandex.ua/internet/ru.
    We parse our new ip ---> for monitor/control it
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'lxml')
    ip_https = soup.find('div', class_="client__desc").text.strip()
    print('ip_https:', ip_https)


def test_ip_https(proxy, useragent):
    url_test_ip_https = 'https://yandex.ua/internet/ru'
    # Test our ip by parsing https://yandex.ua/internet/ru via HTTPS
    test_ip_https_r = requests.get(url_test_ip_https, headers=useragent, proxies=proxy)
    respons_for_ip_https = test_ip_https_r.text
    get_ip_https(respons_for_ip_https)

