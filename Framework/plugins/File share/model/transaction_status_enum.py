from enum import Enum
class TransactionStatus(Enum):
    WAITING = 1
    SENDING = 2
    FINISHED = 3