import requests
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
        with open('proxies.txt', 'r') as file:
            proxies_in_file = file.read()
    except FileNotFoundError:
        proxies_in_file = []

    soup = BeautifulSoup(html, 'lxml')
    links = soup.tbody.find_all('tr')
    for link in links:
        host_port = link.find('td').text + ':' + link.find('td').find_next_siblings('td')[0].text
        if host_port not in proxies_in_file:
            print('Added new proxy:', host_port)
            proxies.append(host_port)

    return proxies


def del_bad_proxy_from_list(proxy: str) -> list:
    """
    Func del input proxy from a list of proxies from file
    :param proxy: str - input data
    :return: error or list of proxies
    """
    try:
        with open('proxies.txt', 'r') as file:
            proxies_in_file = file.read().split('\n')
            if proxy in proxies_in_file:
                proxies_in_file.remove(proxy)

                return proxies_in_file
            else:
                proxies_in_file.remove('')
                if len(proxies_in_file) == 0:
                    proxy_upd()

    except FileNotFoundError as e:
        print(e, 'Maybe, proxies.txt doesnot created yet')
        proxies_in_file = []

        return proxies_in_file


def proxy_upd():
    write_to_file(get_new_proxy(get_html()))


def write_to_file(proxies: list):
    """
    Write input list of proxies into file
    :param proxies: list proxies as host:port pare
    :return:
    """
    with open('proxies.txt', 'a') as file:
        for i in proxies:
            file.write(f'{i}\n')

    print('Write comlete!')


if __name__ == '__main__':
    proxy_upd()
