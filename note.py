class Note:
    notes = ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']

    def __init__(self, full_name):
        self.name = ''
        for c in full_name:
            if c.isdigit():
                self.octave = c
            else:
                self.name += c
        self.full_name = full_name

    def __eq__(self, other):
        return (self.name, self.octave) == (other.name, other.octave)

    def __ne__(self, other):
        return (self.name, self.octave) != (other.name, other.octave)

    def __lt__(self, other):
        if self.octave != other.octave:
            return self.octave < other.octave
        else:
            if self.name[0] == other.name[0]:
                # Assuming only flats here!
                return len(self.name) > len(other.name)
            if (self.name >= 'C' and other.name >= 'C') or (self.name < 'C' and other.name < 'C'):
                return self.name < other.name
            else:
                return self.name >= 'C'

    def __gt__(self, other):
        if self.octave != other.octave:
            return self.octave > other.octave
        else:
            if self.name[0] == other.name[0]:
                # Assuming only flats here!
                return len(self.name) < len(other.name)
            if (self.name >= 'C' and other.name >= 'C') or (self.name < 'C' and other.name < 'C'):
                return self.name > other.name
            else:
                return self.name <= 'C'


class NotePair:
    intervals = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'D5', 'P5', 'm6', 'M6', 'm7', 'M7']

    # static block to initialize name interval maps
    name_interval_map_asc = {}
    name_interval_map_desc = {}
    for index1 in range(len(Note.notes)):
        interval_index = 0
        for index2 in range(index1, index1 + len(Note.notes)):
            key = Note.notes[index1] + Note.notes[index2 % len(Note.notes)]
            name_interval_map_asc[key] = intervals[interval_index]
            name_interval_map_desc[key] = intervals[-abs(interval_index)]
            interval_index += 1

    @staticmethod
    def get_interval(note1, note2):
        if note1 < note2:
            return NotePair.name_interval_map_asc[note1.name + note2.name]
        else:
            return NotePair.name_interval_map_desc[note1.name + note2.name]

    @staticmethod
    def get_note2(map, note1, interval, is_asc):
        note2_name = ''
        for key, val in map.items():
            if key[:len(note1.name)] == note1.name and val == interval:
                note2_name = key[len(note1.name):]

        note1_oct = note1.octave

        # Generate interval_semitone mapping
        interval_semitone = dict(zip(NotePair.intervals, range(len(NotePair.intervals))))

        # Generate note_semitone_offsets mapping
        c_index = Note.notes.index('C')  # Find the index of 'C' in the list
        notes_from_c = Note.notes[c_index:] + Note.notes[:c_index]  # Rotate the list
        note_semitone_offsets = dict(zip(notes_from_c, range(len(Note.notes))))

        semitone_diff = interval_semitone[interval]
        semitones_from_c = note_semitone_offsets[note1.name]

        total_semitones = semitones_from_c + semitone_diff if is_asc else semitones_from_c - semitone_diff
        note2_oct = str(total_semitones // 12 + int(note1_oct))

        return Note(note2_name + note2_oct)

    @classmethod
    def from_note1_note2(cls, note1, note2):
        interval = NotePair.get_interval(note1, note2)
        is_asc = note1 < note2
        return cls(note1, note2, interval, is_asc)

    # Generates a NotePair instance by finding a second note based on a first note and an interval
    @classmethod
    def from_note1_interval_is_asc(cls, note1, interval, is_asc=True):
        map = NotePair.name_interval_map_asc if is_asc else NotePair.name_interval_map_desc
        note2 = NotePair.get_note2(map, note1, interval, is_asc)
        return cls(note1, note2, interval, is_asc)

    def __init__(self, note1, note2, interval, is_ascending):
        self.note1 = note1
        self.note2 = note2
        self.interval = interval
        self.is_ascending = is_ascending
