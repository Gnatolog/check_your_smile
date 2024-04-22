from celery import shared_task
import requests


@shared_task
def get_module_analiz(name, path,
                      name_file_lateral,
                      name_file_frontal):
    r = requests.get('http://127.0.0.1:8000/data_analiz/' + name + '/' +
                     path + '/' + name_file_lateral + '/' + name_file_frontal)

    if r.status_code == 200:
        return r.json()







