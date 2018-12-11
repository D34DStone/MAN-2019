#!/usr/bin/python3

import sys
from math import ceil
import binascii

from pydub.pydub import AudioSegment

from utils import decode_raw_data

"""
def modify_sample(src, val, claster_size, sample_size):
    src_bin = bin(src)
    src_bin_prefix = src_bin[0:src_bin.find('b') + 1]
    src_bin_body = src_bin[src_bin.find('b') + 1:]
    val_bin_body = bin(val)[2:]
    print(val_bin_body,  ' ', src_bin_body)
    while len(src_bin_body) < sample_size:
        src_bin_body = '0' + src_bin_body
    src_bin_body = src_bin_body[0:len(src_bin_body) - 4 - 1] + val_bin_body
    return int(src_bin_prefix + src_bin_body, 2)
    

def discover_sample(src, claster_size, sample_size):
    src_bin = bin(src)
    src_bin_body = src_bin[src_bin.find('b') + 1:]
    val_bin_body = src_bin_body[-claster_size:]
    return int('0b' + val_bin_body, 2)


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

"""
# const to make all elements positive
POSITIVE_CONST = 2 ** 15


def string_spliter(s, interval):
    return [s[x : x + interval] for x in range (0, len(s) - len(s) % interval, interval)]


def bits2string(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
    
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def to_const_size(val, bits=16, sub_by_pos_const=True):
    val_bin_body = bin(val)[2:]
    if sub_by_pos_const:
        val_bin_body = bin(val + POSITIVE_CONST)[2:]
    return '0' * (bits - len(val_bin_body)) + val_bin_body

class LSBHeader:
    EXTRA_BITS_SIZE = 16
    CLASTER_SIZE_SIZE = 16
    CLASTER_NUMBER_SIZE = 16
    SAMPLE_SIZE_SIZE = 16
    LSB_HEADER_SIZE = EXTRA_BITS_SIZE + CLASTER_SIZE_SIZE + CLASTER_NUMBER_SIZE + SAMPLE_SIZE_SIZE

    extra_bits = None
    clasters_number = None
    claster_size = None
    sample_size = None

    def sign(self, data_stream):       
        data_stream_arr = list(data_stream)
        extra_bits = to_const_size(self.extra_bits, self.EXTRA_BITS_SIZE)
        claster_number = to_const_size(self.clasters_number, self.CLASTER_NUMBER_SIZE)
        claster_size = to_const_size(self.claster_size, self.CLASTER_SIZE_SIZE)
        sample_size = to_const_size(self.sample_size, self.SAMPLE_SIZE_SIZE)
        for i in range(self.EXTRA_BITS_SIZE):
            data_stream_arr[i] = extra_bits[i]
        for i in range(self.CLASTER_NUMBER_SIZE):
            data_stream_arr[i + self.EXTRA_BITS_SIZE] = claster_number[i]
        for i in range(self.CLASTER_SIZE_SIZE):
            data_stream_arr[i + self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE] = claster_size[i]
        for i in range(self.SAMPLE_SIZE_SIZE):
            data_stream_arr[i + self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE + self.CLASTER_SIZE_SIZE] = sample_size[i]
        return ''.join(data_stream_arr)
        

    def extract_from(self, data_stream):
        self.extra_bits = int('0b' + data_stream[0:self.EXTRA_BITS_SIZE], 2) - POSITIVE_CONST
        self.clasters_number = int('0b' + data_stream[self.EXTRA_BITS_SIZE:self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE], 2) - POSITIVE_CONST
        self.claster_size = int('0b' + data_stream[self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE:self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE + self.CLASTER_SIZE_SIZE], 2) - POSITIVE_CONST
        self.sample_size = int('0b' + data_stream[self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE + self.CLASTER_SIZE_SIZE:self.LSB_HEADER_SIZE], 2) - POSITIVE_CONST
        #print("DUMPING: {}, {}, {}, {}".format(data_stream[0:self.EXTRA_BITS_SIZE], data_stream[self.EXTRA_BITS_SIZE:self.EXTRA_BITS_SIZE + self.CLASTER_NUMBER_SIZE], 0, 0))

def insert_message_clasters(samples_stream, msg_clasters, header, sample_size = 16):
    samples_stream_arr = list(samples_stream)
    for i in range(len(msg_clasters)):
        current_claster = msg_clasters[i]
        for j in range (header.claster_size):
            samples_stream_arr[header.LSB_HEADER_SIZE + sample_size * (i + 1) - header.claster_size + j + 1] = current_claster[j]
    return ''.join(samples_stream_arr)


def extract_message_clasters(samples_stream, header, sample_size=16):
    msg_clasters = []
    for i in range(header.clasters_number):
        current_claster = ''
        for j in range (header.claster_size):
            current_claster += samples_stream[header.LSB_HEADER_SIZE + sample_size * (i + 1) - header.claster_size + j + 1]
        msg_clasters.append(current_claster)
    return msg_clasters


def encode_message_to_clasters(msg, sample_size=16, claster_size=4):
    pass

def dump_samples(samples, sample_size):
    def dump_int(val):
        val_bin = bin(val)
        val_bin_body = val_bin[2:]
        return '0' * (sample_size - len(val_bin_body)) + val_bin_body
    return ''.join(list(map(
        lambda val:
            dump_int(val + POSITIVE_CONST),
        samples
    )))


def parse_samples_stream(samples, sample_size):
    return list(map(
        lambda s:
            int('0b' + s, 2) - POSITIVE_CONST,
        string_spliter(samples, sample_size)
    ))


def encode_msg(msg, claster_size=4):
    msg_stream = text_to_bits(msg)
    msg_clasters = string_spliter(msg_stream, claster_size)
    extra_bits = 0
    if len(msg_stream) > len(msg_clasters) * claster_size:
        bits_delta = len(msg_stream) - len(msg_clasters) * claster_size
        extra_bits = claster_size - bits_delta
        extra_claster = ''
        for i in range(bits_delta):
            extra_claster += msg_stream[len(msg_clasters) * claster_size + i]
        extra_claster += '0' * extra_bits
        msg_clasters.append(extra_claster)
    header = LSBHeader()
    header.extra_bits = extra_bits
    header.claster_size = claster_size
    header.clasters_number = len(msg_clasters)
    header.sample_size = 16
    return msg_clasters, header


def decode_msg_clasters(msg_clasters, header):
    msg = ''.join(msg_clasters)
    if header.extra_bits != 0:
        msg = msg[:-header.extra_bits]
    return text_from_bits(msg)


if __name__ == "__main__":
    pass

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