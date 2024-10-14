import os
import random
import json
from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
from applyModel import apply

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
MUSIC_FOLDER = './music/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_emotion():
    return random.choice(['positive', 'neutral', 'negative'])

def apply_model():
    return apply()
    # return random _emotion()

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

        language = request.form.get('language', 'non-thai').lower()
        emotion = apply_model()

        emotion_folder = os.path.join(MUSIC_FOLDER, language, emotion)
        if not os.path.exists(emotion_folder) or not os.listdir(emotion_folder):
            return jsonify({'error': 'No music available for this emotion'}), 500

        available_songs = [song for song in os.listdir(emotion_folder) if os.path.isdir(os.path.join(emotion_folder, song))]
        selected_song = random.choice(available_songs)

        song_folder = os.path.join(emotion_folder, selected_song)
        song_file_path = os.path.join(song_folder, f'{selected_song}.mp3')
        cover_file_path = os.path.join(song_folder, f'{selected_song}.png')
        description_file_path = os.path.join(song_folder, f'{selected_song}.json')

        if not all(os.path.exists(path) for path in [song_file_path, cover_file_path, description_file_path]):
            return jsonify({'error': 'One or more files are missing for the selected song'}), 500

        with open(description_file_path, 'r', encoding='utf-8') as f:
            song_details = json.load(f)

        song_url = url_for('get_file', language=language, emotion=emotion, folder=selected_song, filename=f'{selected_song}.mp3', _external=True)
        cover_url = url_for('get_file', language=language, emotion=emotion, folder=selected_song, filename=f'{selected_song}.png', _external=True)

        return jsonify({
            'id': selected_song,
            'emotion': emotion,
            'song_url': song_url,
            'cover_url': cover_url,
            'name': song_details.get('name', selected_song),
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
    emotion_folder = os.path.join(MUSIC_FOLDER, language, emotion)

    if not os.path.exists(emotion_folder) or not os.listdir(emotion_folder):
        return jsonify({'error': 'No music available for this emotion and language'}), 500

    available_songs = [song for song in os.listdir(emotion_folder) if os.path.isdir(os.path.join(emotion_folder, song)) and song != data['id']]
    if not available_songs:
        return jsonify({'error': 'No new songs available for this emotion and language'}), 500

    selected_song = random.choice(available_songs)
    song_folder = os.path.join(emotion_folder, selected_song)
    song_file_path = os.path.join(song_folder, f'{selected_song}.mp3')
    cover_file_path = os.path.join(song_folder, f'{selected_song}.png')
    description_file_path = os.path.join(song_folder, f'{selected_song}.json')

    if not all(os.path.exists(path) for path in [song_file_path, cover_file_path, description_file_path]):
        return jsonify({'error': 'One or more files are missing for the selected song'}), 500

    with open(description_file_path, 'r', encoding='utf-8') as f:
        song_details = json.load(f)

    song_url = url_for('get_file', language=language, emotion=emotion, folder=selected_song, filename=f'{selected_song}.mp3', _external=True)
    cover_url = url_for('get_file', language=language, emotion=emotion, folder=selected_song, filename=f'{selected_song}.png', _external=True)

    return jsonify({
        'id': selected_song,
        'name': song_details.get('name', selected_song),
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

    try:
        new_rating = int(new_rating)
    except ValueError:
        return jsonify({'error': 'Rating must be a number'}), 400

    song_folder = os.path.join(MUSIC_FOLDER, language, emotion, song_id)
    description_file_path = os.path.join(song_folder, f'{song_id}.json')

    if not os.path.exists(description_file_path):
        return jsonify({'error': 'Song description file not found'}), 404

    with open(description_file_path, 'r', encoding='utf-8') as f:
        song_details = json.load(f)

    current_rating = song_details.get('rating', 0)
    total_ratings = song_details.get('total_ratings', 0)

    new_total_ratings = total_ratings + 1
    updated_rating = ((current_rating * total_ratings) + new_rating) / new_total_ratings

    song_details['rating'] = updated_rating
    song_details['total_ratings'] = new_total_ratings

    with open(description_file_path, 'w', encoding='utf-8') as f:
        json.dump(song_details, f, indent=4)

    return jsonify({
        'message': 'Rating updated',
        'new_rating': updated_rating,
        'total_ratings': new_total_ratings
    })

@app.route('/file/<language>/<emotion>/<folder>/<filename>', methods=['GET'])
def get_file(language, emotion, folder, filename):
    file_path = os.path.join(MUSIC_FOLDER, language, emotion, folder, filename)

    if os.path.exists(file_path):
        mimetype = 'audio/mpeg' if filename.endswith('.mp3') else 'image/png'
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)

    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
