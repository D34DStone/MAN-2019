from pydub.pydub.utils import get_array_type
import array

def decode_raw_data(data, raw_size=16):
    array_type=get_array_type(raw_size)
    return array.array(array_type, data)