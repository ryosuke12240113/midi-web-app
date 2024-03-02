# midi_utils.py

from mido import MidiFile

def parse_midi_data(midi_file_path):
    # MIDIファイルを開く
    mid = MidiFile(midi_file_path)

    # 解析されたMIDIデータを保存するためのリスト
    music_sequence = []

    # MIDIメッセージを反復処理する
    for i, track in enumerate(mid.tracks):
        print(f'Track {i}: {track.name}')
        for msg in track:
            if not msg.is_meta and msg.type == 'note_on':
                # ここでノート情報を抽出し、music_sequenceに追加します
                # この例では、ノート番号とベロシティのみを取得しています
                note = msg.note
                velocity = msg.velocity
                music_sequence.append((note, velocity))

    # 解析されたデータを返す
    return music_sequence
