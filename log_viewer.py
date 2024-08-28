import os
import re
from datetime import datetime

class LogViewer:
    def __init__(self, log_file='autofixer.log'):
        self.log_file = log_file

    def read_logs(self):
        with open(self.log_file, 'r') as file:
            return file.readlines()

    def parse_log_entry(self, line):
        match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (.*)', line)
        if match:
            timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S,%f')
            message = match.group(2)
            return timestamp, message
        return None, None

    def display_logs(self, start_date=None, end_date=None, error_type=None):
        logs = self.read_logs()
        for line in logs:
            timestamp, message = self.parse_log_entry(line)
            if timestamp:
                if start_date and timestamp < start_date:
                    continue
                if end_date and timestamp > end_date:
                    continue
                if error_type and error_type not in message:
                    continue
                print(f"{timestamp}: {message}")

    def display_statistics(self):
        logs = self.read_logs()
        error_counts = {}
        fix_counts = {}
        total_fixes = 0
        successful_fixes = 0

        for line in logs:
            _, message = self.parse_log_entry(line)
            if message:
                parts = message.split(' | ')
                if len(parts) == 3:
                    error_type = parts[0].split(': ')[1]
                    rule = parts[1].split(': ')[1]
                    result = parts[2].split(': ')[1]

                    error_counts[error_type] = error_counts.get(error_type, 0) + 1
                    fix_counts[rule] = fix_counts.get(rule, 0) + 1
                    total_fixes += 1
                    if result == "Исправлено":
                        successful_fixes += 1

        print("Статистика автофиксера:")
        print(f"Всего исправлений: {total_fixes}")
        print(f"Успешных исправлений: {successful_fixes}")
        print(f"Процент успешных исправлений: {(successful_fixes / total_fixes) * 100:.2f}%")
        print("\nКоличество ошибок по типам:")
        for error_type, count in error_counts.items():
            print(f"  {error_type}: {count}")
        print("\nКоличество применений правил:")
        for rule, count in fix_counts.items():
            print(f"  {rule}: {count}")

def main():
    viewer = LogViewer()
    while True:
        print("\nМеню:")
        print("1. Показать все логи")
        print("2. Показать логи за определенный период")
        print("3. Показать логи определенного типа ошибок")
        print("4. Показать статистику")
        print("5. Выход")
        
        choice = input("Выберите опцию: ")
        
        if choice == '1':
            viewer.display_logs()
        elif choice == '2':
            start_date = input("Введите начальную дату (YYYY-MM-DD): ")
            end_date = input("Введите конечную дату (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            viewer.display_logs(start_date, end_date)
        elif choice == '3':
            error_type = input("Введите тип ошибки: ")
            viewer.display_logs(error_type=error_type)
        elif choice == '4':
            viewer.display_statistics()
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()