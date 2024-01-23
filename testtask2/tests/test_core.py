import responses


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


@responses.activate
def test_empty_address(client):
    api_key = 'some_api_key'
    address = ''
    responses.add(
        responses.POST,
        f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}',
        status=302
    )
    response = client.post('/')
    assert response.status_code == 500, 'Пустой запрос'


@responses.activate
def test_wrong_address(client):
    api_key = 'some_api_key'
    address = 'asdasjfaslkfjas;fjas;klf'
    responses.add(
        responses.POST,
        f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}'
    )
    response = client.post('/')
    assert response.status_code == 400, 'Результат не найден'


@responses.activate
def test_out_of_mkad(client):
    api_key = 'some_api_key'
    address = 'Саратов, площадь Ленина'
    client.get('/')
    responses.add(
        responses.POST,
        f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}',
        status=302
    )
    response = client.get('/your_address?address=45.970117+51.58051')
    assert b'509.7062853821279' in response.data


@responses.activate
def test_out_of_mkad(client):
    api_key = 'some_api_key'
    address = 'Москва, ЦНИИ туберкулёза'
    client.get('/')
    responses.add(
        responses.POST,
        f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}',
        status=302
    )
    response = client.get('/your_address?address=38.343043+55.714105')
    assert 'Точка внутри МКАД' in response.data
