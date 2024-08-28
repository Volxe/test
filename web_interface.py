from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from auto_fixer import AutoFixer
import difflib
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

ALLOWED_EXTENSIONS = {'py', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

auto_fixer = AutoFixer()

@app.route('/get_statistics')
def get_statistics():
    stats = auto_fixer.get_stats()
    stats['success_rate'] = f"{(stats['successful_fixes'] / stats['total_fixes'] * 100):.2f}%" if stats['total_fixes'] > 0 else "0%"
    return render_template('statistics_partial.html', stats=stats)

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/logs')
def logs():
    with open(auto_fixer.log_file, 'r') as f:
        logs = []
        for line in f.readlines()[-50:]:  # Показываем последние 50 записей
            timestamp_str, message = line.split(' - ', 1)
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
            except ValueError:
                timestamp = timestamp_str  # Если не удается преобразовать, оставляем как есть
            logs.append({'timestamp': timestamp, 'message': message.strip()})
    return render_template('logs.html', logs=logs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            fixed_file_path, comments = auto_fixer.fix_file(file_path)
            
            if fixed_file_path:
                with open(fixed_file_path, 'r', encoding='utf-8') as f:
                    fixed_code = f.read()
                
                diff = list(difflib.unified_diff(
                    original_code.splitlines(keepends=True),
                    fixed_code.splitlines(keepends=True),
                    fromfile='Original',
                    tofile='Fixed',
                    n=10
                ))
                
                fixed_filename = os.path.basename(fixed_file_path)
                return render_template('result.html', 
                                       original_code=original_code, 
                                       fixed_code=fixed_code, 
                                       diff=diff,
                                       comments=comments,
                                       fixed_filename=fixed_filename)
            else:
                return "Не удалось исправить файл", 500
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)