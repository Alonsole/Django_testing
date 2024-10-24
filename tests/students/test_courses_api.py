import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course


@pytest.fixture
def client():
    """Фикстура для клиента"""
    return APIClient()


@pytest.fixture
def course_create():
    """Фикстура для фабрики курсов"""
    def create_course(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return create_course


@pytest.fixture
def student_create():
    """Фикстура для фабрики студентов"""
    def create_student(*args, **kwargs):
        return baker.make(Student, *args,**kwargs)
    return create_student

@pytest.fixture
def course_n(course_create):
    """Фикстура создание трех экземпляров модели Course"""
    return course_create(_quantity=3,)


test_url = '/api/v1/courses/'


@pytest.mark.django_db
def test_get_first_course(client, course_create):
    """
    Проверка получения первого курса (retrieve-логика):
    создаем курс через фабрику;
    строим урл и делаем запрос через тестовый клиент;
    проверяем, что вернулся именно тот курс, который запрашивали;
    """
    add_course = course_create(name='First Test course',)
    response = client.get(test_url)
    assert response.status_code == 200
    data = response.json()
    assert data[0].get('name') == add_course.name


@pytest.mark.django_db
def test_get_list_course(client, course_n):
    """
    Проверка получения списка курсов:
    создаем курсы через фабрику;
    строим урл и делаем запрос через тестовый клиент;
    проверяем, что вернулся список курсов, который запрашивали;
    """
    response = client.get(test_url)
    assert response.status_code == 200
    data = response.json()
    for i, course_data in enumerate(data):
        assert course_data.get('name') == course_n[i].name


@pytest.mark.django_db
def test_course_filter_list_by_id(client, course_n):
    """Проверка фильтрации списка курсов по id"""
    for course in course_n:
        response = client.get(f'{test_url}?id={course.id}')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_course_list_by_name(client, course_n):
    """Проверка фильтрации списка курсов по Name"""
    for course in course_n:
        response = client.get(f'{test_url}?name={course.name}')
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    """Тест успешного создания курса"""
    count = Course.objects.count()
    data = {'name': 'Test create course',}
    response = client.post(test_url, data, )
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_create):
    """Тест успешного обновления курса"""
    course = course_create()
    data = {'name': 'Updated name course',}
    response = client.patch(f'{test_url}{course.id}/', data)
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == data.get('name')


@pytest.mark.django_db
def test_delete_course(client, course_create):
    """Тест успешного удаления курса"""
    course = course_create()
    response = client.delete(f'{test_url}{course.id}/')
    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()