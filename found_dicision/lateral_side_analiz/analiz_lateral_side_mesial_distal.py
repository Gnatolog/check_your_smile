import cv2

img = cv2.imread('right_side.JPG', 0)
img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # resize
cropped = img[200:450, 100:400]  # обрезка изображения image[y1:y2, x1:x2]
point_medial_tuber_upper_molar = 0
point_medial_tuber_lower_molar = 0

for y in range(250):                     # оперделение центра медиального бугра моляра в/ч
    for x in range(140, 141):
        if cropped[y][x]:
            cropped[y][x]=0
    point_medial_tuber_upper_molar = 140

for y in range(250):                     # оперделение центра медиального бугра моляра н/ч
    for x in range(120,121):
        if cropped[y][x]:
            cropped[y][x]=0
    point_medial_tuber_lower_molar = 120


print(f'{point_medial_tuber_upper_molar= }')
print(f'f{point_medial_tuber_lower_molar= }')

result_analiz = (point_medial_tuber_upper_molar
                 - point_medial_tuber_lower_molar)  # расположение бугров относительно
                                                    # друг к другу


if result_analiz > 0:
    if result_analiz == 0:
        print("У Вас прямой прикус")
    elif 0 < result_analiz < 50:
        print("У Вас нормальный прикус")
    elif result_analiz > 50:
        print("У Вас II класс по Энглю")
else:
    print("У Вас III класс по Энглю")





cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()