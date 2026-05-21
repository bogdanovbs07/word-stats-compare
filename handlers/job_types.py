# job_types.py

from enum import Enum

class JobType(Enum):
    WORD_STATS = "WORD_STATS"
    DOWNLOAD = "DOWNLOAD"
    PARSE = "PARSE"
    WORD_STATS_COMPARE = "WORD_STATS_COMPARE"  # ← НОВЫЙ ТИП
