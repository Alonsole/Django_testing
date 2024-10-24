# Тестирование Django-приложения

## Описание

Бэкенд простого приложения с курсами и списком студентов. Вся логика для бэкенда уже есть в заготовке и описаны тесты.

## Что Сделано?

Написаны тесты для текущей логики приложения.

Заведены фикстуры:

- для api-client - def client(),
- для фабрики курсов - def course_create(),
- для фабрики студентов - def student_create(),
- создание трех экземпляров модели Coursе - def course_n(course_create).

В качестве библиотеки для фабрик используется `model_bakery` (https://github.com/model-bakers/model_bakery).

URL Для теста вынесен:  
test_url = '/api/v1/courses/'

Добавлены следующие тесты:

- проверка получения первого курса (retrieve-логика) - def test_get_first_course(client, course_create),
- проверка получения списка курсов (list-логика) - def test_get_list_course(client, course_n),
- проверка фильтрации списка курсов по `id`- test_course_filter_list_by_id(client, course_n),
- проверка фильтрации списка курсов по `name` - def test_filter_course_list_by_name(client, course_n),
- тест успешного создания курса - def test_create_course(client),
- тест успешного обновления курса - def test_update_course(client, course_create),
- тест успешного удаления курса - def test_delete_course(client, course_create).

Перед началом работы убедитесь, что все зависимости установлены (dev-зависимости указаны в `requirements-dev.txt`) 
и тесты успешно запускаются. Вы должны увидеть:

## Документация

pytest: https://docs.pytest.org/en/stable/

pytest-django: https://pytest-django.readthedocs.io/en/latest/

тестирование DRF: https://www.django-rest-framework.org/api-guide/testing/

## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements-dev.txt
```

Вам необходимо будет создать базу в postgres, настроить подключение к ДБ и прогнать миграции:

settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netology_django_testing',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'Пароль!!!',
    }
}
```
Выполнить миграцию:

```base
python manage.py migrate
```

Запуск тестов по команде:

```bash
pytest
```

Проверка покрытия тестов:  
В пропуске: tests/* , .venv/* , manage.py, django_testing/* , *tests.py

Запуск по команде:

```bash
 pytest --cov=.
```
Пример вывода:
```
Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
students\__init__.py                                 0      0   100%
students\admin.py                                    1      0   100%
students\apps.py                                     3      0   100%
students\filters.py                                  7      0   100%
students\migrations\0001_initial.py                  5      0   100%
students\migrations\0002_auto_20201101_2359.py       4      0   100%
students\migrations\__init__.py                      0      0   100%
students\models.py                                   7      0   100%
students\serializers.py                              6      0   100%
students\views.py                                   10      0   100%
--------------------------------------------------------------------
TOTAL                                               43      0   100%
```