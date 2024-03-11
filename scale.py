from note import NotePair


class Scale:
    def __init__(self, root, quality, interval_list):
        self.root = root
        self.quality = quality
        self.interval_list = interval_list
        self.full_name = f'{root.name} {quality}'
        self.notes = Scale.get_notes(root, interval_list)

    @staticmethod
    def get_notes(root, interval_list):
        notes = []
        current_note = root
        notes.append(current_note)
        for interval in interval_list:
            pair = NotePair.from_note1_interval_is_asc(current_note, interval)
            notes.append(pair.note2)
            current_note = pair.note2
        return notes
