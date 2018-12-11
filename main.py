import argparse

from LSB2 import *
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
    header = Header()
    header.claster_size = 4
    header.sample_size = 16
    msg = ""
    with open(args.inp, "r") as f:
        msg = f.read()
    src_song = AudioSegment.from_wav(args.src)
    msg_clasters = text_to_clasters(msg, header)
    samples = list(src_song.get_array_of_samples())
    new_samples = encode(samples, msg_clasters, header)
    out_song = src_song._spawn(array('h', new_samples))
    out_song.export(args.out, format="wav")


if args.algorithm == "decode":
    msg = ""
    header = Header()
    src_song = AudioSegment.from_wav(args.src)
    samples = list(src_song.get_array_of_samples())
    msg = decode(samples)
    with open(args.out, "w") as f:
        f.write(msg)
