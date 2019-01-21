import requests
import time
from random import choice, uniform
from bs4 import BeautifulSoup
from .create_proxy_list_HTTPS import get_html, get_new_proxy, write_to_file, del_bad_proxy_from_list, proxy_upd
from multiprocessing import Pool


def proxy_changer():
    """
    Func use data from files and generate random combination of proxy and User-Agent
    :return: random combination proxy and useragent
    """
    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/proxies.txt', 'r') as f:
        proxies = f.read().split('\n')
        proxies.remove('')

    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/useragents.txt', 'r') as f:
        useragents = f.read().split('\n')

    useragent = {'User-Agent': choice(useragents)}
    proxy = {'https': 'https://' + choice(proxies)}
    return proxy, useragent


def get_ip(html):
    """
    Func for parsing http://sitespy.ru/my-ip.
    We parse our new ip ---> for monitor/control it
    :param html: html data from request http://sitespy.ru/my-ip
    :return: None/ print uor new ip and User-Agent
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


def main():
    token = 254002135060
    proxy, useragent = proxy_changer()

    while token < 254002135100:
        url = f'https://fex.net/j_object_view/{token}'
        try:
            # Try to use proxy ip
            r = requests.get(url, headers=useragent, proxies=proxy)
            respons_data = r.json()

            # test_ip_http(proxy, useragent)
            # test_ip_https(proxy, useragent)

        except requests.exceptions.ConnectionError as e:
            print(e.response)
            del_bad_proxy_from_list(proxy.get('https').split('//')[1])
            proxy, useragent = proxy_changer()
            continue

        if respons_data.get('result') == 1:
            print(token, proxy,
                  list(map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')],
                           respons_data.get('upload_list'))))
        elif respons_data.get('result') == 0 and respons_data.get('captcha') == 1:
            print(token, proxy, respons_data)
            proxy, useragent = proxy_changer()
            continue
        elif respons_data.get('result') == 0:
            print(token, proxy, respons_data)

        time.sleep(uniform(0, 0.5))
        token += 1


if __name__ == '__main__':
    main()
