import os
import csv

from django.core.management.base import BaseCommand

from apps.bing_wapper.models import BingWapper


DATA_PATH = r'./data'


class Command(BaseCommand):

    def handle(self, *args, **options):
        main()
        pass


def main():
    insert_data()
    pass


def get_data_list():
    data_list = []
    video_list_file = os.path.join(DATA_PATH, 'bingwapper_list.csv')
    with open(video_list_file, 'r', encoding='utf8') as f:
        data_list = list(csv.DictReader(f))

    return data_list


def insert_data():
    filename_set = {i[0] for i in BingWapper.objects.values_list('filename')}

    wapper_list = []
    datas = get_data_list()
    for data in datas:
        if data['filename'] in filename_set:
            continue
        info = {
            'filename': data['filename'],
            'title': data['title'],
            'date': data['date'],
            'location': data['location'],
            'description': data['description'],
            'url': data['url'],
            'keyword': data['keyword'],
            'author': data['author']
        }
        wapper_list.append(BingWapper(**info))

    BingWapper.objects.bulk_create(wapper_list)
