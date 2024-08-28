import json
import threading

class StatisticsManager:
    def __init__(self, stats_file='autofixer_stats.json'):
        self.stats_file = stats_file
        self.stats_lock = threading.Lock()
        self.load_stats()

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
        with self.stats_lock:
            return self.stats.copy()
