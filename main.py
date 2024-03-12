import os
from note import Note, NotePair
import scales as sc
import scale as s
import time
import random
import pygame

NUM_NOTES_SCALE_DICTATION = 4

scales = {}
note_filename_map = {}
notes = []
directory = 'piano_notes'

interval_to_scale_tone = {
    'P1': '1',
    'm2': 'b2',
    'M2': '2',
    'm3': 'b3',
    'M3': '3',
    'P4': '4',
    'D5': 'b5',
    'P5': '5',
    'm6': 'b6',
    'M6': '6',
    'm7': 'b7',
    'M7': '7'
}


def fill_data_strucs():
    for filename in os.listdir(directory):
        if filename.startswith('Piano'):
            li = filename.split('.')
            note_name = li[2]
            notes.append(Note(note_name))
            note_filename_map[note_name] = filename

    s.set_all_notes(notes)
    global scales
    scales = sc.init_scales()
    # scale = scales['Melodic Minor']['Melodic Minor']['C']
    # for note in scale.notes:
    #     print(note.full_name)


def play_note(note, sleep_time):
    filename = f'{directory}/{note_filename_map[note.full_name]}'
    note = pygame.mixer.Sound(filename)
    note.play()
    time.sleep(sleep_time)
    note.stop()


def print_pair(note_pair):
    note1 = note_pair.note1
    note2 = note_pair.note2
    print(f'note1: {note1.full_name} note2: {note2.full_name} '
          f'interval: {note_pair.interval} is_asc?: {note_pair.is_ascending}')


def interval_identification_exercise():
    note1 = random.choice(notes)
    note2 = random.choice(notes)
    note_pair = NotePair.from_note1_note2(note1, note2)

    correct_answer = note_pair.interval

    while True:
        while True:
            play_note(note1, 1.5)
            play_note(note2, 1.5)

            user_answer = input("What is the interval? (r to repeat) ")

            if user_answer == 'q':
                return False
            if user_answer == 'p':
                print_pair(note_pair)
            if user_answer != 'r':
                break
        if user_answer[0] == 'p' or user_answer[0] == 'd':
            user_answer = user_answer.upper()
        if user_answer == correct_answer:
            print("Correct!")
            break
        else:
            print(f"Incorrect. The answer is {correct_answer}")
            yn = input("go back? y/n ")
            if yn == 'n':
                break

    return True


def select_nested_dict_element(d, title):
    while True:
        try:
            print(f'{title}: ')
            for i, key in enumerate(d):
                print(f'\t{i + 1}: {key}')
            resp = int(input()) - 1
            keys_li = list(d.keys())
            key_name = keys_li[resp]
            return key_name, d[key_name]
        except (IndexError, ValueError):
            print(f'Invalid {title[:len(title) - 1].lower()} choice, please try again.')


def choose_scale():
    system_name, system = select_nested_dict_element(scales, 'Scale Systems')
    mode_name, mode = select_nested_dict_element(system, 'Modes')

    while True:
        try:
            key_choice = input(f'Select a key for {mode_name} (flats only): ')
            return mode[key_choice]
        except KeyError:
            print('Invalid key choice, please try again.')


def quiz_user(message, correct_answer):
    user_answer = input(message)
    is_quit = False
    play_again = False
    is_correct = False
    if user_answer[0] == 'p' or user_answer[0] == 'd':
        user_answer = user_answer.upper()
    if user_answer == 'q':
        is_quit = True
    elif user_answer == 'r':
        play_again = True
    elif user_answer == correct_answer:
        print("Correct!")
        is_correct = True
    else:
        print(f"Incorrect. Try again. Answer: {correct_answer}")

    return is_quit, play_again, is_correct


# Play the notes which will serve as the prompt for the user.
def play_prompt(scale, note_choices):
    print('Please listen to the following notes to familiarize yourself with the key:')
    for note in scale.triad:
        play_note(note, sleep_time=1.5)
    time.sleep(1.5)
    print(f'Now please answer the following questions based on these {len(note_choices)} notes')
    for note in note_choices:
        play_note(note, sleep_time=1.5)


def scale_dictation_exercise(num_notes):
    scale = choose_scale()
    root_note = scale.notes[0]

    while True:
        # pick random notes from scale.notes and quiz the user
        note_choices = []
        for i in range(num_notes):
            note_choices.append(random.choice(scale.notes))

        play_again = True
        for i in range(num_notes):
            if i > 0:
                while True:
                    if play_again:
                        play_prompt(scale, note_choices)

                    pair = NotePair.from_note1_note2(note_choices[i-1], note_choices[i])
                    message = f'Enter guess for interval between note {i} and note {i + 1} (r to repeat): '
                    is_quit, play_again, is_correct = quiz_user(message, pair.interval)
                    if is_quit:
                        return False
                    if play_again:
                        continue
                    if is_correct:
                        break
                    # else just repeat

            while True:
                if play_again:
                    play_prompt(scale, note_choices)

                # find interval from root note for each scale tone
                pair = NotePair.from_note1_note2(root_note, note_choices[i])

                if not pair.is_ascending:
                    selected_note = Note(pair.note2.full_name)
                    # increment selected note's octave until it is greater than root so that we will have the right
                    # scale tone conversion.
                    while root_note > selected_note:
                        selected_note.octave = str(int(selected_note.octave) + 1)
                    new_pair = NotePair.from_note1_note2(root_note, selected_note)
                    correct_answer = interval_to_scale_tone[new_pair.interval]
                else:
                    correct_answer = interval_to_scale_tone[pair.interval]
                message = f'Enter guess for scale tone {i+1} (r to repeat): '
                is_quit, play_again, is_correct = quiz_user(message, correct_answer)
                if is_quit:
                    return False
                if play_again:
                    continue
                if is_correct:
                    break
                # else just repeat


def main():
    pygame.init()
    pygame.mixer.init()
    fill_data_strucs()
    while True:
        choice = input('\n1: Interval identification \n2: Melodic dictation by scale \nq: Quit\n')
        if choice == '1':
            while True:
                if not interval_identification_exercise():
                    break
        elif choice == '2':
            while True:
                if not scale_dictation_exercise(NUM_NOTES_SCALE_DICTATION):
                    break
        elif choice == 'q':
            break
        else:
            print('invalid choice')


if __name__ == '__main__':
    main()
