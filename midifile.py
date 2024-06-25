import mido

# Create a new MIDI file with a single track
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

# Set the tempo (optional)
track.append(mido.MetaMessage('set_tempo', tempo=500000))

# Function to calculate note duration in ticks (adjust as needed)
def calculate_note_duration(velocity):
    # Example: 480 ticks for every velocity value
    return velocity * 480

# Iterate through all notes and alternate velocities
for notenum in range(0, 128):  # Note numbers 0 to 127
    for vel in range(0, 127, 2):  # Velocities 0, 2, 4, ..., 126
        # Note on event
        track.append(mido.Message('note_on', note=notenum, velocity=vel, time=0))
        
        # Insert a delay for reverb tail or sustain effect
        note_duration = calculate_note_duration(vel)
        track.append(mido.Message('note_off', note=notenum, velocity=vel, time=note_duration))

# Insert a measure of silence (4 beats in 4/4 time at standard tempo)
silence_ticks = 4 * 480  # 4 beats * 480 ticks per beat (adjust tempo if necessary)
track.append(mido.Message('note_on', note=0, velocity=0, time=silence_ticks))  # Dummy note with velocity 0
track.append(mido.Message('note_off', note=0, velocity=0, time=0))  # Release the dummy note

# Save the MIDI file
mid.save('every_other_velocity_with_reverb_and_silence.mid')

