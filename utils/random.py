from random import randint

def is_random_proc(chance: int=50) -> bool:
    '''
    min chance value = 0
    max chance value = 100
    :param chance:
    :return:
    '''
    return randint(0, 99) < chance