from enum import Enum


class ChallengeStatus(Enum):
    PENDING = 'pending'
    COMPLETE = 'complete'
    FAILED = 'failed'


