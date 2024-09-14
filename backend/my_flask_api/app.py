import os
import random
from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS  # เพิ่มการนำเข้า CORS

app = Flask(__name__)
CORS(app)  # เพิ่มการกำหนด CORS

UPLOAD_FOLDER = 'uploads/'
MUSIC_FOLDER = './music/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_emotion():
    # สุ่มอารมณ์จาก 3 แบบ: positive, neutral, negative
    return random.choice(['positive', 'neutral', 'negative'])

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    # ตรวจสอบว่ามีไฟล์ใน request หรือไม่
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # ตรวจสอบว่ามีไฟล์ถูกเลือกหรือไม่
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # ตรวจสอบว่านามสกุลไฟล์ถูกต้องหรือไม่
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # สุ่มอารมณ์ (ในขั้นตอนนี้ยังไม่ทำการประมวลผลจริง)
        emotion = random_emotion()

        # หาไฟล์เพลงที่เหมาะสมกับอารมณ์ที่สุ่มได้ในโฟลเดอร์ mp3 และหาไฟล์ปกในโฟลเดอร์ png
        music_path = os.path.join(MUSIC_FOLDER, emotion, 'mp3')
        cover_path = os.path.join(MUSIC_FOLDER, emotion, 'png')

        if not os.path.exists(music_path) or not os.listdir(music_path):
            return jsonify({'error': 'No music available for this emotion'}), 500
        if not os.path.exists(cover_path):
            return jsonify({'error': 'No cover images available for this emotion'}), 500

        # สุ่มเลือกเพลง 1 เพลงจากโฟลเดอร์ mp3
        selected_song = random.choice(os.listdir(music_path))
        song_name = os.path.splitext(selected_song)[0]  # ดึงชื่อเพลงโดยไม่เอาส่วนขยาย

        # ตรวจสอบว่ามีไฟล์ปกที่ตรงกับเพลงในโฟลเดอร์ png หรือไม่
        cover_image = f"{song_name}.png"
        cover_image_path = os.path.join(cover_path, cover_image)

        if not os.path.exists(cover_image_path):
            return jsonify({'error': f'Cover image for {song_name} not found'}), 500

        # สร้าง URL สำหรับไฟล์เพลงและรูปภาพที่สามารถเข้าถึงได้
        song_url = url_for('get_file', folder='mp3', filename=selected_song, emotion=emotion, _external=True)
        cover_url = url_for('get_file', folder='png', filename=cover_image, emotion=emotion, _external=True)

        # ส่ง URL ของไฟล์เพลงและรูปปกกลับไป
        return jsonify({
            'emotion': emotion,
            'song_url': song_url,
            'cover_url': cover_url
        })

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/file/<emotion>/<folder>/<filename>', methods=['GET'])
def get_file(emotion, folder, filename):
    # ส่งไฟล์จากโฟลเดอร์ mp3 หรือ png ตามคำขอ
    folder_path = os.path.join(MUSIC_FOLDER, emotion, folder)
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        if folder == 'mp3':
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype='audio/mpeg')
        elif folder == 'png':
            return send_file(file_path, as_attachment=True, download_name=filename, mimetype='image/png')
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    # ตรวจสอบว่าโฟลเดอร์สำหรับเก็บไฟล์ที่อัปโหลดมีอยู่หรือไม่ ถ้าไม่มีก็สร้างใหม่
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)
