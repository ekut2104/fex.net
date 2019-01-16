import requests
import threading
import pprint


def get_html(url):
    r = requests.get(url)
    if r.json()['result'] == 1:
        print(list(map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')], r.json()['upload_list'])))
        return list(map(lambda x: [x.get('name'), x.get('upload_id'), x.get('size')], r.json()['upload_list']))


if __name__ == '__main__':
    token = 254002135060
    while token < 254002135092:
        print(token)
        url = f'https://fex.net/j_object_view/{token}'
        get_html(url)
        token += 1
