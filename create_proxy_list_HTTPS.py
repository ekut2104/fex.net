import requests
import os
from bs4 import BeautifulSoup


def get_html():
    url = 'https://www.sslproxies.org/'
    r = requests.get(url)
    return r.text


def get_new_proxy(html: str) -> list:
    """
    Func parse html,  filer host:port, and make host:port list
    :param html: 'https://www.sslproxies.org/' - parser only for this url
    :return: list or proxy as host:port pare
    """
    proxies = []
    try:
        with open(os.getcwd() + '/proxies.txt', 'r') as file:
            proxies_in_file = file.read()
    except FileNotFoundError as e:
        print(e)
        proxies_in_file = []

    soup = BeautifulSoup(html, 'lxml')
    links = soup.tbody.find_all('tr')
    for link in links:
        host_port = link.find('td').text + ':' + link.find('td').find_next_siblings('td')[0].text
        if host_port not in proxies_in_file:
            print('Added new proxy:', host_port)
            proxies.append(host_port)

    return proxies


# def del_bad_proxy_from_list(proxy: str):
#     """
#     Func del input proxy from a list of proxies from file
#     :param proxy: str - input data
#     :return: None
#     """
#     try:
#         with open(os.getcwd() + '/proxies.txt', 'r') as file:
#             proxies_in_file = file.read().split('\n')
#             if proxy in proxies_in_file:
#                 proxies_in_file.remove(proxy)
#                 write_to_file(proxies_in_file)
#                 print('Bad proxy delete from proxy list')
#
#             else:
#                 proxies_in_file.remove('')
#                 add_proxy_to_file(get_new_proxy(get_html()))
#
#     except FileNotFoundError as e:
#         print(e, 'Maybe, proxies.txt doesnot created yet')


# def proxy_upd():
#     add_proxy_to_file(get_new_proxy(get_html()))


# def write_to_file(proxies: list):
#     """
#     Write input list of proxies into file
#     :param proxies: list proxies as host:port pare
#     :return:
#     """
#     with open(os.getcwd() + '/proxies.txt', 'w') as file:
#         for i in proxies:
#             file.write(f'{i}\n')
#
#     print('Write comlete!')


def add_proxy_to_file(proxies: list):
    with open(os.getcwd() + '/proxies.txt', 'a') as file:
        for i in proxies:
            file.write(f'{i}\n')

    print('Adding comlete!')


if __name__ == '__main__':
    add_proxy_to_file(get_new_proxy(get_html()))


