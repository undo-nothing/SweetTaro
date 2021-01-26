import json
import requests

requests.packages.urllib3.disable_warnings()  # https add vasify=False


base_url = 'http://127.0.0.1:7777'


def insert_data():
    headers = {
        'content-type': 'application/json',
    }

    images = []
    with open('data_list.json', 'r', encoding="utf-8") as f:
        images.extend([json.loads(i) for i in f.readlines()])

    images = images[::-1]
    # images = images[:5]
    for image in images:
        data = {
            'filename': image['filename'],
            'title': image['title'],
            'date': image['date'],
            'location': image['location'],
            'description': image['description'],
            'url': image['url'],
            'keyword': image['keyword'],
            'author': image['author']
        }

        url = base_url + '/v1/bings/'
        ret = requests.post(url=url, data=json.dumps(data), headers=headers)
        print(ret.url, ret.status_code)
        # print(ret.text)


if __name__ == '__main__':
    insert_data()
