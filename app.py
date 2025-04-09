from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Download route (MUST be POST)
@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    temp_id = str(uuid.uuid4())[:8]
    output_template = f"{temp_id}.%(ext)s"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
