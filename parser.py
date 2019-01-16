import requests
import threading


def get_html(url):
    r = requests.get(url)
    if r.json()['result'] == 1:
        # pprint.pprint(r.json())
        upload_id = r.json()['upload_list'][0]['upload_id']
        name = r.json()['upload_list'][0]['name']
        size = r.json()['folder_upload_size']
        print(name, upload_id, size, f'https://fex.net/load/254002135070/{upload_id}')
        return name, upload_id, size, f'https://fex.net/load/254002135070/{upload_id}'


if __name__ == '__main__':
    token = 200000002030
    while token < 30000000000:
        print(token)
        url = f'https://fex.net/j_object_view/{token}'
        our_thread = threading.Thread(target=get_html(url))
        token += 1
        our_thread.start()
