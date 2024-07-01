import mido
from mido import MidiFile, MidiTrack, Message

# Configuration
note_length = 480  # Length of each note in ticks (adjust this as needed)
ticks_per_beat = 480  # Standard MIDI resolution
bpm = 120
measure_length = ticks_per_beat * 4  # Number of ticks per measure (4/4 time)

# Create a new MIDI file
midi = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
midi.tracks.append(track)

# Set tempo
tempo = mido.bpm2tempo(bpm)
track.append(mido.MetaMessage('set_tempo', tempo=tempo))

# Generate notes
for note in range(21, 109):  # MIDI notes range from 21 (A0) to 108 (C8)
    for velocity in range(1, 128):  # MIDI velocity ranges from 1 to 127
        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=note_length))
        track.append(Message('note_off', note=note, velocity=0, time=measure_length - note_length))

# Save the MIDI file
midi.save('all_notes_velocities.mid')

