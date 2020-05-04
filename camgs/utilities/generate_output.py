from build_csv import build_csv
from parse_data import parse_data
from music21 import stream

build_csv('1')

note_stream = stream.Stream()

parse_data(note_stream, '1')

note_stream.show()
