import requests
import os
import time
from random import choice, uniform
from bs4 import BeautifulSoup
from requests.exceptions import InvalidProxyURL


# from create_proxy_list_HTTPS import get_html, get_new_proxy, write_to_file, del_bad_proxy_from_list, proxy_upd, \
#     add_proxy_to_file
# from multiprocessing import Pool


def get_list_proxy():
    """
    Func use data from files and generate random combination of proxy and User-Agent
    :return: random combination proxy and useragent
    """
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


def main(token, proxies_list, useragent_list):
    while token < 254009000000:
        print('token:', token)
        url = f'https://fex.net/j_object_view/{token}'
        useragent = {'User-Agent': choice(useragent_list)}
        proxy = {'https': 'https://' + choice(proxies_list)}

        try:
            r = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            respons_data = r.json()

            if r.elapsed.total_seconds() > 5.0:
                raise TimeoutError('respose elapsed time is over 5s')

            # test_ip_http(proxy, useragent)
            # test_ip_https(proxy, useragent)

        except InvalidProxyURL:
            proxies_list.remove(proxy.get('https').split('//')[1])
            continue
        except requests.exceptions.ConnectionError:
            proxies_list.remove(proxy.get('https').split('//')[1])
            continue
        except TimeoutError:
            proxies_list.remove(proxy.get('https').split('//')[1])
            continue

        if respons_data.get('result') == 1:
            with open('DB.txt', 'a') as f:
                data = list(
                    map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')], respons_data.get('upload_list')))
                for l in data:
                    load_url = f'{token}' + ' ' + f'https://fex.net/load/{token}/{l[1]}' + ' ' + f'{l[0]}' + ' ' + f'{l[2]}\n'
                    f.write(load_url)
        elif respons_data.get('result') == 0 and respons_data.get('captcha') == 1:
            print(token, proxy, respons_data)
            print('FEX.NET - detect us. We need to update proxybase, and continue about some time')
            continue
        token += 1


if __name__ == '__main__':
    proxies_list, useragent_list = get_list_proxy()
    token = get_token()
    try:
        main(token, proxies_list, useragent_list)
    except:
        with open(os.getcwd() + '/fex.net/proxies.txt', 'w') as f:
            for i in proxies_list:
                f.write(f'{i}\n')
