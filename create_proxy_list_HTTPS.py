import requests
from bs4 import BeautifulSoup


def get_html():
    url = 'https://www.sslproxies.org/'
    r = requests.get(url)
    return r.text


def get_proxy(html: str) -> list:
    """
    Func parse html,  filer host:port, and make host:port list
    :param html: 'https://www.ip-adress.com/proxy-list' - parser only for this url
    :return: list or proxy as host:port pare
    """
    proxies = []
    soup = BeautifulSoup(html, 'lxml')
    links = soup.tbody.find_all('tr')
    for link in links:
        host_port = link.find('td').text + ':' + link.find('td').find_next_siblings('td')[0].text
        proxies.append(host_port)
    return proxies


def write_to_file(proxies: list):
    """
    Write input list of proxies into file
    :param proxies: list proxies as host:port pare
    :return:
    """
    with open('proxies.txt', 'w') as file:
        for i in proxies:
            if proxies.index(i) < len(proxies)-1:
                file.write(f'{i}\n')
                # print(i, file=file, sep="\n")
            else:
                # print(i, file=file, sep="")
                file.write(f'{i}')
    print('Write comlete!')


if __name__ == '__main__':
    write_to_file(get_proxy(get_html()))
