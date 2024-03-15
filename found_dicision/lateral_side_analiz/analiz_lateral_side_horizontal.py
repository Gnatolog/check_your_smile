import cv2

img = cv2.imread('right_side.JPG', 0)
img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # resize
cropped = img[200:450, 100:400]  # обрезка изображения image[y1:y2, x1:x2]
height_dent_upper_6 = 0
height_dent_lower_6 = 0

count_pixcel_dent_all = 0  # общая длина зубов
for y in range(200):  # ставим число по пикселям

    if cropped[y][100:105][0] > 70:
        count_pixcel_dent_all += 1

    if cropped[y][100:105][0] > 50 and (40 < y < 132):
        cropped[133][60:150] = 0
        height_dent_upper_6 += 1

print(f'{count_pixcel_dent_all= }')
print(f'{height_dent_upper_6}')

height_dent_lower_6 = count_pixcel_dent_all - height_dent_upper_6
print(f'{height_dent_lower_6= }')
part_upper_dent = round(height_dent_upper_6 / count_pixcel_dent_all, 1)
part_lowwer_dent = round(height_dent_lower_6 / count_pixcel_dent_all, 1)
print(f'{part_upper_dent= }')
print(f'{part_lowwer_dent= }')

result_analiz = part_upper_dent - part_lowwer_dent   # переменная хранить данные анализа

if result_analiz > 0.4:
    print("У вас глубокий прикус")
elif  0 < result_analiz <= 0.4:
    print("У вас нормальный прикус")
elif result_analiz == 0:
    print("У вас прямой прикус")
elif result_analiz < 0:
    print("У вас открытый прикус")


cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
