import cv2
import numpy as np
from app.utils import start_tread


class Worker:
    """
    Basi class work image

    """

    # region filed

    def __init__(self, name_img_front: str, name_img_lateral,
                 path_field_front: str, path_field_lateral: str):
        self.name_img_front = name_img_front
        self.name_img_lateral = name_img_lateral
        self.path_field_front: path_field_front
        self.path_field_lateral = path_field_lateral

    # endregion


class Preprocessing(Worker):
    """
    Preprocessing image for analiz

    """

    # region field

    def __init__(self, name_img_front: str, name_img_lateral: str,
                 path_field_front: str, path_field_lateral: str):
        super().__init__(name_img_front, name_img_lateral, path_field_front,
                         path_field_lateral)
        self.name_img_front = name_img_front
        self.name_img_lateral = name_img_lateral
        self.path_field_front = path_field_front
        self.path_field_lateral = path_field_lateral
        self.result_image_front = np
        self.result_image_lateral = np

    # endregion

    # region method

    def aligned_brightness(self):

        def brightness_frontal():

            if self.name_img_front:
                img_correct_brig = self.result_image_front
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # по пиксельно повышаем яркость
                img_correct_brig = cv2.filter2D(img_correct_brig, -1, kernel)
                self.result_image_front = img_correct_brig
                print("Correct bright successful")

        def brightness_lateral():

            if self.name_img_lateral:
                img_correct_brig = self.result_image_lateral
                if img_correct_brig[0][0][1] < 100:
                    kernel = np.array([[-1, -1, -1], [-1, 11, -1], [-1, -1, -1]])  # по пиксельно повышаем яркость
                    img_correct_brig = cv2.filter2D(img_correct_brig, -1, kernel)
                else:
                    kernel = np.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])  # по пиксельно повышаем яркость
                    img_correct_brig = cv2.filter2D(img_correct_brig, -1, kernel)
                self.result_image_lateral = img_correct_brig
                print("Correct bright successful")
            else:
                raise ValueError("Sorry incorrect data")

        start_tread(brightness_frontal, brightness_lateral)

    def noise_correction(self):
        print(f'{self.name_img_front= }')
        print(f'{self.name_img_lateral= }')

        def noise_front():

            if self.name_img_front:
                print(f'{self.path_field_front}{self.name_img_front}')
                img_correct = cv2.imread(f'{self.path_field_front}/{self.name_img_front}')
                median_image = cv2.medianBlur(img_correct, 9)  # аргумент ksize указывает на размер фильтра
                self.result_image_front = median_image
                print("Correct noise successful")

        def noise_lateral():
            if self.name_img_lateral:
                img_correct = cv2.imread(f'{self.path_field_lateral}/{self.name_img_lateral}')
                median_image = cv2.medianBlur(img_correct, 3)  # аргумент ksize указывает на размер фильтра
                self.result_image_lateral = median_image
                print("Correct noise successful")

            else:
                raise ValueError("Sorry incorrect data")

        start_tread(noise_front, noise_lateral)

    def contrast_correction(self):

        if self.name_img_front:
            img_correct_contrast = self.result_image_front
            # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=12., tileGridSize=(1, 1))  # level contrast
            lab = cv2.cvtColor(img_correct_contrast, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
            l, a, b = cv2.split(lab)  # split on 3 different channels
            l2 = clahe.apply(l)  # apply CLAHE to the L-channel
            lab = cv2.merge((l2, a, b))  # merge channels
            img_correct_contrast = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR4
            self.result_image_front = img_correct_contrast
            cv2.imwrite(f'{self.path_field_front}/result_front.jpg', img_correct_contrast)
            print("Correct contrast successful")

        elif self.name_img_lateral:
            pass
        else:
            raise ValueError("Sorry incorrect data")

    def convert_in_black_white(self):

        if self.name_img_front:
            img_black_white = cv2.cvtColor(self.result_image_front, cv2.COLOR_BGR2GRAY)
            self.result_image_front = img_black_white
            print("Convert black white image successful")

        if self.name_img_lateral:
            img_black_white = cv2.cvtColor(self.result_image_lateral, cv2.COLOR_BGR2GRAY)
            self.result_image_lateral = img_black_white
            print("Convert black white image successful")

        else:
            raise ValueError("Sorry incorrect data")

    def check_dent(self):

        def check_dent_frontal():

            if self.name_img_front:
                img_check_dent = self.result_image_front
                for y in range(img_check_dent.shape[0]):
                    for x in range(img_check_dent.shape[1]):
                        if img_check_dent[y][x] < 180:
                            img_check_dent[y][x] = 0

                cv2.imwrite(f'{self.path_field_front}/result_front.jpg', img_check_dent)
                print('Check dent successful frontal')

        def check_dent_lateral():
            if self.name_img_lateral:
                img_check_dent = self.result_image_lateral
                for y in range(img_check_dent.shape[0]):
                    for x in range(img_check_dent.shape[1]):
                        if img_check_dent[y][x] < 180:
                            img_check_dent[y][x] = 0

                cv2.imwrite(f'{self.path_field_lateral}/result_lateral.jpg', img_check_dent)
                print('Check dent successful lateral')
            else:
                raise ValueError("Sorry incorrect data")

        start_tread(check_dent_frontal, check_dent_lateral)

    # endregion


class Cuter:
    """
    Cropping the image by the area of interest
    Save image on server

    """

    # region field
    def __init__(self, path_file_front: str, path_file_lateral: str):
        self.path_file_front = path_file_front
        self.path_file_lateral = path_file_lateral

    # endregion

    # region method

    def cut_image(self):
        # Cut front
        def cute_frontal():
            img = cv2.imread(f'{self.path_file_front}result_front.jpg', flags=0)
            img_resize = cv2.resize(img, (800, 600))  # resize
            cropped = img_resize[200:400, 200:650]  # обрезка изображения image[y1:y2, x1:x2]
            cv2.imwrite(f'{self.path_file_front}/result_front.jpg', cropped)

        # Cut lateral
        def cute_lateral():
            img = cv2.imread(f'{self.path_file_lateral}result_lateral.jpg', flags=0)
            img_resize = cv2.resize(img, (800, 600))  # resize
            cropped = img_resize[200:420, 130:450]  # обрезка изображения image[y1:y2, x1:x2]
            cv2.imwrite(f'{self.path_file_lateral}/result_lateral.jpg', cropped)

        start_tread(cute_frontal, cute_lateral)

    # endregion


class Analyzer:
    """

    Analiz image and getting the result

    """

    # region field
    def __init__(self, path_file_front: str, path_file_lateral: str, ):
        self.path_file_front = path_file_front
        self.path_file_lateral = path_file_lateral
        self.max_len_pix_upper = 0

    # endregion

    # region method
    def front_analyze_vert(self) -> list:

        img = cv2.imread(f'{self.path_file_front}result_front.jpg')
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
        self.max_len_pix_upper = 0
        for key in max_width_dent_pix.keys():
            if max_width_dent_pix[key][0] > max_len_upper:
                max_len_upper = max_width_dent_pix[key][0]
                self.max_len_pix_upper = max_width_dent_pix[key][1]

        # Определить расположение центра центральных резцов нижней челюсти
        # относительно центра центра центральных резцов верхней челюсти
        max_len_pix_lower = 0
        check_central_low = [False]  # список хранит значение находится ли резцы
        # в пределах нормы или нет

        for y in range(self.max_len_pix_upper - 20, self.max_len_pix_upper + 21):

            if img[165][y][2] < 200:
                if y == self.max_len_pix_upper:
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
                img[y][self.max_len_pix_upper] = 0

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

        img = cv2.imread(f'{self.path_file_front}result_front.jpg')
        height_dent_1_1 = 0  # длина первого резца вч
        count_pixcel_dent_all = 0  # общая длина зубов
        count_dent = 0
        width = img.shape[0]  # 200
        height = img.shape[1]  # 450
        # print(f'{width= }')
        # print(f'{height= }')

        for i in range(width):
            if img[i][self.max_len_pix_upper][2] > 200:
                img[i][self.max_len_pix_upper - 40][2] = 255
                count_pixcel_dent_all += 1
            elif img[i][self.max_len_pix_upper][2] < 200 and (50 < i < 116):
                height_dent_1_1 = i
                img[i][:height] = 0

        height_dent_4_1 = count_pixcel_dent_all - height_dent_1_1
        part_upper_dent = round(height_dent_1_1 / count_pixcel_dent_all, 1)
        part_lower_dent = round(height_dent_4_1 / count_pixcel_dent_all, 1)

        # print(f'{count_pixcel_dent_all= }')
        # print(f'{height_dent_4_1= }')
        # print(f'{height_dent_1_1= }')
        # print(f'{part_upper_dent= }')
        # print(f'{part_lowwer_dent= }')

        result_analiz = part_upper_dent - part_lower_dent  # переменная хранить данные анализа

        return result_analiz

        # cv2.imshow('cropped', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def lateral_analyze_vert(self):

        img = cv2.imread(f'{self.path_file_lateral}result_lateral.jpg', 0)
        width = img.shape[0]
        height = img.shape[1]
        height_dent_upper_6 = 0
        height_dent_lower_6 = 0

        count_pixcel_dent_all = 0  # общая длина зубов
        for y in range(width):  # ставим число по пикселям

            if img[y][48:52][0] > 190:
                img[y][50] = 0
                count_pixcel_dent_all += 1

            if img[y][48:52][0] > 190 and y < 132:
                height_dent_upper_6 += 1

        height_dent_lower_6 = count_pixcel_dent_all - height_dent_upper_6
        part_upper_dent = round(height_dent_upper_6 / count_pixcel_dent_all, 1)
        part_lowwer_dent = round(height_dent_lower_6 / count_pixcel_dent_all, 1)

        result_analiz = part_upper_dent - part_lowwer_dent  # переменная хранить данные анализа

        return result_analiz

        # cv2.imshow('cropped', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def later_analyze_sag(self):
        img = cv2.imread(f'{self.path_file_lateral}result_lateral.jpg', 0)
        width = img.shape[0]
        height = img.shape[1]
        point_medial_tuber_upper_molar = 0
        point_medial_tuber_lower_molar = 0

        # Определить первый моляр в,ч
        len_den_upper_molar = 0
        number_teeth_upper_molar = 0

        max_width_dent_pix_upper = {}

        for x in range(20, height // 2):
            if img[width // 4][x] - 15 > 200:
                len_den_upper_molar += 1

            elif len_den_upper_molar > 2:
                number_teeth_upper_molar += 1
                max_width_dent_pix_upper[number_teeth_upper_molar] = (len_den_upper_molar, x)
                len_den_upper_molar = 0

        # print(f'{max_width_dent_pix_upper= }')

        # Определить первый моляр н,ч

        len_den_lower_molar = 0
        number_teeth_lower_molar = 0
        max_width_dent_pix_lower = {}

        for x in range(height // 2):
            if img[width // 2 + 40][x] > 200:
                len_den_lower_molar += 1

            elif len_den_lower_molar > 2:
                number_teeth_lower_molar += 1
                max_width_dent_pix_lower[number_teeth_lower_molar] = (len_den_lower_molar, x)
                len_den_lower_molar = 0

        # print(f'{max_width_dent_pix_lower= }')

        # оперделение центра медиального бугра моляра в/ч

        max_len_upper_molar = 0
        for y in max_width_dent_pix_upper.values():
            if y[0] > max_len_upper_molar:
                max_len_upper_molar = y[0]
                point_medial_tuber_upper_molar = y[1]
        # print(point_medial_tuber_upper_molar)

        # оперделение центра медиального бугра моляра н/ч

        max_len_lower_molar = 0
        for y in max_width_dent_pix_lower.values():
            if y[0] > max_len_lower_molar:
                max_len_lower_molar = y[0]
                point_medial_tuber_lower_molar = y[1]
        # print(point_medial_tuber_lower_molar)

        # проводим перпендикуляр по медиальному бугру вч

        for y in range(width):  # [y][x]
            for x in range(height):
                img[y][point_medial_tuber_upper_molar] = 255
                img[y][point_medial_tuber_lower_molar] = 0

        # TODO удалить после отладки
        # print(f'{point_medial_tuber_upper_molar= }')
        # print(f'{point_medial_tuber_lower_molar= }')

        # расположение бугров относительно друг друга

        result_analiz = (point_medial_tuber_upper_molar
                         - point_medial_tuber_lower_molar)

        return result_analiz
    # endregion


class Resulter:
    """

    Interpretation of the analysis result

    """

    # region field
    def __init__(self, name_user: str, results: dict, template: dict):
        self.name_user = name_user
        self.results = results
        self.result_diagnostic = template
        self.eval_data = {}

    # endregion

    # region method
    def evaluation_data(self):
        # fill in the name
        self.result_diagnostic.update({'name': self.name_user})

        # region analiz front vertical
        result_front_vertical = self.results['front_vert']
        if len(result_front_vertical) > 0:
            if result_front_vertical[0] is True:
                self.eval_data['front_vert'] = True
                self.result_diagnostic['result_front_vertical'] = \
                    'У Вас не обнаружено смещение нижней челюсти'
            else:
                self.eval_data['front_vert'] = False
                self.result_diagnostic['result_front_vertical'] = \
                    'У Вас обнаружено смещение нижней челюсти'
        else:
            self.eval_data['front_vert'] = False
            self.result_diagnostic['result_front_vertical'] = "Вы не передали изображение"
        # endregion

        # region analiz front horizontal
        result_front_horizantal = self.results['front_hor']

        if isinstance(result_front_horizantal, float):
            if result_front_horizantal > 0.2:
                self.eval_data['front_hor'] = "overbite"
                self.result_diagnostic['result_front_hor'] = "У вас снижена высота прикуса в переднем отделе"

            elif 0 < result_front_horizantal <= 0.2:
                self.eval_data['front_hor'] = "normalbite"
                self.result_diagnostic['result_front_hor'] = "У вас нормальная высота прикуса в переднем отделе"

            elif result_front_horizantal == 0:
                self.eval_data['front_hor'] = "jointbite"
                self.result_diagnostic['result_front_hor'] = "У вас зубы смыкаются стык в стык в переднем отделе"

            elif result_front_horizantal < 0:
                self.eval_data['front_hor'] = "openbite"
                self.result_diagnostic['result_front_hor'] = "У вас увеличена высота прикуса в переднем отделе"

        # endregion

        # region analiz lateral horizontal

        result_lateral_horizontal = self.results['lateral_vert']

        if isinstance(result_lateral_horizontal, float):

            if result_lateral_horizontal > 0.4:
                self.eval_data['lateral_vert'] = "overbite"
                self.result_diagnostic['result_lateral_vert'] = ("У вас снижена высота прикуса "
                                                                 "в боковом отделе")
            elif 0 < result_lateral_horizontal <= 0.4:
                self.eval_data['lateral_vert'] = "normal"
                self.result_diagnostic['result_lateral_vert'] = "У Вас нормальная высота в боковом отделе"

            elif result_lateral_horizontal == 0:
                self.eval_data['lateral_vert'] = "jointbite"
                self.result_diagnostic['result_lateral_vert'] = ("У Вас зубы смыкаются стык в стык "
                                                                 "в боковом отделе")
            elif result_lateral_horizontal < 0:
                self.eval_data['lateral_vert'] = "openbite"
                self.result_diagnostic['result_lateral_vert'] = "У Вас не смыкаются зубы в боковом отделе"

        # endregion

        # region analiz lateral sag

        result_lateral_sag = self.results['lateral_sag']

        if isinstance(result_lateral_sag, int):
            if result_lateral_sag > 0:
                if result_lateral_sag == 0:
                    self.eval_data['lateral_sag'] = "joinbite"
                    self.result_diagnostic['result_lateral_sag'] = ("У Вас зубы смыкаются стык "
                                                                    "в стык в боковом отделе")
                elif 0 < result_lateral_sag < 50:
                    self.eval_data['lateral_sag'] = "normal"
                    self.result_diagnostic['result_lateral_sag'] = ("У вас нормальное "
                                                                    "положеие нижней челюсти")
                elif result_lateral_sag > 50:
                    self.eval_data['lateral_sag'] = "distalbite"
                    self.result_diagnostic['result_lateral_sag'] = ("У Вас нижняя челюсть "
                                                                    "расположена к зади")
            else:
                self.eval_data['lateral_sag'] = "mesialbite"
                self.result_diagnostic['result_lateral_sag'] = ("У Вас нижняя челюсть "
                                                                "расположена к перди")

        # endregion

        # Получение результатов диагностики

        vertical_diagnos = ' '
        horizontal_diagnos_front = ' '
        horizontal_diagnos_lateral = ' '

        # анализ полученных данных  в вертикальной плоскости
        # с сопоставлением данных анализи боковой группы зубов

        # region frontal overbite

        if self.eval_data['front_hor'] == 'overbite' \
                and self.eval_data['lateral_vert'] == 'overbite':
            vertical_diagnos = ("У Вас глубокий прикус", 2)

        elif self.eval_data['front_hor'] == 'overbite' \
                and self.eval_data['lateral_vert'] == 'jointbite':
            vertical_diagnos = (("Зубы смыкаются стык в стык в боковм отделе "
                                 "У Вас глубокий прикус", 2))

        elif self.eval_data['front_hor'] == 'overbite' \
                and self.eval_data['lateral_vert'] == 'openbite':
            vertical_diagnos = (("Зубы отсутствуют в жевательном отделе "
                                 "У Вас глубокий прикус", 2))

        elif self.eval_data['front_hor'] == 'overbite' \
                and self.eval_data['lateral_vert'] == 'normal':
            vertical_diagnos = ("У Вас нормальная высота прикуса ", 1)

        # endregion

        # region front normalbite

        elif self.eval_data['front_hor'] == 'normalbite' \
                and self.eval_data['lateral_vert'] == 'normal':
            vertical_diagnos = ("У Вас нормальная высота прикуса ", 0)

        elif self.eval_data['front_hor'] == 'normalbite' \
                and self.eval_data['lateral_vert'] == 'overbite':
            vertical_diagnos = ("У Вас снижена  высота прикуса в боковом отделе ", 1)

        elif self.eval_data['front_hor'] == 'normalbite' \
                and self.eval_data['lateral_vert'] == 'jointbite':
            vertical_diagnos = ("У Вас нормальная высота прикуса ", 1)

        elif self.eval_data['front_hor'] == 'normalbite' \
                and self.eval_data['lateral_vert'] == 'openbite':
            vertical_diagnos = ("У Вас нормальная высота прикуса "
                                "но отсутствуют зубы в боковом отделе", 1)

        # endregion

        # region front jointbite

        elif self.eval_data['front_hor'] == 'jointbite' \
                and self.eval_data['lateral_vert'] == 'normal':
            vertical_diagnos = ("У Вас прямой прикус ", 1)

        elif self.eval_data['front_hor'] == 'jointbite' \
                and self.eval_data['lateral_vert'] == 'overbite':
            vertical_diagnos = ("У Вас прямой прикус а также"
                                " снижена  высота прикуса в боковом отделе ", 2)

        elif self.eval_data['front_hor'] == 'jointbite' \
                and self.eval_data['lateral_vert'] == 'jointbite':
            vertical_diagnos = ("У Вас прямой прикус ", 2)

        elif self.eval_data['front_hor'] == 'jointbite' \
                and self.eval_data['lateral_vert'] == 'openbite':
            vertical_diagnos = ("У Вас прямой прикус "
                                "но отсутствуют зубы в боковом отделе", 1)

        # endregion

        # region front openbite
        elif self.eval_data['front_hor'] == 'openbite' \
                and self.eval_data['lateral_vert'] == 'normal':
            vertical_diagnos = ("У Вас Открытый прикус ", 1)

        elif self.eval_data['front_hor'] == 'openbite' \
                and self.eval_data['lateral_vert'] == 'overbite':
            vertical_diagnos = ("У Вас Открытый прикус а также"
                                " снижена  высота прикуса в боковом отделе ", 2)

        elif self.eval_data['front_hor'] == 'openbite' \
                and self.eval_data['lateral_vert'] == 'jointbite':
            vertical_diagnos = ("У Вас Открытый прикус ", 2)

        elif self.eval_data['front_hor'] == 'openbite' \
                and self.eval_data['lateral_vert'] == 'openbite':
            vertical_diagnos = ("У Вас Окрытый прикус "
                                "и отсутствуют зубы в боковом отделе", 2)

        # endregion

        # region front offset

        if self.eval_data['front_vert'] is True:
            horizontal_diagnos_front = ('У Вас смещение нижней челюсти не обнаружено', 0)
        else:
            horizontal_diagnos_front = ('У Вас обнаружено смещение нижней челюсти', 2)

        # endregion

        # region offset lateral sagital

        if self.eval_data['lateral_sag'] == "joinbite":
            horizontal_diagnos_lateral = ("У Вас прямой прикус", 1)

        elif self.eval_data['lateral_sag'] == "normal":
            horizontal_diagnos_lateral = ("У Вас нет патологии прикуса", 0)

        elif self.eval_data['lateral_sag'] == "distalbite":
            horizontal_diagnos_lateral = ("У Вас дистальнный прикус", 2)

        elif self.eval_data['lateral_sag'] == "mesialbite":
            horizontal_diagnos_lateral = ("У Вас мезиальный прикус", 2)

        # endregion

        # region list_diagnostic

        list_diagnostic = (vertical_diagnos,
                           horizontal_diagnos_lateral,
                           horizontal_diagnos_front)
        # endregion

        # region check ball diagnosis

        total_diagnosis_ball = 0
        for check_diagnosis_ball in list_diagnostic:
            total_diagnosis_ball += check_diagnosis_ball[1]

        # endregion

        # region to make a diagnosis

        preliminary_diagnosis_result = ''
        recommendation = ''

        if 0 < total_diagnosis_ball <= 3:

            preliminary_diagnosis_result = ('У вас есть незначительные изменения прикуса но они '
                                            'находятся в пределах нормы')

            recommendation = ('Рекомендовано проводить проффилактический'
                              ' осмотр у стоматолога раз в 6 месяцев')

        elif 3 < total_diagnosis_ball < 5:

            preliminary_diagnosis_result = ('У вас есть  изменения прикуса средней степени '
                                            'тяжести ')

            recommendation = ('Рекомендовано обратиться к стоматологу '
                              'для консультации и дольнейшего обследования')

        elif total_diagnosis_ball >= 5:

            preliminary_diagnosis_result = ('У Вас определяются изменения прикуса '
                                            'тяжёлой степени тяжести')

            recommendation = ('Рекомендовано обратиться к стоматологу '
                              'для консультации и дольнейшего обследования')
        # endregion

        self.result_diagnostic['preliminary diagnosis'] = preliminary_diagnosis_result
        self.result_diagnostic['recommendation'] = recommendation

        # TODO убрать после релиза
        # print('Diagnostic complete')

    def get_result(self):
        return self.result_diagnostic

    # endregion
