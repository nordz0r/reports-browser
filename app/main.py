import os
from datetime import datetime
from flask import Flask, render_template, send_from_directory

FOLDER = os.getenv("FOLDER")

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    files_list = os.listdir(FOLDER)

    reports = []

    for file in files_list:
        file_path = os.path.join(FOLDER, file)
        if os.path.isfile(file_path):
            report_id, date_start, date_end = file.split('.')[0].split('_')
            file_size = human_readable_size(os.path.getsize(file_path))


            reports.append({
                'id': report_id,
                'date_start': date_start,
                'date_end': date_end,
                'file_size': file_size,
            })

    # Сортировка списка отчетов по дате начала, от самого нового к самому старому
    reports = sorted(reports, key=lambda r: datetime.strptime(r['date_start'], '%Y-%m-%d'), reverse=True)
    
    return render_template('index.html', reports=reports)


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
