from parser import get_list_proxy
from random import choice
import requests
from requests.exceptions import InvalidProxyURL
import multiprocessing
import threading



def frange(start, step):
    i = start
    while i:
        yield i
        i += step


def some_func(url):
    while True:
        useragent = {'User-Agent': choice(useragent_list)}
        proxy = {'https': 'https://' + choice(proxies_list)}

        try:
            r = requests.get(url, headers=useragent, proxies=proxy, timeout=2)
            respons_data = r.json()

            if r.elapsed.total_seconds() > 5.0:
                raise TimeoutError('respose elapsed time is over 5s')

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
            data = list(map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')], respons_data.get('upload_list')))

            return data, proxies_list

        elif respons_data.get('result') == 0 and respons_data.get('captcha') == 1:
            print(token, proxy, respons_data)
            print('FEX.NET - detect us. We need to update proxybase, and continue about some time')

        break


if __name__ == '__main__':
    proxies_list, useragent_list = get_list_proxy()
    for token in frange(200000000000, 1):
        url = f'https://fex.net/j_object_view/{token}'
        p = multiprocessing.Process(target=some_func, args=(url, ))
        p.start()
