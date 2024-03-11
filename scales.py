from note import Note
from scale import Scale

# dictionary of interval structures for all modes,
intervals = {'Melodic Minor': {
    'Melodic Minor': ['M2', 'm2', 'M2', 'M2', 'M2', 'M2', 'm2']
}, 'Major': {
    'Major': ['M2', 'M2', 'm2', 'M2', 'M2', 'M2', 'm2']
}, 'Harmonic Minor': {
    'Harmonic Minor': ['M2', 'm2', 'M2', 'M2', 'm2', 'm3', 'm2']
}}

# dictionary of mode names for base scales
mode_names = {
    'Melodic Minor': ['Dorian b9', 'Lydian Augmented', 'Lydian Dominant', 'Mixolydian b6', 'Aeolian b5', 'Super Locrian'],
    'Major': ['Dorian', 'Phrygian', 'Lydian', 'Dominant', 'Aeolian', 'Locrian'],
    'Harmonic Minor': ['Locrian Natural 6', 'Ionian #5', 'Dorian #11',
                       'Phrygian Dominant', 'Lydian #9', 'Super Locrian bb7']
}


def add_modes(obj, parent_intervals, modes_li):
    index = 1  # keep track of starting note in parent scale for new mode, start at 1 because root mode is pre-defined
    for mode in modes_li:
        obj[mode] = parent_intervals[index:] + parent_intervals[:index]
        index += 1


for key in intervals:
    obj = intervals[key]
    parent_name = list(obj.keys())[0]
    add_modes(obj, obj[parent_name], mode_names[parent_name])

scales = {}

# convert lists of intervals to scale objects and populate scales dictionary
for scale_category_name in intervals:
    scale_category_intervals_obj = intervals[scale_category_name]
    scale_category_obj = {}
    for scale_name in scale_category_intervals_obj:
        interval_li = scale_category_intervals_obj[scale_name]
        scale_mode_obj = {}
        for name in Note.notes:
            root = Note(name + '3')  # use notes from octave 3 as roots
            scale = Scale(root, scale_name, interval_li)
            scale_mode_obj[name] = scale  # index third-layer by note name

        scale_category_obj[scale_name] = scale_mode_obj
    scales[scale_category_name] = scale_category_obj
