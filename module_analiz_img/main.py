from presenter import presenter
from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()


@app.get('/data_analiz/{name}')
async def module_analiz_start(name: str):
    run_process = presenter.Startprocession(name,
                                            1, 'ffff111')
    run_process.start_analiz()

    if run_process.get_result():
        return JSONResponse(run_process.get_result())

    return "Произошла ошибка Извините"

# if __name__ == '__main__':
#     module_analiz_start()
