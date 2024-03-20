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
            img_black_white = cv2.cvtColor(self.result_image, cv2.COLOR_BGR2GRAY)
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


class Cuter:
    """
    Cropping the image by the area of interest
    Save image on server

    """

    # region field
    def __init__(self, path_file):
        self.path_file = path_file

    # endregion

    # region method

    def front_cut(self):
        img = cv2.imread(f'{self.path_file}result.jpg', flags=0)
        img_resize = cv2.resize(img, (800, 600))  # resize
        cropped = img_resize[200:400, 200:650]  # обрезка изображения image[y1:y2, x1:x2]
        cv2.imwrite(f'{self.path_file}/result.jpg', cropped)

    def lateral_cut(self):
        pass

    # endregion


class Analyzer:
    """

    Analiz image and getting the result

    """

    # region field
    def __init__(self, path_file):
        self.path_file = path_file

    # endregion

    # region method
    def front_analyze_vert(self) -> list[bool, int]:

        img = cv2.imread(f'{self.path_file}result.jpg')
        width = img.shape[0]  # 200
        height = img.shape[1]  # 450

        # Определить центральные резцы в,ч
        len_dent = 0
        number_teeth = 0
        max_width_dent_pix = {}

        for x in range(height):
            if img[width // 4][x][2] > 200:
                len_dent += 1
            elif len_dent > 2:
                number_teeth += 1
                max_width_dent_pix[number_teeth] = (len_dent, x)
                len_dent = 0

        # Поиск максимального значения в.ч
        max_len_upper = 0
        max_len_pix_upper = 0
        for key in max_width_dent_pix.keys():
            if max_width_dent_pix[key][0] > max_len_upper:
                max_len_upper = max_width_dent_pix[key][0]
                max_len_pix_upper = max_width_dent_pix[key][1]

        # Определить расположение центра центральных резцов
        # относительно центра центра центральных резцов верхней челюсти
        max_len_pix_lower = 0
        check_central_low = [False]  # список хранит значение находится ли резцы
        # в пределах нормы или нет

        for y in range(max_len_pix_upper - 20, max_len_pix_upper + 21):

            if img[165][y][2] < 200:
                if y == max_len_pix_upper:
                    check_central_low.append(y)
                    check_central_low[0] = True
                    break
                else:
                    check_central_low[0] = True
                    max_len_pix_lower = y

        check_central_low.append(max_len_pix_lower)

        # TODO удалить после отадки
        # print(check_central_low)

        for y in range(width):  # [y][x]
            for x in range(height):  # порводим перпедикуляр по центру верхних зубов
                img[y][max_len_pix_upper] = 0

        for y in range(100, 200):  # [y][x]
            for x in range(height):  # проводим перпедикуляр по центру нижних зубов зубов
                img[y][max_len_pix_lower] = 0

        # TODO удалить после отадки
        # print(f'{max_len_pix_upper= }\n{check_central_low[1]= }')

        # TODO удалить после перееноса в результер

        # cv2.imshow('cropped', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return check_central_low

    def front_analyze_hor(self):

        img = cv2.imread(f'{self.path_file}result.jpg')
        height_dent_1_1 = 0  # длина первого резца вч
        count_pixcel_dent_all = 0  # общая длина зубов
        count_dent = 0
        width = img.shape[0]  # 200
        height = img.shape[1]  # 450
        # print(f'{width= }')
        # print(f'{height= }')

        for i in range(width):
            # print(img[i][185:190][1][1])
            if img[i][185:190][1][1] > 160:
                count_pixcel_dent_all += 1
            if img[i][185:190][1][1] < 200 and (50 < i < 116):
                height_dent_1_1 = i
                img[i][:height] = 0

        height_dent_4_1 = count_pixcel_dent_all - height_dent_1_1
        part_upper_dent = round(height_dent_1_1 / count_pixcel_dent_all, 1)
        part_lowwer_dent = round(height_dent_4_1 / count_pixcel_dent_all, 1)
        print(f'{height_dent_4_1= }')
        print(f'{height_dent_1_1= }')
        print(f'{part_upper_dent= }')
        print(f'{part_lowwer_dent= }')

        result_analiz = part_upper_dent - part_lowwer_dent  # переменная хранить данные анализа

        if result_analiz > 0.2:
            print("У вас глубокий прикус")
        elif 0 < result_analiz <= 0.2:
            print("У вас нормальный прикус")
        elif result_analiz == 0:
            print("У вас прямой прикус")
        elif result_analiz < 0:
            print("У вас открытый прикус")

    def lateral_analyze_vert(self):
        pass

    def later_analyze_sag(self):
        pass
    # endregion


class Resulter:
    """

    Interpretation of the analysis result

    """

    # region field
    def __init__(self, name_user: str, id_user: int, results: dict, template: dict):
        self.name_user = name_user
        self.id_user = id_user
        self.results = results
        self.result_diagnostic = template
        self.eval_data = {}

    # endregion

    # region method
    def evaluation_data(self):
        # fill in the name, id
        self.result_diagnostic.update({'name': self.name_user})
        self.result_diagnostic.update({'id': self.id_user})

        # analiz front vertical
        result_front_vertical = self.results['front_vert']

        if result_front_vertical[0] is True:
            self.eval_data['front_vert'] = True
            self.result_diagnostic['result_front_vertical'] = \
                'У Вас не обнаружено смещение нижней челюсти'
        else:
            self.eval_data['front_vert'] = False
            self.result_diagnostic['result_front_vertical'] = \
                'У Вас обнаружено смещение нижней челюсти'

        print('Diagnostic complete')

    def get_result(self):
        return self.result_diagnostic

    # endregion
