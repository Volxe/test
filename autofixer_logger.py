import logging
from datetime import datetime

class AutofixerLogger:
    def __init__(self, log_file='autofixer.log', level=logging.INFO):
        self.logger = logging.getLogger('AutofixerLogger')
        self.logger.setLevel(level)
        
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.error_counts = {}
        self.fix_counts = {}
        self.total_fixes = 0
        self.successful_fixes = 0

    def log_fix(self, error_type, rule_applied, result, level=logging.INFO):
        log_message = f"Ошибка: {error_type} | Правило: {rule_applied} | Результат: {result}"
        self.logger.log(level, log_message)

        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        self.fix_counts[rule_applied] = self.fix_counts.get(rule_applied, 0) + 1
        self.total_fixes += 1
        if result == "Исправлено":
            self.successful_fixes += 1

    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def get_statistics(self):
        success_rate = (self.successful_fixes / self.total_fixes) * 100 if self.total_fixes > 0 else 0
        stats = {
            "total_fixes": self.total_fixes,
            "successful_fixes": self.successful_fixes,
            "success_rate": f"{success_rate:.2f}%",
            "error_counts": dict(self.error_counts),
            "fix_counts": dict(self.fix_counts)
        }
        return stats

    def print_statistics(self):
        stats = self.get_statistics()
        self.logger.info("Статистика автофиксера:")
        self.logger.info(f"Всего исправлений: {stats['total_fixes']}")
        self.logger.info(f"Успешных исправлений: {stats['successful_fixes']}")
        self.logger.info(f"Процент успешных исправлений: {stats['success_rate']}")
        self.logger.info("Количество ошибок по типам:")
        for error_type, count in stats['error_counts'].items():
            self.logger.info(f"  {error_type}: {count}")
        self.logger.info("Количество применений правил:")
        for rule, count in stats['fix_counts'].items():
            self.logger.info(f"  {rule}: {count}")

def set_log_level(level):
    logger = logging.getLogger('AutofixerLogger')
    logger.setLevel(level)

# Пример использования
if __name__ == "__main__":
    logger = AutofixerLogger(level=logging.DEBUG)
    logger.log_debug("Это отладочное сообщение")
    logger.log_info("Это информационное сообщение")
    logger.log_warning("Это предупреждение")
    logger.log_error("Это сообщение об ошибке")
    logger.log_fix("Синтаксическая ошибка", "Добавление двоеточия", "Исправлено", level=logging.INFO)
    logger.log_fix("Отсутствие скобок", "Добавление скобок", "Исправлено", level=logging.DEBUG)
    logger.print_statistics()

    print("\nИзменение уровня логирования на WARNING")
    set_log_level(logging.WARNING)
    logger.log_debug("Это отладочное сообщение не должно отображаться")
    logger.log_info("Это информационное сообщение не должно отображаться")
    logger.log_warning("Это предупреждение должно отображаться")
    logger.log_error("Это сообщение об ошибке должно отображаться")