fmt_dict = {"sep": None}


def message_start_index(datastream, marker_length):
    for i, chars in enumerate(zip(*(datastream[j:] for j in range(marker_length)))):
        if len(set(chars)) == marker_length:
            return i + marker_length


def solve(data):
    return message_start_index(data, 4), message_start_index(data, 14)
