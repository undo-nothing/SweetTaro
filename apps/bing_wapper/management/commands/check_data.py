from django.core.management.base import BaseCommand


DATA_PATH = r'./data'


class Command(BaseCommand):

    def handle(self, *args, **options):
        main()
        pass


def main():
    from apps.bing_wapper.utils import check_bingwapper_data, check_all_data
    check_bingwapper_data()
    check_all_data()
