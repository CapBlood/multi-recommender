# Разработка

На данной странице описаны частные случаи, описывающие шаблонные действия для расширения, модификации или тестирования функционала Multirec.

## Добавление новых команд CLI

Для добавления новых команд необходима модификация модуля `cli.py` в корне пакета `multirec`. Для добавления новой команды необходимо создать новую функцию и обернуть ее в декоратор `@manage.command`, добавляя далее необходимые вам декораторы в соответствии с библиотекой [click](https://click.palletsprojects.com/en/8.1.x/). Например:
```python
@manage.command()
@click.argument(
    'csv_path',
    type=click.Path(exists=True, dir_okay=False)
)
@click.option(
    '--mappings',
    type=click.STRING
)
@click.option(
    '--index',
    type=click.STRING,
    default=None,
    help='Наименование столбца индексов.'
)
def web(csv_path, mappings, index):
    env = dict()
    if mappings:
        env['MAPPINGS'] = mappings
    if index:
        env['INDEX'] = index

    os.environ.update(env)
    subprocess.run([
        "streamlit", "run", "src/multirec/web/app.py",
        csv_path
    ])
```

После реализации команда будет доступна через [Kedro](https://docs.kedro.org/en/stable/get_started/install.html) и через утилиту multirec, устанавливаемую с пакетом:
```bash
kedro manage web --index Rank --mappings Shikimori_url:Url,recommendations:Recommendations,Russian_name:Name,Russian_description:Description data/03_primary/anime_with_recommendations.csv
```

## Добавление новых модульных пайплайнов

Добавление новых модульных пайплайнов осуществляется с помощью утилиты [Kedro](https://docs.kedro.org/en/stable/get_started/install.html), например:
```bash
kedro pipeline create drop_nan_column
```

После выполнения вышеуказанной команды в подпакете `pipelines` пакета `multirec` создастся новый пайплайн (подпакет) с указанным именем и с шаблонными файлами:

- `README.md`, содержащий описание пайплайна (его входные, выходные данные и описание работы);
- `nodes.py`, предназначенный для хранения функций, который ответственный за основной функционал;
- `pipeline.py`, предназначенный для оборачивания функций из `nodes.py` в `node` и затем в `pipeline`, функций `create_pipeline` должна возвращать готовый `pipeline`.

Также одновременно создастся одноименный пакет в директории `tests`, предназначенный для хранения тестов соответствующего пайплайна.

После реализации модульного пайплайна также необходимо создать в его пакете файл `requirements.txt` с требуемыми для него библиотеками Python, который также необходимо продублировать в корневой `requirements.txt` пакета `multirec`.

Для включения модульного пайплайна в "общие" пайплайны, запускаемые через утилиту Kedro или `multirec`, необходимо зарегистрировать в файле `pipeline_registry.py` в корне пакета `multirec` новый пайплайн или добавить в уже существующий ([подробнее](https://docs.kedro.org/en/stable/nodes_and_pipelines/pipeline_registry.html) об этом). 

## Кастомные датасеты

В данном проекте используется кастомный датасет `MongoDBDataset`:
- при загрузке происходит экспорт указанной коллекции в `JSON`, затем его конвертация в `pandas.Dataframe`, который передается далее пайплайну;
- при сохранении происходит конвертация полученного на вход `pandas.Dataframe` в `JSON` и его вставка с перезаписью в указанную коллекцию `MondoDB`.

Пример конфигурации `MongoDBDataset`:
```yml
dataframe_with_recs:
  type: multirec.extras.datasets.mongo_dataset.MongoDBDataset
  filepath: mongodb://localhost:27017
  database: test
  collection: anime
  # filter_columns - опционален
  filter_columns:
    - Name
    - Episodes
    - Studio
    - Rating
    - Description
    - Tags
    - Related_Mange
    - recommendations
```


## Тестирование 

Запуск тестов осуществляется с помощью утилиты [Tox](https://tox.wiki/en/latest/). Для запуска необходимо в корне проекта запустить следующую команду, которая запустит все найденные ею тесты в пакете `tests`:
```bash
tox
```

## Сборка пакета

Для сборки пакета необходимо в корне репозитория выполнить команду `python -m build . --wheel`, после чего в директории `dist` появится пакет `.whl`, который затем можно установить.

## Микроупаковка модульных пайплайнов

Для микроупаковки модульного пайплайна Kedro необходимо ввести следующую команду в корне репозитория:
```bash
kedro micropkg package pipelines.<pipeline_name>
```

Для вставки микропакета модульного пайплайна в другой проект Kedro:
```bash
kedro micropkg pull -d pipelines /path/to/tag.gz
```
