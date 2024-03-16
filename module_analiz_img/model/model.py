import cv2
from pathlib import Path


class Worker:
    """
    Basi class work image

    """

    # region filed

    def __init__(self, name_img: str, path_field: str, type_image: str):
        self.name_img = name_img
        self.path_field: path_field
        self.type_image = type_image

    # endregion


class Loader(Worker):
    """
    Load file from storage
    Save file on server

    """
    pass


class Preprocessing(Worker):
    """

    Preprocessing image for analiz
    Save file on server

    """

    # region field

    def __init__(self, name_img: str, path_field: str, type_image: str):
        super().__init__(name_img, path_field, type_image)

    # endregion

    # region method

    def aligned_brightness(self):
        pass

    def noise_correction(self):
        pass

    def convert_in_black_white(self):
        pass

    # endregion


class Cuter(Worker):
    """
    Cropping the image by the area of interest
    Save image on server

    """

    # region field

    def __init__(self, name_img: str, path_field: str, type_image: str):
        super().__init__(name_img, path_field, type_image)

    # endregion

    # region method


    def front_cut(self):
        pass

    def lateral_cut(self):
        pass

    # endregion


class Analyzer(Worker):
    """

    Analiz image and getting the result

    """

    # region field
    def __init__(self, name_img: str, path_field: str, type_image: str):
        super().__init__(name_img, path_field, type_image)

    # endregion

    # region method
    def front_analyze_vert(self):
        pass

    def front_analyze_hor(self):
        pass

    def lateral_analyze_vert(self):
        pass

    def later_analyze_sag(self):
        pass
    # endregion


class Resulter(Worker):
    """

    Interpretation of the analysis result

    """

    # region field

    def __init__(self, name_img: str, path_field: str, type_image: str):
        super().__init__(name_img, path_field, type_image)

    # endregion

    # region method

    def load_result_data(self):
        pass

    def evaluation_data(self):
        pass

    def save_result(self):
        pass

    def get_path_result(self):
        pass

    # endregion
