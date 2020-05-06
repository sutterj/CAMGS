from build_csv import build_csv
from parse_data import parse_data
from perform_analysis import check_range, check_countour, check_key
from music21 import stream, midi, musicxml

composition_id = '2'

build_csv(composition_id)

note_stream = stream.Stream()

parse_data(note_stream, composition_id)

check_range(note_stream)
check_countour(note_stream)
check_key(note_stream)

midi_file = midi.translate.streamToMidiFile(note_stream)
midi_file.open('../user_data/midi' + composition_id + '.midi', 'wb')
midi_file.write()
midi_file.close()

exporter = musicxml.m21ToXml.GeneralObjectExporter(note_stream)
xml_bytes = exporter.parse()
xml_string = xml_bytes.decode('utf-8')
xml_file = open('../user_data/xml' + composition_id + '.xml', 'w')
xml_file.write(xml_string)
xml_file.close()
