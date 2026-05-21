# handlers/word_stats_compare.py

import uuid

class PermanentJobError(Exception):
    """Исключение для фатальных ошибок задачи"""
    pass

def validate_payload(payload):
    """Проверяет корректность payload."""
    if payload is None:
        raise PermanentJobError("WORD_STATS_COMPARE requires payload")
    
    left_id = payload.get("left_job_id")
    right_id = payload.get("right_job_id")
    
    if left_id is None or right_id is None:
        raise PermanentJobError("WORD_STATS_COMPARE requires left_job_id and right_job_id in payload")
    
    try:
        uuid.UUID(str(left_id))
    except ValueError:
        raise PermanentJobError(f"left_job_id must be a valid UUID, got: {left_id}")
    
    try:
        uuid.UUID(str(right_id))
    except ValueError:
        raise PermanentJobError(f"right_job_id must be a valid UUID, got: {right_id}")
    
    if left_id == right_id:
        raise PermanentJobError("left_job_id and right_job_id must be different")

def compare_word_stats(left_data, right_data):
    """Сравнивает слова из двух задач WORD_STATS."""
    left_words = set(left_data.get("top_words", {}).keys())
    right_words = set(right_data.get("top_words", {}).keys())
    
    return {
        "common_words": sorted(list(left_words & right_words)),
        "left_only": sorted(list(left_words - right_words)),
        "right_only": sorted(list(right_words - left_words))
    }

def handle_word_stats_compare(job_payload):
    """
    Основной обработчик задачи WORD_STATS_COMPARE.
    job_payload должен содержать left_job_id и right_job_id.
    """
    validate_payload(job_payload)
    
    left_id = job_payload["left_job_id"]
    right_id = job_payload["right_job_id"]
    
    # Здесь должна быть загрузка задач из БД
    # Для демонстрации используем заглушки
    left_data = {"top_words": {"python": 10, "celery": 5, "redis": 3}}
    right_data = {"top_words": {"python": 8, "rabbitmq": 4, "celery": 2}}
    
    comparison = compare_word_stats(left_data, right_data)
    
    return {
        "left_job_id": left_id,
        "right_job_id": right_id,
        "left_url": "https://example.com/page1",
        "right_url": "https://example.com/page2",
        **comparison
    }
