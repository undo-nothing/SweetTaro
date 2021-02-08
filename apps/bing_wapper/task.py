from celery import shared_task

from .utils import check_bingwapper_data


@shared_task
def check_bingwapper_data_task():
    check_bingwapper_data()
