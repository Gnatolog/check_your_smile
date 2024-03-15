import numpy as np
import cv2

img = cv2.imread('normal_bite.JPG', 0)

height = img.shape[0]
width = img.shape[1]
img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # resize
cropped = img[200:400, 200:650]  # обрезка изображения image[y1:y2, x1:x2]
list_pix = []
height_dent_1_1 = 0  # длина первого резца вч
count_pixcel_dent_all = 0  # общая длина зубов
for i in range(200):
    print(cropped[i][185:190][3])
    if cropped[i][185:190][3] > 160:
        count_pixcel_dent_all += 1
    if cropped[i][185:190][3] < 200 and (i > 50 and i < 116):
        height_dent_1_1 = i
        cropped[i][:450] = 0

height_dent_4_1 = count_pixcel_dent_all - height_dent_1_1
part_upper_dent = round(height_dent_1_1 / count_pixcel_dent_all, 1)
part_lowwer_dent = round(height_dent_4_1 / count_pixcel_dent_all, 1)
print(f'{height_dent_4_1= }')
print(f'{height_dent_1_1= }')
print(f'{part_upper_dent= }')
print(f'{part_lowwer_dent= }')

# первые выводы

result_analiz = part_upper_dent - part_lowwer_dent  # переменная хранить данные анализа

if result_analiz > 0.2:
    print("У вас глубокий прикус")
elif 0 < result_analiz <= 0.2:
    print("У вас нормальный прикус")
elif result_analiz == 0:
    print("У вас прямой прикус")
elif result_analiz < 0:
    print("У вас открытый прикус")

# cv2.line(img,(0,(height//2)),(wight,(height//2)),(0,0,0),2)  # горизантальная линия
# cv2.line(img,((wight//2), 0),((wight//2),height),(0,0,0),2)  # вертикальная линия
# cv2.imshow('image', img)
cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
