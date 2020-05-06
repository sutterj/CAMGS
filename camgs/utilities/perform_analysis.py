from music21 import analysis, voiceLeading

analyzer = analysis.discrete.Ambitus()


def check_range(note_stream):
    print(analyzer.getSolution(note_stream))


def check_countour(note_stream):
    print(voiceLeading.NNoteLinearSegment(note_stream).melodicIntervals)


def check_key(note_stream):
    print(note_stream.analyze('key'))
    print(note_stream.analyze('key').correlationCoefficient)
