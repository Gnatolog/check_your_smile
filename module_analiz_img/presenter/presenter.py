from model import model
from viewer import viewer
import json
from pathlib import Path


# TODO Добавить эндпоинт по запуску процесса


class Startprocession:
    """
    Starting the processing process
    """

    # region field

    def __init__(self, name_user: str, id_user: int, task_id: str, ):
        self.name_user = name_user
        self.id_user = id_user
        self.task_id = task_id
        self.result_analiz = {}

    # endregion

    # region method

    def start_analiz(self):
        # Load template
        template = viewer.Vieweresulter().get_result_view()

        # load_file = model.Loader()   # загрузка файла из хранилища

        # Preprocessing
        preprocessing = model.Preprocessing('low_pricus.JPG',
                                            '/home/gnatolog/check_your_smile/'
                                            'module_analiz_img/temp_storage/',
                                            'front')
        preprocessing.noise_correction()
        preprocessing.aligned_brightness()
        preprocessing.contrast_correction()
        preprocessing.convert_in_black_white()
        preprocessing.check_dent()

        cute = model.Cuter('/home/gnatolog/check_your_smile/'
                           'module_analiz_img/temp_storage/')

        cute.front_cut()

        # Analiz

        analiz = model.Analyzer('/home/gnatolog/check_your_smile/'
                                'module_analiz_img/temp_storage/')

        # analiz.front_analyze_hor()
        self.result_analiz['front_vert'] = analiz.front_analyze_vert()

        # Interpretations analiz

        interprit = model.Resulter(name_user=self.name_user, id_user=self.id_user,
                                   results=self.result_analiz, template=template)
        interprit.evaluation_data()

        result_file = Path.cwd() / 'result_diagnostic'/f'result_diagnostic_{self.name_user}.json'
        with open(result_file, 'w', encoding='utf-8') as fr:
            json.dump(interprit.get_result(), fr, indent=2, ensure_ascii=False)


    def get_result(self):
        pass

    # endregion
