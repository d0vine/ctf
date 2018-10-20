import midi
import string
import sys

A4 = 440
C0 = A4*pow(2, -4.75)
name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
def note_from_freq(freq):
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return name[n] + str(octave)

def filter_notes(pattern_sub):
    return filter(lambda el: type(el) is midi.events.NoteOnEvent, pattern_sub)

def check_valid(pattern_sub):
    notes = filter_notes(pattern_sub)
    for n in notes:
        try:
            print mapping[n.pitch][:-2]
            if mapping[n.pitch][:-2] not in acceptable:
                return False
        except KeyError:
            return False
    return True

mapping = {key: value for key, value in [(getattr(midi, c), c) for c in dir(midi) if c.lower()[0] in string.ascii_lowercase and c[-1] in string.digits]}
task_map = {'A': 0, 'B': 1, 'Cs': 2, 'Ds': 3, 'F': 4, 'G': 5}
acceptable = ['A', 'B', 'Cs', 'Ds', 'F', 'G']

pattern = midi.read_midifile('bwv2342.mid')
print '[+] MIDI file loaded with {} tracks'.format(len(pattern))
# for i in range(0, len(pattern)):
TRACK_ID = int(sys.argv[1])

notes = filter_notes(pattern[TRACK_ID])
lines = []

print '[+] {} notes from track {} filtered out'.format(len(notes), TRACK_ID)

if not check_valid(pattern[TRACK_ID]):
    print '[-] Uh-oh, this looks invalid! :('
    sys.exit(1)

print '[+] All good, let\'s rock!'

for note in notes:
    note_name = mapping[note.pitch]
    print note_name
    offset = int(note_name[-1]) if note_name[:-2] in ('A', 'B') else int(note_name[-1])-1
    ss = '!' * int(task_map[note_name[:-2]]+offset)
    print 'ss: {}'.format(ss)
    lines.append(ss)

from pwn import *

r = remote('bwv2342.ctf.hackover.de', 1337)

for line in lines:
    print 'Sending: \n'.format(line)
    r.send('{}\n'.format(line))

print r.recv(4096)
