#!/usr/bin/python3

import sys
from math import ceil
from pydub.pydub import AudioSegment

from utils import decode_raw_data


def modify_sample(src, val, claster_size, sample_size):
    src_bin = bin(src)
    src_bin_prefix = src_bin[0:src_bin.find('b') + 1]
    src_bin_body = src_bin[src_bin.find('b'):]
    val_bin = bin(val)[2:]
    while len(src_bin_body) < sample_size:
        src_bin_body = '0' + src_bin_body
    src_bin_body = src_bin_body[0:len(src_bin_body) - 4 - 1] + val_bin
    return int(src_bin_prefix + src_bin_body, 2)
    

class LSBHeader:
    extra_bits = 0
    claster_size = 0
    clasters_number = 0

    EXTRA_BITS_FIELD_SIZE = 16
    CLASTER_SIZE_FIELD_SIZE = 16
    CLASTERS_NUMBER_FIELD_SIZE = 16
    HEADER_SIZE = EXTRA_BITS_FIELD_SIZE + CLASTER_SIZE_FIELD_SIZE + CLASTERS_NUMBER_FIELD_SIZE

    def __init__(self, extra_bits=0, claster_size=0, clasters_number=0):
        self.extra_bits = extra_bits
        self.claster_size = claster_size
        self.clasters_number = clasters_number

    def sign(self, samples):
        pass

    def extract_from(self, data):
        pass


# cuts array into numbers <2^claster_size from source string
def cut_message(msg, claster_size=4):
    msg_stream = bin(int.from_bytes(msg.encode(), 'big'))[2:]
    clasters_number = ceil(len(msg_stream) / claster_size)
    clasters = []
    for current_claster in range(clasters_number):
        clasters.append(msg_stream[ current_claster * claster_size : (current_claster + 1) * claster_size ])
    extra_bits = clasters_number * claster_size - len(msg_stream)
    clasters[clasters_number - 1] += '0' * (clasters_number * claster_size - len(msg_stream) )
    result_header = LSBHeader(extra_bits=extra_bits, claster_size=claster_size, clasters_number=clasters_number)
    return clasters, result_header


def insert_message(data, msg_clasters, start_from=0):
    pass

def encode(samples, message, raw_width=16, claster_size=4):
    clasters, result_header = cut_message(message, claster_size=claster_size)
    result_header.sign(samples)

if __name__ == "__main__":
    cut_message("hello, world")

"""
if __name__ == "__main__":
    if sys.argv[1] not in ["encode", "decode"]:
        exit(1)

    mode = sys.argv[1]

    if mode == "encode":
        msg_file = sys.argv[2]
        src_file = sys.argv[3]
        out_file = sys.argv[4]

        data_to_encode = "" 
        with open(msg_file, "r") as file:
            data_to_encode = file.read()

        sound = AudioSegment.from_file(src_file, format="wav")


        print(decode_raw_data(sound.get_array_of_samples()))
    else:
        pass
"""