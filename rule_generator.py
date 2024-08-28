from auto_fixer import AutoFixer
from log_analyzer import LogAnalyzer
from log_viewer import LogViewer
import re

class RuleGenerator:
    def __init__(self):
        self.log_analyzer = LogAnalyzer()
        self.log_viewer = LogViewer()
        self.auto_fixer = AutoFixer()

    def generate_rules(self):
        # Используем LogAnalyzer вместо LogViewer для получения статистики
        log_analysis = self.log_analyzer.analyze_logs()
        
        # Получение статистики из LogAnalyzer
        stats = self.log_analyzer.get_statistics()
        
        # Генерация новых правил на основе анализа и статистики
        proposed_rules = self.create_proposed_rules(log_analysis, stats)
        
        # Тестирование новых правил
        validated_rules = self.test_rules(proposed_rules)
        
        return validated_rules

    def create_proposed_rules(self, log_analysis, stats):
        proposed_rules = []
        
        # Анализ наиболее частых ошибок
        for error_type, count in stats['error_counts'].items():
            if count > 3:  # Изменено с 10 на 3
                new_rule = self.create_rule_for_error(error_type)
                if new_rule:
                    proposed_rules.append(new_rule)
        
        # Анализ неэффективных правил
        for rule, count in stats['fix_counts'].items():
            if count < 2:  # Изменено с 5 на 2
                improved_rule = self.improve_existing_rule(rule)
                if improved_rule:
                    proposed_rules.append(improved_rule)
        
        return proposed_rules

    def create_rule_for_error(self, error_type):
        # Логика создания нового правила на основе типа ошибки
        # Это пример, вам нужно будет реализовать конкретную логику
        if error_type == "missing_parentheses":
            return {
                "name": "add_missing_parentheses",
                "pattern": r'(\w+)\.(\w+)(?!\()',
                "replacement": r'\1.\2()'
            }
        # Добавьте другие типы ошибок по мере необходимости
        return None

    def improve_existing_rule(self, rule):
        # Логика улучшения существующего правила
        # Это пример, вам нужно будет реализовать конкретную логику
        if rule == "add_colons":
            return {
                "name": "add_colons_improved",
                "pattern": r'(def|class|if|elif|else|for|while|try|except|finally)([^\n:]*)\n(?!\s*:)',
                "replacement": r'\1\2:\n'
            }
        # Добавьте другие правила по мере необходимости
        return None

    def test_rules(self, proposed_rules):
        validated_rules = []
        for rule in proposed_rules:
            if self.test_rule_on_samples(rule):
                validated_rules.append(rule)
        return validated_rules

    def test_rule_on_samples(self, rule):
        # Тестирование правила на образцах кода
        # Это пример, вам нужно будет реализовать конкретную логику тестирования
        sample_codes = [
            "def function_name\n    pass",
            "if condition\n    do_something()",
            "for item in items\n    print(item)"
        ]
        success_count = 0
        for code in sample_codes:
            fixed_code = re.sub(rule['pattern'], rule['replacement'], code)
            if fixed_code != code:
                success_count += 1
        
        return success_count / len(sample_codes) > 0.7  # Пример порога успешности

    def apply_new_rules(self, auto_fixer):
        new_rules = self.generate_rules()
        for rule in new_rules:
            # Добавляем новое правило в AutoFixer
            auto_fixer.add_rule(rule['name'], rule['pattern'], rule['replacement'])
        return new_rules

# Пример использования
generator = RuleGenerator()
validated_rules = generator.generate_rules()