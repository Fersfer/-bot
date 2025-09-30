import cv2
import numpy as np

image_path = 'screen.jpg'

def get_red_fill_percentage(image_path, x1, y1, x2, y2):
    """
    Вычисляет процент заполнения красными оттенками в заданном прямоугольнике
    на скриншоте.

    :param image_path: Путь к файлу скриншота.
    :param x1, y1: Координаты верхнего левого угла прямоугольника.
    :param x2, y2: Координаты нижнего правого угла прямоугольника.
    :return: Процент заполнения красным цветом или None в случае ошибки.
    """
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print(f"Ошибка: Не удалось загрузить изображение по пути {image_path}")
        return None

    # Проверка корректности координат
    height, width, _ = image.shape
    if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
        print("Ошибка: Некорректные координаты прямоугольника.")
        return None

    # Вырезаем область интереса (ROI)
    roi = image[y1:y2, x1:x2]

    # Если ROI пустой (например, из-за некорректных координат), возвращаем 0
    if roi.shape[0] == 0 or roi.shape[1] == 0:
        print("Ошибка: Область интереса пуста.")
        return 0.0

    # Преобразование ROI в HSV
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Определение диапазонов для красного цвета в HSV
    # Красный цвет находится на двух концах спектра HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Создание маски для каждого диапазона
    mask1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
    # Объединение масок для получения полной маски красного цвета
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Подсчет количества красных пикселей в ROI
    # red_mask будет бинарным изображением (0 или 255).
    # Non-zero count вернет количество пикселей со значением 255 (красные).
    num_red_pixels = cv2.countNonZero(red_mask)

    # Общее количество пикселей в ROI
    total_pixels_in_roi = roi.shape[0] * roi.shape[1]

    # Вычисление процента
    if total_pixels_in_roi == 0:
        return 0.0
    percentage = (num_red_pixels / total_pixels_in_roi) * 100

    return percentage


# ХП моба
rect_x1, rect_y1, rect_x2, rect_y2 = 786, 2, 1132, 7
mob_health = get_red_fill_percentage(image_path, rect_x1, rect_y1, rect_x2, rect_y2)
# ХП перса
rectp_x1, rectp_y1, rectp_x2, rectp_y2 = 29, 58, 240, 60
pers_health = get_red_fill_percentage(image_path, rectp_x1, rectp_y1, rectp_x2, rectp_y2)
# Результат на скрине
image_display = cv2.imread(image_path)
if image_display is not None:
    cv2.rectangle(image_display, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 0), 1)
    cv2.putText(image_display, f"{mob_health:.1f}%", (rect_x1, rect_y2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.rectangle(image_display, (rectp_x1, rectp_y1), (rectp_x2, rectp_y2), (0, 255, 0), 1)
    cv2.putText(image_display, f"{pers_health:.1f}%", (rectp_x1, rectp_y2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Image with ROI", image_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()