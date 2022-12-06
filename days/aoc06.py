fmt_dict = {"sep": None}


def message_start_index(datastream, marker_length):
    for i in range(0, len(datastream) - marker_length + 1):
        if len(set(datastream[i : i + marker_length])) == marker_length:
            return i + marker_length


def solve(data):
    return message_start_index(data, 4), message_start_index(data, 14)
