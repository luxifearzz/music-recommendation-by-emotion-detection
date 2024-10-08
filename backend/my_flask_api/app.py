import os
import random
import json
from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
MUSIC_FOLDER = './music/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image_for_model(filepath):
    # เตรียมข้อมูลรูปภาพเพื่อส่งเข้าโมเดล
    # นี่เป็นตัวอย่างการเตรียมข้อมูล เช่น การแปลงรูปภาพเป็น array หรือการจัดการรูปภาพ
    # คุณสามารถแทนที่โค้ดนี้ด้วยการใช้งานโมเดลที่เหมาะสม
    image_data = {
        'filename': filepath,
        'description': 'Data prepared for model'
    }
    return image_data

def random_emotion():
    return random.choice(['positive', 'neutral', 'negative'])

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        language = request.form.get('language', 'english').lower()

        # เตรียมข้อมูลสำหรับโมเดล
        image_data = prepare_image_for_model(filepath)

        # ใช้ random_emotion แทนในระหว่างการพัฒนา
        emotion = random_emotion()

        music_path = os.path.join(MUSIC_FOLDER, language, emotion, 'mp3')
        cover_path = os.path.join(MUSIC_FOLDER, language, emotion, 'png')
        description_path = os.path.join(MUSIC_FOLDER, language, emotion, 'description')

        if not os.path.exists(music_path) or not os.listdir(music_path):
            return jsonify({'error': 'No music available for this emotion'}), 500
        if not os.path.exists(cover_path):
            return jsonify({'error': 'No cover images available for this emotion'}), 500

        selected_song = random.choice(os.listdir(music_path))
        song_name = os.path.splitext(selected_song)[0]
        cover_image = f"{song_name}.png"
        cover_image_path = os.path.join(cover_path, cover_image)

        if not os.path.exists(cover_image_path):
            return jsonify({'error': f'Cover image for {song_name} not found'}), 500

        description_file_path = os.path.join(description_path, f"{song_name}.json")
        if not os.path.exists(description_file_path):
            return jsonify({'error': 'Description file not found'}), 500

        with open(description_file_path, 'r') as f:
            song_details = json.load(f)

        song_url = url_for('get_file', folder='mp3', filename=selected_song, emotion=emotion, language=language, _external=True)
        cover_url = url_for('get_file', folder='png', filename=cover_image, emotion=emotion, language=language, _external=True)

        return jsonify({
            'id': song_details.get('id', ''),
            'emotion': emotion,
            'song_url': song_url,
            'cover_url': cover_url,
            'name': song_details.get('name', song_name),
            'description': song_details.get('description', ''),
            'links': {
                'youtube': song_details.get('youtube', ''),
                'spotify': song_details.get('spotify', '')
            },
            'rating': song_details.get('rating', 0),
            'total_ratings': song_details.get('total_ratings', 0),
            'language': language
        })

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/new-song', methods=['POST'])
def new_song():
    data = request.json
    if not data or 'id' not in data or 'emotion' not in data or 'language' not in data:
        return jsonify({'error': 'Missing required fields: id, emotion, and language are required'}), 400

    emotion = data['emotion']
    language = data['language']
    music_path = os.path.join(MUSIC_FOLDER, language, emotion, 'mp3')
    description_path = os.path.join(MUSIC_FOLDER, language, emotion, 'description')

    if not os.path.exists(music_path) or not os.listdir(music_path):
        return jsonify({'error': 'No music available for this emotion and language'}), 500

    available_songs = [song for song in os.listdir(music_path) if song != f"song{data['id']}.mp3"]
    if not available_songs:
        return jsonify({'error': 'No new songs available for this emotion and language'}), 500

    selected_song = random.choice(available_songs)
    song_name = os.path.splitext(selected_song)[0]

    description_file_path = os.path.join(description_path, f"{song_name}.json")
    if not os.path.exists(description_file_path):
        return jsonify({'error': 'Description file not found'}), 500

    with open(description_file_path, 'r') as f:
        song_details = json.load(f)

    song_url = url_for('get_file', folder='mp3', filename=selected_song, emotion=emotion, language=language, _external=True)
    cover_url = url_for('get_file', folder='png', filename=f"{song_name}.png", emotion=emotion, language=language, _external=True)

    return jsonify({
        'id': song_name.split('song')[-1],
        'name': song_details.get('name', song_name),
        'description': song_details.get('description', ''),
        'links': {
            'youtube': song_details.get('youtube', ''),
            'spotify': song_details.get('spotify', '')
        },
        'rating': song_details.get('rating', 0),
        'total_ratings': song_details.get('total_ratings', 0),
        'song_url': song_url,
        'cover_url': cover_url,
        'language': language,
        'emotion': emotion
    })

@app.route('/rate', methods=['POST'])
def rate_song():
    data = request.json
    song_id = data.get('id')
    new_rating = data.get('rating')
    language = data.get('language')
    emotion = data.get('emotion')

    if not song_id or not new_rating or not language or not emotion:
        return jsonify({'error': 'Missing required fields: id, rating, language, emotion are required'}), 400

    description_path = os.path.join(MUSIC_FOLDER, language, emotion, 'description')
    description_file = next((f for f in os.listdir(description_path) if f"song{song_id}.json" in f), None)

    if not description_file:
        return jsonify({'error': 'Song description file not found'}), 404

    description_file_path = os.path.join(description_path, description_file)
    with open(description_file_path, 'r') as f:
        song_details = json.load(f)

    current_rating = song_details.get('rating', 0)
    total_ratings = song_details.get('total_ratings', 0)

    new_total_ratings = total_ratings + 1
    updated_rating = ((current_rating * total_ratings) + new_rating) / new_total_ratings

    song_details['rating'] = updated_rating
    song_details['total_ratings'] = new_total_ratings

    with open(description_file_path, 'w') as f:
        json.dump(song_details, f, indent=4)

    return jsonify({
        'message': 'Rating updated',
        'new_rating': updated_rating,
        'total_ratings': new_total_ratings
    })

@app.route('/file/<language>/<emotion>/<folder>/<filename>', methods=['GET'])
def get_file(language, emotion, folder, filename):
    folder_path = os.path.join(MUSIC_FOLDER, language, emotion, folder)
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        mimetype = 'audio/mpeg' if folder == 'mp3' else 'image/png'
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)

    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
