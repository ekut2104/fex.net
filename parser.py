import requests
import os
import time
from random import choice, uniform
from bs4 import BeautifulSoup
from requests.exceptions import InvalidProxyURL
import concurrent.futures




def get_list_proxy():
    """
    Func use data from files and generate random combination of proxy and User-Agent
    :return: random combination proxy and useragent
    """
    print(os.getcwd())
    with open(os.getcwd() + '/fex.net/proxies.txt', 'r') as f:
        proxies = f.read().split('\n')
        try:
            proxies.remove('')
        except ValueError:
            pass

    with open(os.getcwd() + '/fex.net/useragents.txt', 'r') as f:
        useragents = f.read().split('\n')

    return proxies, useragents


def get_token():
    with open(os.getcwd() + '/fex.net/DB.txt', 'r') as f:
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


def some_func(url):
    while True:
        useragent = {'User-Agent': choice(USERAGENT_LIST)}
        proxy = {'https': 'https://' + choice(PROXY_LIST)}
        try:
            r = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            respons_data = r.json()

            if r.elapsed.total_seconds() > 5.0:
                raise TimeoutError('respose elapsed time is over 5s')

        except InvalidProxyURL:
            try:
                PROXY_LIST.remove(proxy.get('https').split('//')[1])
            except ValueError:
                pass
            continue

        except ConnectionError:
            try:
                PROXY_LIST.remove(proxy.get('https').split('//')[1])
            except ValueError:
                pass
            continue

        except TimeoutError:
            try:
                PROXY_LIST.remove(proxy.get('https').split('//')[1])
            except ValueError:
                pass
            continue

        if respons_data.get('result') == 1:
            with open('DB.txt', 'a+') as f:
                f.write(f'{url}\n')
            time.sleep(1)
            break

        elif respons_data.get('result') == 0 and respons_data.get('captcha') == 1:
            print(url, proxy, respons_data)
            print('FEX.NET - detect us. We need to update proxybase, and continue about some time')

        # print(url)
        break


def main():
    workers = 150
    token = 254002136116
    while True:
        urls = []
        for _ in range(workers):
            url = f'https://fex.net/j_object_view/{token}'
            token += 1
            urls.append(url)
        with concurrent.futures.ThreadPoolExecutor(workers) as executor:
            for _ in executor.map(some_func, urls):
                pass


if __name__ == '__main__':
    start_token = 254009000039
    PROXY_LIST, USERAGENT_LIST = get_list_proxy()
    main()
