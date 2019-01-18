import requests
import time
from random import choice
from bs4 import BeautifulSoup


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
    proxy = {'http': 'http://' + choice(proxies)}
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


def main():
    token = 254002135060
    proxy, useragent = proxy_changer()

    while token < 254002145092:
        url = f'https://fex.net/j_object_view/{token}'
        url_test_ip = 'http://sitespy.ru/my-ip'
        try:
            # Tyr to use proxy ip
            r = requests.get(url, headers=useragent, proxies=proxy)
            respons_data = r.json()

            # Test our ip by parsing http://sitespy.ru/my-ip
            # test_ip_r = requests.get(url_test_ip, headers=useragent, proxies=proxy)
            # respons_data_for_ip = test_ip_r.text
            # get_ip(respons_data_for_ip)

        except requests.exceptions.ConnectionError as e:
            print(e.response)
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

        # time.sleep(random.uniform(0, 1))
        token += 1


if __name__ == '__main__':
    main()
