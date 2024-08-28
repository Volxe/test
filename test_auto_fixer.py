import os
from auto_fixer import AutoFixer
import difflib

def test_auto_fixer():
    auto_fixer = AutoFixer()
    test_files_dir = "test_files"
    test_files = [f for f in os.listdir(test_files_dir) if f.endswith('.py')]

    for file in test_files:
        file_path = os.path.join(test_files_dir, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"Тестирование файла: {file}")
            print("Оригинальный код:")
            print(code)
            print("\nИсправленный код:")
            
            fixed_code = auto_fixer.fix_errors(code)
            print(fixed_code)
            
            # Показываем разницу
            print("\nРазница:")
            diff = difflib.unified_diff(code.splitlines(), fixed_code.splitlines(), lineterm='')
            for line in diff:
                if line.startswith('+'):
                    print(f"\033[92m{line}\033[0m")  # Зеленый для добавленных строк
                elif line.startswith('-'):
                    print(f"\033[91m{line}\033[0m")  # Красный для удаленных строк
                else:
                    print(line)
            
            # Сохраняем исправленный код в новый файл
            fixed_file_path = os.path.join(test_files_dir, f"fixed_{file}")
            with open(fixed_file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
        except Exception as e:
            print(f"Ошибка при обработке файла {file}: {str(e)}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_auto_fixer()

