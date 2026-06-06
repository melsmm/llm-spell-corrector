# `notebooks/` — Jupyter-ноутбуки

Ноутбуки покрывают весь пайплайн проекта: построение датасетов, оценку качества и замеры скорости инференса.

## Построение датасетов

### `build_spell_correction_dataset_1m.ipynb`
Сборка синтетического датасета на **~1 млн** примеров (`synth_spell_correction_1m.csv`) — основа для **Stage 1** обучения.

Чистые тексты (`nerus`, `gazeta`, `wikipedia`) портятся набором алгоритмов:

| Категория | Источник | Алгоритм | Примеров |
|---|---|---|---|
| Готовые пары | russian_gec_dataset | — | ~25 000 |
| Готовые пары | RUSpellRU | — | ~2 000 |
| Готовые пары | MultidomainGold | — | ~3 569 |
| Чистые (без изменений) | nerus / wikipedia / gazeta | identity | ~50 000 |
| SBSC (статистическая порча) | nerus / wikipedia / gazeta | SBSCCorruptor | ~200 000 |
| CharAug | nerus / wikipedia / gazeta | CharAugCorruptor | ~150 000 |
| WordAug | nerus / wikipedia / gazeta | WordAugCorruptor | ~100 000 |
| Punctuation corruption | nerus / wikipedia / gazeta | custom | ~150 000 |
| Lowercase | nerus / wikipedia / gazeta | lowercase | ~100 000 |
| Mixed (2–3 алгоритма) | nerus / wikipedia / gazeta | multi-corrupt | ~219 431 |
| **ИТОГО** | | | **~1 000 000** |

Собственный алгоритм **`corrupt_punctuation`** удаляет знаки препинания (по отдельности или все сразу) и вставляет лишние — для обучения модели восстановлению пунктуации. Добавление «чистых» примеров без изменений учит модель не «переисправлять» корректный текст.

### `build_spell_correction_dataset_30k.ipynb`
Сборка датасета `spell_correction_30k.csv` из объединения **готовых пар** открытых датасетов (~30 тыс.) — используется на **Stage 2** обучения. Идея: дать модели в конце обучения увидеть качественные, «человеческие» примеры ошибок.

Оба ноутбука также строят графики статистик (см. [`../data/graphics/`](../data/graphics/)).

## Оценка качества

### `spell_correction_eval_stage_1.ipynb` / `spell_correction_eval_stage_2.ipynb`
Асинхронная оценка модели (Stage 1 / Stage 2) на бенчмарке [`ai-forever/spellcheck_punctuation_benchmark`](https://huggingface.co/datasets/ai-forever/spellcheck_punctuation_benchmark) — датасеты `RUSpellRU`, `MultidomainGold`, `MedSpellchecker`, `GitHubTypoCorpusRu`.

Запросы идут на vLLM-сервер (OpenAI-совместимый API), метрики считаются через `sage.evaluation.Scorer`. Результаты сохраняются в [`../data/metrics/`](../data/metrics/).

## Замеры скорости инференса

### `inference_time_spell_corrector.ipynb`
Замер времени инференса нашей модели через vLLM (асинхронные запросы).

### `inference_time_sage.ipynb`
Замер времени инференса `sage_fredt5_large` для сравнения.

➡️ На RUSpellRU (2008 примеров): наша модель — **45 с** (0.022 с/пример), SAGE — **284 с** (0.141 с/пример).

## Запуск

Перед оценкой/замерами нужно поднять vLLM-сервер с моделью (см. корневой [README](../README.md#-запуск-модели)). Ноутбуки по умолчанию обращаются к `http://localhost:9900/v1`.

Зависимости — в корневом [`requirements.txt`](../requirements.txt).
