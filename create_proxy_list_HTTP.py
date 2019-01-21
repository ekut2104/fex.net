import requests
from bs4 import BeautifulSoup


def get_html():
    url = 'https://www.ip-adress.com/proxy-list'
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
        proxies.append(link.get_text().split('\n')[1])

    return proxies


def write_to_file(proxies: list):
    """
    Write input list of proxies into file
    :param proxies: list proxies as host:port pare
    :return:
    """
    count = 1
    with open('proxies.txt', 'w') as file:
        for i in proxies:
                print(i, file=file, sep="\n")
    return 'Write comlete!'


if __name__ == '__main__':
    write_to_file(get_proxy(get_html()))
