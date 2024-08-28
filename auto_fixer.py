import logging
import re
import os
import difflib
import json
from datetime import datetime
from autofixer_logger import AutofixerLogger, set_log_level
from statistics_manager import StatisticsManager

class AutoFixer:
    def __init__(self, log_file='autofixer.log', stats_file='autofixer_stats.json'):
        self.log_file = log_file
        self.logger = AutofixerLogger(level=logging.INFO)
        self.stats_manager = StatisticsManager(stats_file=stats_file)

    def load_stats(self):
        try:
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        except FileNotFoundError:
            self.stats = {
                "total_fixes": 0,
                "successful_fixes": 0,
                "error_counts": {},
                "fix_counts": {}
            }

    def save_stats(self):
        with self.stats_lock:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f)

    def update_stats(self, error_type, fix_type, success):
        with self.stats_lock:
            self.stats["total_fixes"] += 1
            if success:
                self.stats["successful_fixes"] += 1
            self.stats["error_counts"][error_type] = self.stats["error_counts"].get(error_type, 0) + 1
            self.stats["fix_counts"][fix_type] = self.stats["fix_counts"].get(fix_type, 0) + 1
            self.save_stats()

    def get_stats(self):
        return self.stats_manager.get_stats()

    def set_log_level(self, level):
        self.logger.logger.setLevel(level)

    def fix_file(self, file_path):
        self.logger.log_info(f"Начало исправления файла: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                original_code = file.read()
            
            fixed_code = self.fix_errors(original_code)
            
            fixed_file_path = self.get_fixed_file_path(file_path)
            with open(fixed_file_path, 'w', encoding='utf-8') as file:
                file.write(fixed_code)
            
            comments = self.generate_comments(original_code, fixed_code)
            
            self.logger.log_info(f"Файл исправлен и сохранен: {fixed_file_path}")
            return fixed_file_path, comments
        except Exception as e:
            self.logger.log_error(f"Ошибка при исправлении файла: {str(e)}")
            return None, None

    def get_fixed_file_path(self, original_path):
        dir_name, file_name = os.path.split(original_path)
        base_name, ext = os.path.splitext(file_name)
        return os.path.join(dir_name, f"{base_name}_fixed{ext}")

    def fix_errors(self, code):
        self.logger.log_info("Начало исправления ошибок")
        
        # Существующие исправления
        code = self.add_colons(code)
        code = self.remove_semicolons(code)
        code = self.fix_indentation(code)
        
        # Новые исправления
        code = self.fix_string_concatenation(code)
        code = self.fix_method_calls(code)
        code = self.fix_type_conversion(code)
        code = self.fix_function_calls(code)
        code = self.add_else_colons(code)
        code = self.fix_variable_naming(code)
        code = self.fix_import_style(code)
        code = self.fix_comparison_operators(code)
        
        self.logger.log_info("Завершение исправления ошибок")
        return code

    def fix_string_concatenation(self, code):
        # Заменяем конкатенацию строки и переменной на f-строку
        pattern = r'print\("([^"]+)" \+ ([^)]+)\)'
        replacement = r'print(f"\1{{\2}}")'
        return re.sub(pattern, replacement, code)

    def fix_method_calls(self, code):
        # Добавляем скобки к вызовам методов без аргументов
        pattern = r'(\w+)\.(\w+)(?!\()'
        replacement = r'\1.\2()'
        return re.sub(pattern, replacement, code)

    def fix_type_conversion(self, code):
        # Добавляем преобразование типов для input
        pattern = r'(\w+)\s*=\s*input\(([^)]+)\)'
        replacement = r'\1 = int(input(\2))'
        return re.sub(pattern, replacement, code)

    def fix_function_calls(self, code):
        # Исправляем синтаксис вызова функций
        pattern = r'(\w+)\((\w+)\s+(\w+)\)'
        replacement = r'\1(\2, \3)'
        return re.sub(pattern, replacement, code)

    def add_else_colons(self, code):
        # Добавляем двоеточие после else
        pattern = r'\belse(?!\s*:)'
        replacement = r'else:'
        return re.sub(pattern, replacement, code)

    def add_colons(self, code):
        # Добавляем двоеточие после определения функций и классов
        pattern = r'(def|class|if|elif|else|for|while|try|except|finally)([^\n:]*)\n'
        replacement = r'\1\2:\n'
        return re.sub(pattern, replacement, code)

    def remove_semicolons(self, code):
        # Удаляем точки с запятой в конце строк
        return re.sub(r';(\s*\n)', r'\1', code)

    def fix_indentation(self, code):
        # Простая коррекция отступов (может потребоваться более сложная логика)
        lines = code.split('\n')
        indented_lines = []
        indent_level = 0
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith(('def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally')):
                indented_lines.append('    ' * indent_level + stripped_line)
                indent_level += 1
            elif stripped_line == '':
                indented_lines.append('')
            else:
                indented_lines.append('    ' * indent_level + stripped_line)
        return '\n'.join(indented_lines)

    def fix_error(self, code, error_type):
        self.logger.log_debug(f"Попытка исправления ошибки типа: {error_type}")
        # Логика исправления ошибки
        fixed_code = self.apply_fix(code, error_type)
        
        # Логирование результата
        result = "Исправлено" if fixed_code != code else "Не исправлено"
        self.logger.log_fix(error_type, "Применено правило X", result, level=logging.INFO)
        
        return fixed_code

    def apply_fix(self, code, error_type):
        self.logger.log_debug(f"Применение правила для ошибки типа: {error_type}")
        # Реализация конкретных правил исправления
        if error_type == "missing_colon":
            return self.add_colons(code)
        elif error_type == "extra_semicolon":
            return self.remove_semicolons(code)
        # Добавьте другие типы ошибок по мере необходимости
        return code

    def print_statistics(self):
        self.logger.print_statistics()

    def add_rule(self, name, pattern, replacement):
        setattr(self, name, lambda code: re.sub(pattern, replacement, code))
        self.logger.log_info(f"Добавлено новое правило: {name}")

    def fix_variable_naming(self, code):
        # Исправляем имена переменных, начинающиеся с заглавной буквы
        pattern = r'\b([A-Z][a-z0-9]+)\b(?!\s*=\s*class\b)'
        replacement = lambda m: m.group(1).lower()
        return re.sub(pattern, replacement, code)

    def fix_import_style(self, code):
        # Заменяем "from module import *" на "import module"
        pattern = r'from\s+(\w+)\s+import\s+\*'
        replacement = r'import \1'
        return re.sub(pattern, replacement, code)

    def fix_comparison_operators(self, code):
        # Заменяем "==" на "is" для сравнения с None, True, False
        pattern = r'(==|!=)\s*(None|True|False)\b'
        replacement = lambda m: 'is' if m.group(1) == '==' else 'is not'
        return re.sub(pattern, replacement, code)

    def generate_comments(self, original_code, fixed_code):
        diff = list(difflib.unified_diff(
            original_code.splitlines(keepends=True),
            fixed_code.splitlines(keepends=True),
            fromfile='Original',
            tofile='Fixed',
            n=0
        ))

        comments = []
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                comments.append(self.analyze_addition(line[1:]))
            elif line.startswith('-') and not line.startswith('---'):
                comments.append(self.analyze_removal(line[1:]))

        return "\n".join(comments)

    def analyze_addition(self, line):
        line = line.strip()
        if line.endswith(':'):
            return f"Добавлено двоеточие в конце строки: '{line}'"
        elif re.match(r'^\s+', line):
            return f"Исправлен отступ в строке: '{line}'"
        elif '=' in line:
            return f"Добавлено присваивание: '{line}'"
        else:
            return f"Добавлена новая строка: '{line}'"

    def analyze_removal(self, line):
        line = line.strip()
        if line.endswith(';'):
            return f"Удалена точка с запятой в конце строки: '{line}'"
        elif re.match(r'^\s+', line):
            return f"Удалена строка с неправильным отступом: '{line}'"
        else:
            return f"Удалена строка: '{line}'"

# Пример использования
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python auto_fixer.py <путь_к_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    fixer = AutoFixer(log_level=logging.DEBUG)
    fixed_file_path, comments = fixer.fix_file(file_path)

    if fixed_file_path:
        print(f"Файл исправлен и сохранен: {fixed_file_path}")
        print(comments)
    else:
        print("Не удалось исправить файл")

    fixer.print_statistics()