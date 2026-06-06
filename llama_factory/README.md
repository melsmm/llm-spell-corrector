# `llama_factory/` — конфигурация обучения

Дообучение модели проводилось в фреймворке [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) методом **LoRA** в две стадии. Здесь хранятся конфиги обучения (формат LLaMA Board) и графики обучения.

Базовая модель: [`RefalMachine/RuadaptQwen3-4B-Instruct`](https://huggingface.co/RefalMachine/RuadaptQwen3-4B-Instruct).

## `llamaboard_configs/`

### `stage_1.yaml` — Stage 1
LoRA-дообучение базовой модели на синтетическом датасете `spell_correction_1m` (~1 млн примеров).

Ключевые параметры:

| Параметр | Значение |
| --- | --- |
| Метод | LoRA (rank=32, alpha=64, dropout=0) |
| Датасет | `spell_correction_1m` |
| Эпохи | 2 |
| Learning rate | 8e-5 (cosine, warmup=10) |
| Batch size | 2 × grad. accum. 8 = **16** |
| Cutoff length | 4000 |
| Precision | bf16, FlashAttention-2 |
| Template | `qwen3_nothink` (без reasoning) |

### `stage_2.yaml` — Stage 2
Продолжение обучения **LoRA-адаптера из Stage 1** (`checkpoint_path: RuadaptQwen3_4B_Instruct_on_spell_correction_1m`) на качественном датасете `spell_correction_30k` (~30 тыс. готовых пар).

Отличия от Stage 1:

| Параметр | Значение |
| --- | --- |
| Стартовый чекпоинт | адаптер после Stage 1 |
| Датасет | `spell_correction_30k` |
| Эпохи | 10 |
| Learning rate | 5e-5 |

Идея двухстадийного подхода: сначала модель учится на большом объёме разнообразных синтетических ошибок, затем «дошлифовывается» на меньшем, но более качественном наборе реальных пар.

## `training_graphics/`
Графики процесса обучения:

- `training_loss_stage_1.png` — кривая обучающего loss;
- `training_eval_loss_stage_1.png` — кривая валидационного loss.

## После обучения

Полученный LoRA-адаптер мержится с базовой моделью и публикуется как [`melsmm/Spell-Corrector-RU-4B`](https://huggingface.co/melsmm/Spell-Corrector-RU-4B). Запуск — см. корневой [README](../README.md#-запуск-модели).
