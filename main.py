import argparse

from LSB import lsb_encode, lsb_decode
from pydub.pydub import AudioSegment
from copy import deepcopy
from array import array

parser = argparse.ArgumentParser()
parser.add_argument('algorithm', type=str)
parser.add_argument('--src', type=str)
parser.add_argument('--out', type=str)
parser.add_argument('--inp', type=str)
args = parser.parse_args()

if args.algorithm == "encode":
    msg = ""
    with open(args.inp, "r") as f:
        msg = f.read()
    src_song = AudioSegment.from_wav(args.src)
    samples = list(src_song.get_array_of_samples())
    new_samples = lsb_encode(samples, msg, claster_size=4, sample_size=2*8)
    out_song = src_song._spawn(array('h', new_samples))
    out_song.export(args.out, format="wav")


if args.algorithm == "decode":
    msg = ""
    src_song = AudioSegment.from_wav(args.src)
    samples = list(src_song.get_array_of_samples())
    msg = lsb_decode(samples)
    with open(args.out, "w") as f:
        f.write(msg)

if args.algorithm == "debug":
    src_song = AudioSegment.from_wav(args.src)
    samples = list(src_song.get_array_of_samples())
    print(samples)