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

    def __init__(self, name_user: str, id_user: int, task_id: str):
        self.name_user = name_user
        self.id_user = id_user
        self.task_id = task_id
        self.result_analiz = {}

    # endregion

    # region method

    def start_analiz(self):
        # region Load template

        template = viewer.Vieweresulter().get_result_view()

        # endregion

        # region loadfile storage

        # load_file = model.Loader()   # загрузка файла из хранилища

        # endregion

        # region Preprocessing

        # preprocessing = model.Preprocessing('Beloshin_front.JPG',
        #                                     'Beloshin_lateral.JPG',
        #                                     '/home/gnatolog/check_your_smile/'
        #                                     'module_analiz_img/temp_storage/',)
        # preprocessing.noise_correction()
        # preprocessing.aligned_brightness()
        # preprocessing.contrast_correction()
        # preprocessing.convert_in_black_white()
        # preprocessing.check_dent()

        # endregion

        # region Cut image

        # cute = model.Cuter('/home/gnatolog/check_your_smile/'
        #                    'module_analiz_img/temp_storage/')
        #
        # cute.cut_image()

        # endregion

        # region Analiz

        analiz = model.Analyzer('/home/gnatolog/check_your_smile/'
                                'module_analiz_img/temp_storage/')

        self.result_analiz['front_vert'] = analiz.front_analyze_vert()
        self.result_analiz['front_hor'] = analiz.front_analyze_hor()
        self.result_analiz['lateral_vert'] = analiz.lateral_analyze_vert()
        self.result_analiz['lateral_sag'] = analiz.later_analyze_sag()

        # endregion

        # region Interpretations analiz

        interprit = model.Resulter(name_user=self.name_user, id_user=self.id_user,
                                   results=self.result_analiz, template=template)
        interprit.evaluation_data()

        # endregion

        # region Save result

        result_file = Path.cwd() / 'result_diagnostic'/f'result_diagnostic_{self.name_user}.json'
        with open(result_file, 'w', encoding='utf-8') as fr:
            json.dump(interprit.get_result(), fr, indent=2, ensure_ascii=False)

        # endregion


    def get_result(self):
        pass

    # endregion
