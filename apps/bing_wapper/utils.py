import os
import json
import datetime

import requests
from django.conf import settings

from apps.bing_wapper.models import BingWapper


def check_all_data():
    qs = BingWapper.objects.all().values_list('filename', 'date')
    dates = {i[1] for i in qs}
    files = [i[0] for i in qs]
    start_date = datetime.datetime.strptime('2009-07-12', '%Y-%m-%d').date()
    end_date = datetime.datetime.now().date()

    print(len(dates), len(files))

    for i in range((end_date - start_date).days):
        date = start_date + datetime.timedelta(days=i)
        if date not in dates:
            print(date.strftime('%Y-%m-%d'))

    for file in files:
        file_path = os.path.join(settings.MEDIA_ROOT, 'bingwapper', file + '.jpg')
        if not os.path.exists(file_path):
            print(file)


def download_image(filename):
    url = 'https://cn.bing.com/th?id=OHR.%s_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp' % filename
    file_path = os.path.join(settings.MEDIA_ROOT, 'bingwapper', filename + '.jpg')
    if os.path.exists(file_path):
        return
    ret = requests.get(url=url)
    with open(file_path, 'wb') as f:
        f.write(ret.content)


def check_bingwapper_data():
    url = 'https://cn.bing.com/HPImageArchive.aspx'
    params = {
        "format": 'js',
        'idx': '0',
        'n': '8',
        'mkt': 'zh-CN',
    }
    ret = requests.get(url=url, params=params)
    if ret.status_code != 200:
        return

    datas = json.loads(ret.text)['images']
    for data in datas:
        filename = data.get('urlbase', '').split('=')[-1]
        if filename.startswith('OHR.'):
            filename = filename[4:]

        download_image(filename)
        if not BingWapper.objects.filter(filename=filename).exists():
            title, author = data.get('copyright', '(©').split('(©')
            author = author[:-1].strip()
            title = title.strip()
            date = data.get('enddate', '')
            date = '-'.join([date[0:4], date[4:6], date[6:8]])
            info = {
                'filename': filename,
                'title': title,
                'date': date,
                'author': author,
            }
            BingWapper.objects.create(**info)
