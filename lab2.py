import os
from datetime import datetime
from PIL import Image, ImageFilter, ImageOps

def write_log(filename: str, filter_name: str, status: str) -> None:
    log_path = os.path.join("Lab2_Media", "logs", "history.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Файл: {filename} | Фильтр: {filter_name} | Статус: {status}\n"

    with open(log_path, mode="a", encoding="UTF-8") as log_file:
        log_file.write(log_entry)

def apply_box_filter(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.BoxBlur(radius=1))


def apply_histogram_equalization(image: Image.Image) -> Image.Image:
    rgb_image = image.convert("RGB")
    return ImageOps.equalize(rgb_image)

def main() -> None:
    filename = input("Введите имя файла для обработки (например, image1.jpg или image2.png): ").strip()
    input_path = os.path.join("Lab2_Media", "data", "input", filename)
    output_path = os.path.join("Lab2_Media", "data", "output", "result.jpg")
    filter_description = "Box-фильтр (усреднение) + Выравнивание гистограммы"

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError

        if filename == "image2.png" and not os.access(input_path, os.W_OK):
            raise PermissionError

        with Image.open(input_path) as img:
            img.load()

            step1_img = apply_box_filter(img)
            result_img = apply_histogram_equalization(step1_img)

            result_img.save(output_path, format="JPEG")

        print(f"Обработка завершена успешно. Результат сохранён в {output_path}")
        write_log(filename, filter_description, "Успешно")

    except FileNotFoundError:
        print("Ошибка: Файл не найден")
    except (PermissionError, IOError):
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        write_log(filename, filter_description, "Ошибка доступа")

if __name__ == "__main__":
    main()
