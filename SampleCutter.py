# cut the audio file into equally-spaced parts
# supply the bpm of the file and a fraction to cut the file into chunks

"""
I can figure out the amount of time in, say, a measure of music like

(120 beats/1 minute) * 1 minute / measures

number of measures in a minute... that's an algorithm
bpm * fraction

1 is 18 measures
1/2 is eight measures
1/4 is 4 measures
1/8 is two measures
1/4 is a measure
1/8 is half notes
1/16 is quarter notes
1/32 is eighth notes

... is this better to do with float math?
yeah actually this is better done with samples
aaaaaaaa fuck

number of SAMPLES in a minute... are minutes the best way to do this?
number of samples in a measure?

44100 samples * x seconds   * subdivison of measures (fraction)
1     second    1 measure

to calculate seconds in a measure
       to get number of measures
x beats     *      1/4      *      1 minutes          
1 minute                           60 seconds 

so sample rate * ^ * (fractional component)
"""
from fractions import Fraction
import ffmpeg
import os
import argparse


class cutter:
    # interval, bpm, length, samplerate, fileName, outdir
    def __init__(self, bpm, length, numerator, denominator, fileName, outDir):
        self.bpm = bpm
        # have to figure out how to parse this vv
        self.subdv = Fraction(numerator, denominator)
        self.length = length
        self.fileName = fileName
        self.outDir = outDir
        os.mkdir("./" + self.outDir)

    def run(self):
        lengthOfMeasure = self.bpm * (1/4) / 60
        lengthPerSubdv = lengthOfMeasure * self.subdv
        startTime = 0
        count = 0
        while startTime <= self.length:
            # do your ffmpeg
            outputFile = self.outDir + "/" + self.fileName + "_" + str(count)
            ffmpeg.input(self.fileName, ss=startTime, to=startTime + lengthPerSubdv).output(str(count) + self.fileName).run()
            startTime = startTime + lengthPerSubdv
            print("cutting file with start time " + str(startTime) + " and end time " + str(startTime + lengthPerSubdv) + " to " + outputFile)
            count = count + 1


from pydub import AudioSegment

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut audio/video file into segments based on specified parameters.")
    
    # Define command-line arguments
    parser.add_argument("--bpm", type=int, default=120, help="Beats per minute (default: 120)")
    parser.add_argument("--length", type=int, default=120, help="Total length in seconds (default: 120)")
    parser.add_argument("--numerator", type=int, default=4, help="Numerator of subdivision fraction (default: 4)")
    parser.add_argument("--denominator", type=int, default=1, help="Denominator of subdivision fraction (default: 1)")
    parser.add_argument("--file_name", type=str, default="input.mp4", help="Input file name (default: input.mp4)")
    parser.add_argument("--out_dir", type=str, default="output", help="Output directory (default: output)")
    

    args = parser.parse_args()
    audio = AudioSegment.from_file(args.file_name)
    duration_seconds = len(audio) / 1000.00
    # Parse command-line arguments
    
    # Initialize `Cutter` with command-line arguments
    c = cutter(args.bpm, duration_seconds, args.numerator, args.denominator, args.file_name, args.out_dir)
    
    # Run the cutter
    c.run()
