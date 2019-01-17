import requests
import time
from random import choice
from bs4 import BeautifulSoup
from pprint import pprint


def get_html(url, useragent, proxy):
    r = requests.get(url, headers=useragent, proxies=proxy)
    return r.json()


def proxy_changer():
    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/proxies.txt', 'r') as f:
        proxies = f.read().split('\n')

    proxy = {'http': 'http://' + choice(proxies)}
    # print(proxy, useragent)
    return proxy


def user_agent_changer():
    with open('/mnt/48D443B7D443A5D2/Users/Melnyk.D/OneDrive/MyProjects/Parser/fex.net/useragents.txt', 'r') as f:
        useragents = f.read().split('\n')

    useragent = {'User-Agent': choice(useragents)}
    return useragent


def generate_url_sleep():
    token = 254002135060

    while token < 254002145092:
        url = f'https://fex.net/j_object_view/{token}'
        try:
            useragent = user_agent_changer()
            proxy = proxy_changer()
            respons_data = get_html(url, useragent, proxy)
        except requests.exceptions.ConnectionError as e:
            print(e.response)
            proxy_changer()
            continue

        if respons_data.get('result') == 1:
            print(token, proxy,
                  list(map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')],
                           respons_data.get('upload_list'))))
        elif respons_data.get('result') == 0 and respons_data.get('captcha') == 1:
            print(token, proxy, respons_data)
            useragent = user_agent_changer()
            proxy = proxy_changer()
            continue
        elif respons_data.get('result') == 0:
            print(token, proxy, respons_data)

        # time.sleep(random.uniform(0, 1))
        token += 1


def get_ip(html):
    soup = BeautifulSoup(html, 'lxml')
    ip = soup.find('span', class_='ip').text.strip()
    useragent = soup.find('span', class_='ip').find_next_sibling('span').text.strip()
    print(ip)
    print(useragent)


if __name__ == '__main__':
    generate_url_sleep()
