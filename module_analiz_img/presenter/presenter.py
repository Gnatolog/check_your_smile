from model import model
from viewer import viewer


# TODO Добавить эндпоинт по запуску процесса


class Startprocession:
    """
    Starting the processing process
    """

    # region field

    def __init__(self, name_user: str, id_user: int, task_id: str,):
        self.name_user = name_user
        self.id_user = id_user
        self.task_id = task_id

    # endregion

    # region method

    def start_analiz(self):
        pass

    def get_result(self):
        pass

    # endregion

