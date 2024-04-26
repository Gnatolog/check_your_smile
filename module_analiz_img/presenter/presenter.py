from model import model
from viewer import viewer


class Startprocession:
    """
    Starting the process
    """

    # region field

    def __init__(self, name_user: str,
                 path: str, name_file_frontal: str, name_file_lateral):
        self.name_user = name_user
        self.path = path
        self.name_file_frontal = name_file_frontal
        self.name_file_lateral = name_file_lateral
        self.result_analiz = {}
        self.evaluation_result = {}

    # endregion

    # region method

    def start_analiz(self):
        # region Load template

        template = viewer.Vieweresulter().get_result_view()

        # endregion

        # region Preprocessing
        preprocessing = model.Preprocessing(self.name_file_frontal,
                                            self.name_file_lateral,
                                            path_field_front=f'temp_storage/user_img/{self.path}/frontal/',
                                            path_field_lateral=f'temp_storage/user_img/{self.path}/lateral/'
                                            )
        preprocessing.noise_correction()
        preprocessing.aligned_brightness()
        preprocessing.contrast_correction()
        preprocessing.convert_in_black_white()
        preprocessing.check_dent()

        # endregion

        # region Cut image

        cute = model.Cuter(path_file_front=f'temp_storage/user_img/{self.path}/frontal/',
                           path_file_lateral=f'temp_storage/user_img/{self.path}/lateral/')

        cute.cut_image()

        # endregion

        # region Analiz

        analiz = model.Analyzer(path_file_lateral=f'temp_storage/user_img/{self.path}/lateral/',
                                path_file_front=f'temp_storage/user_img/{self.path}/frontal/')

        self.result_analiz['front_vert'] = analiz.front_analyze_vert()
        self.result_analiz['front_hor'] = analiz.front_analyze_hor()
        self.result_analiz['lateral_vert'] = analiz.lateral_analyze_vert()
        self.result_analiz['lateral_sag'] = analiz.later_analyze_sag()

        # endregion

        # region Interpretations analiz

        interprit = model.Resulter(name_user=self.name_user,
                                   results=self.result_analiz, template=template)
        interprit.evaluation_data()

        # endregion

        self.evaluation_result = interprit.get_result()

    def get_result(self):
        return self.evaluation_result

    # endregion
