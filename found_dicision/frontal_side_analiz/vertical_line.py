import cv2

img = cv2.imread('normal_bite.JPG', 0)
img = cv2.resize(img, (800, 600), interpolation=cv2.INTER_CUBIC)  # resize
cropped = img[200:400, 200:650]  # обрезка изображения image[y1:y2, x1:x2]
point_line_upper_jaw = 0
point_line_lower_jaw = 0

for y in range(200):  # [y][x]
    for x in range(150, 350):  # порводим перпедикуляр по центру верхних зубов
        cropped[y][250] = 0
        print(f'{y= }')
        if y == 180:
            point_line_upper_jaw = 250  # получаем точку проекции центра между зубами в/ч на н/ч

for y in range(100, 200):  # [y][x]
    for x in range(150, 350):  # проводим перпедикуляр по центру нижних зубов зубов
        cropped[y][234] = 0
        point_line_lower_jaw = 234  # значение устанавливаем по x

print(f'{point_line_upper_jaw= }\n{point_line_lower_jaw= }')

result_vertical_analiz = point_line_upper_jaw - point_line_lower_jaw

if result_vertical_analiz >= 0:

    if 0 <= result_vertical_analiz < 50:
        print("У Вас нормальный прикус")
    elif result_vertical_analiz > 50:
        print("У вас обнаружена патология")
else:
    if -50 < result_vertical_analiz < 0:
        print("У вас нормальный прикус")
    elif result_vertical_analiz < -50:
        print("У Вас патология прикуса")

cv2.imshow('cropped', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
