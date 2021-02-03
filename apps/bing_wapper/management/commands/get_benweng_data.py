import os
from lxml import etree

import requests
from django.core.management.base import BaseCommand

requests.packages.urllib3.disable_warnings()  # https add vasify=False


DATA_PATH = r'./data'
IMAGE_PATH = r'./media/bingwapper'
HTML_PATH = './data/html'


class Command(BaseCommand):

    def handle(self, *args, **options):
        main()
        pass


def open_url(url='', params={}):
    headers = {}
    headers = {
        'User-Agent': "Mozilla/5.0 ",
    }
    try:
        ret = requests.get(url, verify=False, headers=headers)
    except Exception:
        print('open url error')
        ret = None
    return ret


def filter_html(html, xrules=[]):
    data = []
    try:
        selectror = etree.HTML(html)
        for each in xrules:
            data.append(selectror.xpath(each))
    except Exception:
        print('find data error')
        data = []

    return data


def download_image(name, full_url):
    if os.path.exists(os.path.join(IMAGE_PATH, name + '.jpg')):
        return

    ret = open_url(full_url)
    ret = ret._content
    pic_path = os.path.join(IMAGE_PATH, name + '.jpg')
    with open(pic_path, 'wb') as f:
        f.write(ret)


def get_html():
    start = 1
    end = 4217
    exists_set = set(os.listdir(HTML_PATH))
    for i in range(start, end):
        url = 'https://www.benweng.com/bing/details/%s.html' % i
        if '%s.html' % i not in exists_set:
            print(url)
            ret = open_url(url)
            if not ret:
                continue
            ret = ret.text
            file_path = os.path.join(HTML_PATH, '%s.html' % i)
            with open(file_path, 'w', encoding='utf8') as f:
                f.write(ret)


def get_data():
    html_files = os.listdir(HTML_PATH)
    for i in html_files:
        with open(os.path.join(HTML_PATH, i), 'r', encoding='utf8') as f:
            content = f.read()
            rules = [
                '/html/body/main/div/div/div[2]/div[1]/div[3]/img/@data-src',
                '/html/body/main/div/div/div[2]/div[1]/div[1]/text()[2]',
                '/html/body/main/div/div/div[2]/div[1]/div[1]/text()[5]',
                '/html/body/main/div/div/div[2]/div[1]/h5[1]/text()',
                '/html/body/main/div/div/div[2]/div[1]/div[2]/p/text()',
                '/html/body/main/div/div/div[2]/div[1]/div[6]/div[2]/div/a[1]/@href',
            ]
            res = filter_html(content, rules)
            try:
                info = {
                    'filename': res[0][0].split('/')[-1].split('.jpg')[0],
                    'date': res[1][0].strip(),
                    'author': res[2][0].strip().split('（图片文字内容来源于必应搜索）')[0] if res[2] else '',
                    'title': res[3][0].strip(),
                    'description': res[4][0].strip(),
                    'url': res[5][0],
                }
                download_image(info['filename'], info['url'])
            except Exception as e:
                print(res)
                print(e)


def main():
    pass
