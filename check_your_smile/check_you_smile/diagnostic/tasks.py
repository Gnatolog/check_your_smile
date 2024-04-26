from celery import shared_task
import requests


@shared_task
def get_module_analiz(name, path,
                      name_file_lateral,
                      name_file_frontal):
    # host 127.0.0.1 not docker compose or module_image:8001 with docker compose
    r = requests.get('http://module_image:8001/data_analiz/' + name + '/' + path + '/' + name_file_lateral + '/' + name_file_frontal)

    if r.status_code == 200:
        return r.json()







