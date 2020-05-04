import csv
import music21 as m21

note_stream = m21.stream.Stream()

# read and rename composition data file
composition_file = open('../user_data/composition1.csv', mode='r')
composition_reader = csv.DictReader(composition_file)

for row in composition_reader:
    composition_meter = row['bar_beat'] + '/' + row['base_duration']
note_stream.timeSignature = m21.meter.TimeSignature(composition_meter)
composition_file.close()


# read and rename notes data file
note_file = open('../user_data/notes1.csv', mode='r')
note_reader = csv.DictReader(note_file)

for row in note_reader:
    note_pitch_octave = row['pitch']
    note_duration = row['duration']
    if note_pitch_octave == 'rest':
        note = m21.note.Rest(quarterLength=float(note_duration))
    else:
        note = m21.note.Note(
            note_pitch_octave, quarterLength=float(note_duration))
    note_stream.append(note)

note_file.close()


note_stream.show()
