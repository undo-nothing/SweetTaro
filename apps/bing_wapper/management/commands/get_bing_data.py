import os
import csv

from lxml import etree
import requests
from django.core.management.base import BaseCommand

requests.packages.urllib3.disable_warnings()  # https add vasify=False


DATA_PATH = r'./data'
IMAGE_PATH = r'./media/bingwapper'


class Command(BaseCommand):

    def handle(self, *args, **options):
        main()
        pass


def main():
    get_bing_pic()


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
    # print(ret.url, ret.status_code)
    return ret


def filter_html(url='', Xrule=[]):  # provede url and Xrule to filter html
    data = []
    html = open_url(url).text
    try:
        selectror = etree.HTML(html)
        for each in Xrule:
            data.append(selectror.xpath(each))
    except Exception:
        print('find data error')
        data = []

    return data


def trval_page(start=1, end=1):
    urls = []
    for i in range(start, end + 1):
        url = 'https://bing.ioliu.cn/?p=%d' % i
        Xrule = [r'/html/body/div[3]/div/div/a/@href']
        datas = filter_html(url, Xrule)
        urls.extend(datas[0] if datas else [])

    return urls


def download_pic(url, base_dir=''):
    full_url = 'https://bing.ioliu.cn' + url
    ret = open_url(full_url)
    ret = ret._content
    name = url.split('/')[-1].split('?')[0]
    pic_path = os.path.join(base_dir, name + '.jpg')
    with open(pic_path, 'wb') as f:
        f.write(ret)


def get_detail_data(urls):
    data_list = []
    Xrule = (r'/html/body/div[1]/div[4]/p[1]/text()',
             # date
             r'/html/body/div[1]/div[4]/p[3]/em/text()',
             # location
             r'/html/body/div[1]/div[4]/p[4]/em/text()',
             # filename
             r'/html/body/div[1]/div[3]/a[3]/@href',
             r'//meta[@name="keywords"]/@content',
             r'//meta[@name="description"]/@content',
             r'//meta[@name="author"]/@content',
             )
    for each in urls:
        url = 'https://bing.ioliu.cn/' + each
        data = filter_html(url, Xrule)
        print(data[3][0])
        data_dict = dict(filename=data[3][0].split('/')[-1].split('?')[0],
                         title=data[0][0],
                         date=data[1][0],
                         location='' if data[2][0].isdigit() else data[2][0],
                         description='' if data[5][0] == 'null' else data[5][0],
                         url=data[3][0],
                         keyword=data[4][0],
                         author=data[6][-1],
                         )
        data_list.append(data_dict)

    return data_list


def get_urls(start=1, end=1):
    page_size = 12
    start_page = start // page_size + 1
    end_page = end // page_size + 1
    urls = trval_page(start_page, end_page)

    start = start - ((start_page - 1) * page_size)
    end = end - ((start_page - 1) * page_size)
    return urls[start - 1:end]


def save_csv_file(datas, file_name):
    with open(file_name, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f, dialect='excel')
        headers = datas[0].keys() if len(datas) else []
        writer.writerow(headers)
        for data in datas:
            writer.writerow([data.get(key, '') for key in headers])


def get_bing_pic(start=1, end=1):
    urls = get_urls(start, end)
    detail_list = get_detail_data(urls)
    save_csv_file(datas=detail_list, file_name='data_list.csv')
