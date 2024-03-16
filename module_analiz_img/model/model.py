import cv2
import numpy as np
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

        self.name_img = name_img
        self.path_field = path_field
        self.type_image = type_image
        self.result_image = np

    # endregion

    # region method

    def aligned_brightness(self):

        if self.type_image == 'front':
            img_correct_brig = self.result_image
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # по пиксельно повышаем яркость
            img_correct_brig = cv2.filter2D(img_correct_brig, -1, kernel)
            self.result_image = img_correct_brig
            print("Correct bright successful")
        elif self.type_image == 'lateral':
            pass
        else:
            raise ValueError("Sorry incorrect data")

    def noise_correction(self):

        if self.type_image == 'front':
            img_correct = cv2.imread(f'{self.path_field}/{self.name_img}')
            median_image = cv2.medianBlur(img_correct, 9)  # аргумент ksize указывает на размер фильтра
            self.result_image = median_image
            print("Correct noise successful")
        elif self.type_image == 'lateral':
            pass
        else:
            raise ValueError("Sorry incorrect data")

    def contrast_correction(self):

        if self.type_image == 'front':
            img_correct_contrast = self.result_image
            # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=12., tileGridSize=(1, 1))  # level contrast
            lab = cv2.cvtColor(img_correct_contrast, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
            l, a, b = cv2.split(lab)  # split on 3 different channels
            l2 = clahe.apply(l)  # apply CLAHE to the L-channel
            lab = cv2.merge((l2, a, b))  # merge channels
            img_correct_contrast = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR4
            self.result_image = img_correct_contrast
            cv2.imwrite(f'{self.path_field}/result.jpg', img_correct_contrast)
            print("Correct contrast successful")

        elif self.type_image == 'lateral':
            pass
        else:
            raise ValueError("Sorry incorrect data")

    def convert_in_black_white(self):
        if self.type_image == 'front':
            img_black_white = cv2.cvtColor(self.result_image,  cv2.COLOR_BGR2GRAY)
            self.result_image = img_black_white
            print("Convert black white image successful")
        elif self.type_image == 'lateral':
            pass
        else:
            raise ValueError("Sorry incorrect data")

    def check_dent(self):
        if self.type_image == 'front':
            img_check_dent = self.result_image
            for y in range(img_check_dent.shape[0]):
                for x in range(img_check_dent.shape[1]):
                    if img_check_dent[y][x] < 180:
                        img_check_dent[y][x] = 0

            cv2.imwrite(f'{self.path_field}/result.jpg', img_check_dent)
            print('Check dent successful')
        elif self.type_image == 'lateral':
            pass
        else:
            raise ValueError("Sorry incorrect data")

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
