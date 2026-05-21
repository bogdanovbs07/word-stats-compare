# executor.py

from job_types import JobType
from handlers.word_stats_compare import handle_word_stats_compare, PermanentJobError

def execute_job(job):
    """
    Диспетчер задач — выбирает обработчик в зависимости от типа
    """
    try:
        if job["job_type"] == JobType.WORD_STATS.value:
            # Здесь был бы вызов обработчика WORD_STATS
            return {"status": "WORD_STATS handler would run here"}
        
        elif job["job_type"] == JobType.WORD_STATS_COMPARE.value:
            # ← НОВЫЙ ОБРАБОТЧИК
            result = handle_word_stats_compare(job.get("payload"))
            return {"status": "DONE", "result": result}
        
        elif job["job_type"] == JobType.DOWNLOAD.value:
            return {"status": "DOWNLOAD handler would run here"}
        
        else:
            raise PermanentJobError(f"Unknown job type: {job['job_type']}")
    
    except PermanentJobError as e:
        return {"status": "FAILED", "error": str(e)}

# Пример использования (для демонстрации)
if __name__ == "__main__":
    test_job = {
        "job_type": "WORD_STATS_COMPARE",
        "payload": {
            "left_job_id": "123e4567-e89b-12d3-a456-426614174000",
            "right_job_id": "987fcdeb-51a2-43d7-9abc-def123456789"
        }
    }
    
    result = execute_job(test_job)
    print("Результат выполнения задачи:")
    print(result)
