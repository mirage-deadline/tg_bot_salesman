import enum


class States(enum.Enum):
    
    DIALOG_START = 0
    CHOOSE_SIZE = 1
    CHOOSE_PAYMENT = 2
    MAKE_SURE = 3
    DONE_ORDER = 4
    CANCEL = 5