import random
import re
import time
import pyperclip
import threading

def clean_spaces(text):
    """Удаляет все пробельные символы (включая неразрывные пробелы)"""
    return re.sub(r'\s+', '', text)

def change_digits(text):
    """Изменяет цифры в строке согласно правилам:
    цифра < 5 -> случайное от 0-4
    цифра >= 5 -> случайное от 5-9
    Нули не изменяются
    """
    def replace_digit(match):
        digit = int(match.group())
        # Если цифра равна 0, оставляем её без изменений
        if digit == 0:
            return '0'
        elif digit < 5:
            return str(random.randint(0, 4))
        else:
            return str(random.randint(5, 9))
    
    # Заменяем все цифры в строке
    return re.sub(r'\d', replace_digit, text)

def change_order(number_str):
    """Изменяет порядок числа согласно правилам:
    до 1000 - не менять
    до 1 млн - делить на 2
    > 1 млн - делить на 10
    """
    # Убираем все пробельные символы и запятые, заменяем запятую на точку
    clean_str = clean_spaces(number_str).replace(',', '.')
    try:
        number = float(clean_str)
        if number < 1000:
            return number
        elif number < 1000000:
            return number / 2
        else:
            return number / 10
    except ValueError:
        return number_str  # Возвращаем исходную строку если не удалось преобразовать

def process_number_line(line):
    """Обрабатывает одну строку с числом"""
    # Убираем лишние пробелы и спецсимволы
    line = line.strip()
    if not line:
        return line
    # Сначала изменяем порядок
    result_number = change_order(line)
    # Затем изменяем цифры
    changed_digits = change_digits(str(result_number))
    # Форматируем результат с разделителями тысяч
    if isinstance(changed_digits, str) and changed_digits.replace('.', '').replace('-', '').isdigit():
        try:
            num = float(changed_digits)
            formatted = f"{num:,.2f}".replace(',', ' ').replace('.', ',')
            return formatted
        except ValueError:
            return changed_digits
    else:
        return changed_digits

def is_number_string(text):
    """Проверяет, является ли строка числом с пробелами, запятыми и спецсимволами"""
    if not text or not text.strip():
        return False
    # Убираем все пробельные символы и заменяем запятую на точку
    clean_text = clean_spaces(text).replace(',', '.')
    try:
        float(clean_text)
        return True
    except ValueError:
        return False

def monitor_clipboard():
    """Мониторит буфер обмена и обрабатывает числа"""
    print("Мониторинг буфера обмена запущен...")
    print("Программа будет автоматически обрабатывать числа, скопированные в буфер обмена.")
    print("Нажмите Ctrl+C для остановки.")
    last_clipboard = ""
    try:
        while True:
            try:
                current_clipboard = pyperclip.paste()
                # Пропускаем, если уже обработано (начинается с '+')
                if current_clipboard != last_clipboard and not current_clipboard.strip().startswith('+'):
                    if is_number_string(current_clipboard):
                        print(f"\nОбнаружено число в буфере: {current_clipboard}")
                        result = process_number_line(current_clipboard)
                        result_with_plus = '+' + str(result)
                        print(f"Результат обработки: {result_with_plus}")
                        pyperclip.copy(result_with_plus)
                        print(f"Результат скопирован в буфер обмена: {result_with_plus}")
                    last_clipboard = current_clipboard
                time.sleep(0.5)
            except Exception as e:
                print(f"Ошибка при обработке буфера обмена: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nМониторинг буфера обмена остановлен.")

def main():
    print("Программа мониторинга буфера обмена для обработки чисел")
    print("=" * 60)
    try:
        test_clipboard = pyperclip.paste()
        print("Буфер обмена доступен.")
    except Exception as e:
        print(f"Ошибка доступа к буферу обмена: {e}")
        print("Убедитесь, что установлена библиотека pyperclip: pip install pyperclip")
        return
    monitor_clipboard()

if __name__ == "__main__":
    main()