import random


def get_fake_ip(prefix=(115, 42)):
    digit_list = list(prefix)
    for i in range(4 - len(prefix)):
        digit_list.append(random.randint(2, 255))
    return '.'.join(map(str, digit_list))
