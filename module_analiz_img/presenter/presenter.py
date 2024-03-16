from model import model
from viewer import viewer


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

    # endregion

    # region method

    def start_analiz(self):

        # load_file = model.Loader()   # загрузка файла из хранилища

        preprocessing = model.Preprocessing('right_side.JPG',
                                            '/home/gnatolog/check_your_smile/'
                                            'module_analiz_img/temp_storage/',
                                            'front')
        preprocessing.noise_correction()
        preprocessing.aligned_brightness()
        preprocessing.contrast_correction()
        preprocessing.convert_in_black_white()
        preprocessing.check_dent()

    def get_result(self):
        pass

    # endregion


