import argparse

from LSB import *
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

    msg_clasters, header = encode_msg(msg, claster_size=6)
    samples = src_song.get_array_of_samples()
    samples_stream = dump_samples(samples, 8 * src_song.sample_width)


    new_samples_stream = insert_message_clasters(samples_stream, msg_clasters, header)

    new_samples_stream = header.sign(new_samples_stream)

    new_samples = parse_samples_stream(new_samples_stream, sample_size=16)

    out_song = src_song._spawn(array('h', new_samples))
    out_song.export(args.out, format="wav")


if args.algorithm == "decode":
    msg = ""
    header = LSBHeader()
    src_song = AudioSegment.from_wav(args.src)
    samples = src_song.get_array_of_samples()
    samples_stream = dump_samples(samples, 8 * src_song.sample_width)
    header.extract_from(samples_stream)
    msg_clasters = extract_message_clasters(samples_stream, header, sample_size=16)
    msg = decode_msg_clasters(msg_clasters, header)
    print(msg)
    #print(header.claster_size, ' ', header.clasters_number)