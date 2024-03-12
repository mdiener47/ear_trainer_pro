from note import NotePair

all_notes = []


def set_all_notes(li):
    global all_notes
    all_notes = li


class Scale:
    def __init__(self, root, quality, interval_list):
        self.root = root
        self.quality = quality
        self.interval_list = interval_list
        self.full_name = f'{root.name} {quality}'
        self.notes, self.triad = Scale.get_notes_triad(root, interval_list)

    @staticmethod
    def get_notes_triad(root, interval_list):
        notes = []
        triad = []
        current_note = root
        notes.append(current_note)
        for interval in interval_list:
            pair = NotePair.from_note1_interval_is_asc(current_note, interval)
            notes.append(pair.note2)
            current_note = pair.note2

        # initialize root triad for listening context
        triad.append(notes[0])
        triad.append(notes[2])
        triad.append(notes[4])

        # add notes from other octaves
        for note1 in all_notes:
            is_unique = True
            is_in_scale = False
            for note2 in notes:
                # we want to add notes that match the name without octave of a note in the scale,
                # but not duplicate notes that have the same octave and name as another note (full_name includes octave)
                if note1.full_name == note2.full_name:
                    is_unique = False
                if note1.name == note2.name:
                    is_in_scale = True
            if is_unique and is_in_scale:
                notes.append(note1)
        return notes, triad
