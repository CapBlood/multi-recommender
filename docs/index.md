# Welcome to Multirec Documentation

Multirec представляет собой набор рекомендательных систем для разного рода медиа-развлечений:

- фильмы;
- аниме;
- игры и т.д. 

## Установка

### Через PyPI
Установка доступна через `pip`:
```
pip install multirec
```

### Через Kedro

В данном варианте достаточно только клонировать данный репозиторий, затем установить все зависимости с помощью команды `pip install -r src/requirements.txt` и далее работать с [CLI Kedro](https://docs.kedro.org/en/stable/development/commands_reference.html).

## Использование

### Через PyPI
Использование осуществляется с помощью утилиты `multirec` из терминала, устанавливаемой вместе с пакетом (см. [Установка](#через-pypi)). Пример запуска пайплайна, заданного Kedro по умолчанию (подробнее [здесь](pipelines.md)):
```bash
multirec run <path_to_csv> <out_path_to_csv>
```

В данном примере `dataframe` и `dataframe_with_recs` заданы в качестве аргументов, однако при запуске через утилиту Kedro используются значения из директории `conf`.

### Через Kedro

Для работы с Multirec в данном случае используется стандартная утилита `kedro` ([документация](https://kedro.readthedocs.io/en/stable/development/commands_reference.html)).

Для получения списка доступных пайплайнов необходимо вызвать следующую команду:
```bash
kedro registry list
```

**Примечание:** в случае клонирования утилиту Kedro необходимо запускать из корня клонированного репозитория.

### Веб-интерфейс

Multirec имеет простейший интерфейс упрощающий вывод результатов рекомендательных систем на основе [Streamlit](https://streamlit.io/) (например, для тестирования). Для его использования необходимо задать путь к готовому csv-файлу с предсказанными рекомендациями, опционально можно также задать соответствия имен, так как для работы веб-интерфейса требуются определенные столбцы с конкретными названиями:
```
'Name',
'Description',
'Tags',
'Url',
'Recommendations'
```

Пример запуска веб-интерфейса (через Kedro):
```bash
kedro manage web --index Rank --mappings Shikimori_url:Url,recommendations:Recommendations,Russian_name:Name,Russian_description:Description data/03_primary/anime_with_recommendations.csv
```

Пример запуска веб-интерфейса (через `multirec`):
```bash
multirec web --index Rank --mappings Shikimori_url:Url,recommendations:Recommendations,Russian_name:Name,Russian_description:Description data/03_primary/anime_with_recommendations.csv
```

## Наборы данных

Для получения рекомендаций и использования веб-интерфейса можно использовать следующие наборы данных:

- [аниме](https://drive.google.com/file/d/11AMxQb2ADXRYVAXfqBA7X91CPnTnk69e/view?usp=sharing);
- [манга](https://drive.google.com/file/d/1MfU1R9Yaa5x6q2DJR0nz_pSBzKzwmFpy/view?usp=sharing).