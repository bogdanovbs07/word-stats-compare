# WORD_STATS_COMPARE — задача для Celery + Redis

## Описание задания

Новый тип задачи `WORD_STATS_COMPARE` анализирует результаты двух задач `WORD_STATS` и находит:
- общие слова
- слова только из первой задачи
- слова только из второй задачи

## Структура репозитория

word-stats-compare/
├── handlers/
│ └── word_stats_compare.py # Основная логика
├── tests/
│ └── test_word_stats_compare.py # Модульные тесты
├── job_types.py # Перечисление типов задач
├── executor.py # Диспетчер задач
└── README.md # Документация


## Как запустить тесты

```bash
python tests/test_word_stats_compare.py

from executor import execute_job

job = {
    "job_type": "WORD_STATS_COMPARE",
    "payload": {
        "left_job_id": "uuid-левой-задачи",
        "right_job_id": "uuid-правой-задачи"
    }
}

result = execute_job(job)
print(result)

{
    "status": "DONE",
    "result": {
        "left_job_id": "uuid-левой-задачи",
        "right_job_id": "uuid-правой-задачи",
        "left_url": "https://example.com/page1",
        "right_url": "https://example.com/page2",
        "common_words": ["celery", "python"],
        "left_only": ["redis"],
        "right_only": ["rabbitmq"]
    }
}
