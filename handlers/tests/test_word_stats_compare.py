# tests/test_word_stats_compare.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.word_stats_compare import (
    validate_payload, 
    compare_word_stats, 
    PermanentJobError
)

def test_valid_payload():
    """Тест 1: правильный payload"""
    import uuid
    payload = {
        "left_job_id": str(uuid.uuid4()),
        "right_job_id": str(uuid.uuid4())
    }
    validate_payload(payload)
    print("✅ Тест 1 пройден: корректный payload")

def test_missing_payload():
    """Тест 2: отсутствует payload"""
    try:
        validate_payload(None)
        print("❌ Тест 2 провален")
    except PermanentJobError as e:
        if "requires payload" in str(e):
            print("✅ Тест 2 пройден: отсутствие payload обработано")
        else:
            print(f"❌ Тест 2 провален: {e}")

def test_missing_left_id():
    """Тест 3: нет left_job_id"""
    import uuid
    payload = {"right_job_id": str(uuid.uuid4())}
    try:
        validate_payload(payload)
        print("❌ Тест 3 провален")
    except PermanentJobError as e:
        if "left_job_id" in str(e):
            print("✅ Тест 3 пройден: отсутствие left_job_id обработано")
        else:
            print(f"❌ Тест 3 провален: {e}")

def test_invalid_uuid():
    """Тест 4: неверный UUID"""
    import uuid
    payload = {
        "left_job_id": "not-a-uuid",
        "right_job_id": str(uuid.uuid4())
    }
    try:
        validate_payload(payload)
        print("❌ Тест 4 провален")
    except PermanentJobError as e:
        if "valid UUID" in str(e):
            print("✅ Тест 4 пройден: неверный UUID обработан")
        else:
            print(f"❌ Тест 4 провален: {e}")

def test_same_ids():
    """Тест 5: одинаковые ID"""
    import uuid
    same_id = str(uuid.uuid4())
    payload = {
        "left_job_id": same_id,
        "right_job_id": same_id
    }
    try:
        validate_payload(payload)
        print("❌ Тест 5 провален")
    except PermanentJobError as e:
        if "must be different" in str(e):
            print("✅ Тест 5 пройден: одинаковые ID обработаны")
        else:
            print(f"❌ Тест 5 провален: {e}")

def test_compare_words():
    """Тест 6: сравнение слов"""
    left_data = {"top_words": {"python": 10, "celery": 5, "redis": 3}}
    right_data = {"top_words": {"python": 8, "rabbitmq": 4, "celery": 2}}
    
    result = compare_word_stats(left_data, right_data)
    
    if set(result["common_words"]) == {"python", "celery"}:
        print("✅ Тест 6a пройден: common_words корректны")
    else:
        print(f"❌ Тест 6a провален: {result['common_words']}")
    
    if set(result["left_only"]) == {"redis"}:
        print("✅ Тест 6b пройден: left_only корректны")
    else:
        print(f"❌ Тест 6b провален: {result['left_only']}")
    
    if set(result["right_only"]) == {"rabbitmq"}:
        print("✅ Тест 6c пройден: right_only корректны")
    else:
        print(f"❌ Тест 6c провален: {result['right_only']}")

def test_demo_execution():
    """Тест 7: демонстрация полного выполнения"""
    from executor import execute_job
    
    test_job = {
        "job_type": "WORD_STATS_COMPARE",
        "payload": {
            "left_job_id": "123e4567-e89b-12d3-a456-426614174000",
            "right_job_id": "987fcdeb-51a2-43d7-9abc-def123456789"
        }
    }
    
    result = execute_job(test_job)
    
    if result["status"] == "DONE":
        print("✅ Тест 7 пройден: задача выполнена успешно")
        print(f"   Результат: {result['result']}")
    else:
        print(f"❌ Тест 7 провален: {result}")

if __name__ == "__main__":
    print("=" * 50)
    print("Запуск тестов для WORD_STATS_COMPARE")
    print("=" * 50)
    test_valid_payload()
    test_missing_payload()
    test_missing_left_id()
    test_invalid_uuid()
    test_same_ids()
    print("-" * 30)
    test_compare_words()
    print("-" * 30)
    test_demo_execution()
    print("=" * 50)
    print("Тестирование завершено")
