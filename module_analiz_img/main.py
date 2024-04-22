import shutil
from presenter import presenter
from fastapi import FastAPI
from pathlib import Path
from starlette.responses import JSONResponse

app = FastAPI()




@app.get('/data_analiz/{name}/{path}/{name_file_lateral}/{name_file_frontal}')
async def module_analiz_start(name: str, path: str,
                              name_file_lateral: str, name_file_frontal: str):
    run_process = presenter.Startprocession(name,
                                            path=path,
                                            name_file_lateral=name_file_lateral,
                                            name_file_frontal=name_file_frontal)
    run_process.start_analiz()

    if run_process.get_result():
        rm_dir = Path.cwd() / 'temp_storage' / 'user_img' / path
        shutil.rmtree(rm_dir)
        return JSONResponse(run_process.get_result())

    return "Произошла ошибка извините"

# def test_module(name: str, path: str,
#                 name_file_lateral: str, name_file_frontal: str):
#     run_process = presenter.Startprocession(name,
#                                             1, 'ffff111',
#                                             path=path,
#                                             name_file_lateral=name_file_lateral,
#                                             name_file_frontal=name_file_frontal)
#     run_process.start_analiz()
#
#     if run_process.get_result():
#         print(Path.cwd() / 'temp_storage' / 'user_img' / path)
#         rm_dir = Path.cwd()/'temp_storage'/'user_img'/path
#         shutil.rmtree(rm_dir)
#         print(run_process.get_result())
#
#     return "Произошла ошибка Извините"

# if __name__ == '__main__':
#     test_module('test',
#                 '2024.03.57',
#                 'test_1_lateral.JPG',
#                 'test-1_front.JPG'
#                 )
