import sys
from auto_fixer import AutoFixer
import logging

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python fix_file.py <путь_к_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    fixer = AutoFixer(log_level=logging.INFO)
    fixed_file_path = fixer.fix_file(file_path)

    if fixed_file_path:
        print(f"Файл исправлен и сохранен: {fixed_file_path}")
    else:
        print("Не удалось исправить файл")

    fixer.print_statistics()