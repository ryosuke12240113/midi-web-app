from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import pandas as pd
from mido import MidiFile, MidiTrack, Message
from werkzeug.utils import secure_filename
from flask_cors import CORS  
from midi_utils import parse_midi_data

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
MIDI_OUTPUT_FOLDER = 'midi_outputs'  # MIDIファイルの出力フォルダを設定
ALLOWED_EXTENSIONS = {'csv'}
 # MIDIファイルの拡張子を許可

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MIDI_OUTPUT_FOLDER'] = MIDI_OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_midi_file(notes, output_path):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    for note in notes:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=480))

    mid.save(output_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 'file' 変数が request.files から取得されているか確認する
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']  # ここで 'file' 変数を定義
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # MIDI データの解析
            music_sequence = parse_midi_data(file_path)  # この関数は MIDI データを解析して music_sequence を生成する

            # MIDI ファイルの生成
            midi_output_path = os.path.join(app.config['MIDI_OUTPUT_FOLDER'], 'output_midi.mid')
            create_midi_file(music_sequence, midi_output_path)

            # MIDIファイルのダウンロードリンクを提供
            return f'File uploaded successfully. <a href="/uploads/{os.path.basename(midi_output_path)}">Download MIDI file</a>'

    # GETリクエストの処理
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # アップロードフォルダがなければ作成
    os.makedirs(MIDI_OUTPUT_FOLDER, exist_ok=True)  # MIDI出力フォルダがなければ作成
    app.run(host='127.0.0.1', port=5000, debug=True)