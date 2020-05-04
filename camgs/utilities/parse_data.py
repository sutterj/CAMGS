import csv
from music21 import meter, tempo, clef, note, pitch


def parse_data(note_stream, value_id):
    composition_file = open('../user_data/composition'
                            + value_id + '.csv', mode='r')
    composition_reader = csv.DictReader(composition_file)

    for row in composition_reader:
        composition_meter = row['bar_beat'] + '/' + row['base_duration']
        switch_enharmonic = row['enharmonic']
        tempo_value = row['tempo']
    note_stream.timeSignature = meter.TimeSignature(composition_meter)
    metronome_mark = tempo.MetronomeMark(number=int(tempo_value))
    use_clef = clef.TrebleClef()
    note_stream.append([metronome_mark, use_clef])

    composition_file.close()

    note_file = open('../user_data/notes' + value_id + '.csv', mode='r')
    note_reader = csv.DictReader(note_file)

    for row in note_reader:
        note_pitch_octave = row['pitch']
        note_duration = row['duration']
        if note_pitch_octave == 'rest':
            note_entry = note.Rest(quarterLength=float(note_duration))
        else:
            pitch_value = pitch.Pitch(note_pitch_octave)
            if switch_enharmonic == 'flat':
                if "#" in pitch_value.name:
                    pitch_value = pitch_value.getHigherEnharmonic()
            note_entry = note.Note(
                pitch_value, quarterLength=float(note_duration))
        note_stream.append(note_entry)

    note_file.close()

    return note_stream
