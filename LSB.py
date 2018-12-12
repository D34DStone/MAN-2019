from math import ceil
from copy import deepcopy
from random import randint
import binascii

class Header:
    sample_size = 16
    claster_size = 4
    extra_bits = 0
    clasters_number = 0


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


def modify_sample(src, val, header):
    src_bin = bin(src)
    src_bin_prefix = src_bin[0:src_bin.find('b') + 1]
    src_bin_body = src_bin[src_bin.find('b') + 1:]
    val_bin_body = bin(val)[2:]
    while len(src_bin_body) < header.sample_size:
        src_bin_body = '0' + src_bin_body
    while len(val_bin_body) < header.claster_size:
        val_bin_body = '0' + val_bin_body
    src_bin_body = src_bin_body[:-header.claster_size] + val_bin_body
    return int(src_bin_prefix + src_bin_body, 2)
    

def discover_sample(src, header):
    src_bin = bin(src)
    src_bin_body = src_bin[src_bin.find('b') + 1:]
    val_bin_body = src_bin_body[-header.claster_size:]
    return int('0b' + val_bin_body, 2)


def text_to_clasters(text, header):
    msg_stream = text_to_bits(text)
    clasters_number = ceil(len(msg_stream) / header.claster_size)
    clasters = []
    for current_claster in range(clasters_number):
        clasters.append(msg_stream[ current_claster * header.claster_size : (current_claster + 1) * header.claster_size ])
    extra_bits = clasters_number * header.claster_size - len(msg_stream)
    clasters[clasters_number - 1] += '0' * extra_bits
    clasters = list(map(
        lambda claster:
            int('0b' + claster, 2),
        clasters
    ))
    header.extra_bits = extra_bits
    header.clasters_number = clasters_number
    return clasters


def clasters_to_text(clasters, headers):
    clasters_bin  = (list(map(
        lambda claster:
            '0' * (headers.claster_size - len(bin(claster)[2:])) + bin(claster)[2:],
        clasters
    )))
    data_stream = ''.join(clasters_bin)
    if headers.extra_bits:
        data_stream = data_stream[:-headers.extra_bits]
    return text_from_bits(data_stream)


def encode(samples, clasters, header):
    new_samples = deepcopy(samples)
    new_samples[0] = header.sample_size
    new_samples[1] = header.claster_size
    new_samples[2] = header.extra_bits
    new_samples[3] = header.clasters_number
    for i in range(len(clasters)):
        new_samples[i + 4] = modify_sample(new_samples[i + 4], clasters[i], header)
    return new_samples


def decode(samples):
    header = Header()
    header.sample_size = samples[0]
    header.claster_size = samples[1]
    header.extra_bits = samples[2]
    header.clasters_number = samples[3]
    clasters = []
    for i in range(header.clasters_number):
        clasters.append(discover_sample(samples[4 + i], header))
    return clasters_to_text(clasters, header)


def lsb_encode(samples, msg, claster_size=4, sample_size=16):
    header = Header()
    header.claster_size = claster_size
    header.sample_size = sample_size
    msg_clasters = text_to_clasters(msg, header)
    new_samples = encode(samples, msg_clasters, header)
    return new_samples


def lsb_decode(samples):
    msg = decode(samples)
    return msg


if __name__ == "__main__":
    header = Header()
    header.sample_size = 16
    header.claster_size = 1

    samples = [randint(-128, 128) for i in range(0, 500)]

    text = "Hello, World. Nice weather today :D"
    clasters = text_to_clasters(text, header)
    new_samples = encode(samples, clasters, header)

