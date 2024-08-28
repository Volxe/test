from log_viewer import LogViewer
from collections import Counter
from datetime import datetime, timedelta
import time

class LogAnalyzer(LogViewer):
    def __init__(self, log_file='autofixer.log'):
        super().__init__(log_file)

    def analyze_logs(self, minutes=10):  # Изменено с 1 на 10 минут
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=minutes)
        logs = self.read_logs()  # Изменено с get_logs на read_logs

        error_types = Counter()
        fix_rules = Counter()
        total_fixes = 0
        successful_fixes = 0

        for line in logs:
            timestamp, message = self.parse_log_entry(line)
            if timestamp and start_date <= timestamp <= end_date:
                parts = message.split(' | ')
                if len(parts) == 3:
                    error_type = parts[0].split(': ')[1]
                    rule = parts[1].split(': ')[1]
                    result = parts[2].split(': ')[1]

                    error_types[error_type] += 1
                    fix_rules[rule] += 1
                    total_fixes += 1
                    if result == "Исправлено":
                        successful_fixes += 1

        success_rate = (successful_fixes / total_fixes * 100) if total_fixes > 0 else 0

        report = f"Отчет по анализу логов за последнюю минуту:\n\n"
        report += f"Всего исправлений: {total_fixes}\n"
        report += f"Успешных исправлений: {successful_fixes}\n"
        report += f"Процент успешных исправлений: {success_rate:.2f}%\n\n"

        report += "Топ-5 наиболее частых ошибок:\n"
        for error, count in error_types.most_common(5):
            report += f"  {error}: {count}\n"

        report += "\nТоп-5 наиболее эффективных правил:\n"
        for rule, count in fix_rules.most_common(5):
            report += f"  {rule}: {count}\n"

        return report

    def run_analysis(self):
        report = self.analyze_logs(minutes=10)  # Изменено с 1 на 10 минут
        print(report)
        
        # Сохраняем отчет в файл
        with open("log_analysis_report.txt", "a") as f:
            f.write(f"\n{datetime.now()}\n")
            f.write(report)
            f.write("\n" + "="*50 + "\n")

    def get_statistics(self):
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

        success_rate = (successful_fixes / total_fixes) * 100 if total_fixes > 0 else 0
        return {
            'total_fixes': total_fixes,
            'successful_fixes': successful_fixes,
            'success_rate': f"{success_rate:.2f}%",
            'error_counts': error_counts,
            'fix_counts': fix_counts
        }

if __name__ == "__main__":
    analyzer = LogAnalyzer()
    print("Запуск анализатора логов. Анализ будет проводиться каждую минуту.")
    while True:
        analyzer.run_analysis()
        time.sleep(60)  # Ждем 60 секунд перед следующим анализом