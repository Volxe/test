import logging
from auto_fixer import AutoFixer
from log_analyzer import LogAnalyzer
from log_viewer import LogViewer
from rule_generator import RuleGenerator
from web_interface import app as web_app
import threading
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoFixerSystem:
    def __init__(self):
        self.auto_fixer = AutoFixer(log_level=logging.INFO)
        self.log_analyzer = LogAnalyzer()
        self.log_viewer = LogViewer()
        self.rule_generator = RuleGenerator()

    def run_auto_fixer(self):
        while True:
            try:
                logger.info("AutoFixer: Начало цикла исправления")
                code = "def example_function():\nprint('Hello, World!')"
                fixed_code = self.auto_fixer.fix_errors(code)
                logger.info(f"AutoFixer: Исправленный код:\n{fixed_code}")
                logger.info("AutoFixer: Цикл исправления завершен")
            except Exception as e:
                logger.error(f"AutoFixer: Ошибка в цикле исправления: {str(e)}")
            time.sleep(60)

    def run_log_analyzer(self):
        while True:
            try:
                logger.info("LogAnalyzer: Начало анализа логов")
                self.log_analyzer.run_analysis()
                logger.info("LogAnalyzer: Анализ логов завершен")
            except Exception as e:
                logger.error(f"LogAnalyzer: Ошибка при анализе логов: {str(e)}")
            time.sleep(600)  # Анализ каждые 10 минут

    def run_rule_generator(self):
        while True:
            try:
                logger.info("RuleGenerator: Начало генерации правил")
                new_rules = self.rule_generator.generate_rules()
                logger.info(f"RuleGenerator: Новые правила: {new_rules}")
                if new_rules:
                    self.rule_generator.apply_new_rules(self.auto_fixer)
                    logger.info("RuleGenerator: Новые правила применены к AutoFixer")
                else:
                    logger.info("RuleGenerator: Новых правил не создано")
            except Exception as e:
                logger.error(f"RuleGenerator: Ошибка при генерации правил: {str(e)}")
            time.sleep(3600)

    def run_web_interface(self):
        logger.info("WebInterface: Запуск веб-интерфейса")
        web_app.run(debug=False, use_reloader=False)

    def run(self):
        threads = [
            threading.Thread(target=self.run_auto_fixer, name="AutoFixer"),
            threading.Thread(target=self.run_log_analyzer, name="LogAnalyzer"),
            threading.Thread(target=self.run_rule_generator, name="RuleGenerator"),
            threading.Thread(target=self.run_web_interface, name="WebInterface")
        ]

        for thread in threads:
            thread.start()
            logger.info(f"Запущен поток: {thread.name}")

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    logger.info("Запуск AutoFixerSystem")
    system = AutoFixerSystem()
    system.run()