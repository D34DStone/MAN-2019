#TEST CASE: 
from LSB import *
from random import randint

r = encode_msg('hello, world! How it going on?', 6)
header = r[1]
msg_clasters = r[0]
samples = [randint(-512, 512) for i in range(100)]
samples_stream = dump_samples(samples, sample_size=16)
samples_stream_1 = insert_message_clasters(samples_stream, msg_clasters, header)
samples_stream_1 = header.sign(samples_stream_1)
samples_1 = parse_samples_stream(samples_stream_1, sample_size=16)

samples_stream_2 = dump_samples(samples_1, sample_size=16)
header_2 = LSBHeader()
header_2.extract_from(samples_stream_2)
msg_clasters_2 = extract_message_clasters(samples_stream_2, header_2)
print(decode_msg_clasters(msg_clasters_2, header_2))