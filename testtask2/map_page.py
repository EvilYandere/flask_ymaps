from typing import Union
from flask import Blueprint, render_template, request, redirect, url_for, session, Response
from testtask2.forms import MapForm
from bs4 import BeautifulSoup
import requests
import testtask2.is_mkad
import logging

# необходимые библиотеки


logging.basicConfig(filename='logs.log')    # логирование
logger = logging.getLogger()
map_page = Blueprint('map_page', __name__, template_folder='templates')  # blueprint
api_key = '4dd3cbc3-f73e-445b-8343-2c16a0a1cecc'  # ключ разработчика для Yandex Геокодера


@map_page.route('/', methods=['GET', 'POST'])  # страница для ввода адреса
def get_distance() -> Union[str, Response]:  # функция вычисления расстояния
    form = MapForm()  # использование заранее созданной формы из файла forms.py
    if request.method == "POST":  # метод "POST"
        address = request.form['address']  # считывание адреса, введенного пользователем в форму
        if address == '':  # если адрес пустой
            raise Exception('Пустой запрос')
        source = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}')
        # обращение к Геокодеру с указанным ключом разработчика и введенным адресом
        if source.status_code == 500:  # если нет ответа от серверов Яндекса
            raise Exception('Ошибка сервера')  # ошибка сервера
        source = source.text  # преобразование полученного ответа в текст
        soup = BeautifulSoup(source, 'xml')  # создание экземпляра BeautifulSoup, параметр документа - XML
        try:
            true_address = soup.find('Point').text  # поиск внутри XML-документа тэга Point,
        # так как в нем содержатся координаты точки
        except AttributeError:  # если ошибка в возвращаемом сервером значении
            raise Exception('API вернул NoneType object')
        if true_address is None:  # если ответ от сервера пустой
            raise Exception('Запрошенный результат не найден')
        coords = testtask2.is_mkad.address_to_float(true_address)  # преобразование полученной точки
        # в пару из двух float
        if testtask2.is_mkad.is_mkad(coords):  # если указанная точка находится внутри массива точек МКАД
            true_address = 'Точка внутри МКАД'
            session['true_address'] = true_address  # передача найденного адреса в сессию
            logger.info(f'{address}, " ", {true_address}'.encode('utf-8'))    # запись логов
            return redirect(url_for('.your_address', address=true_address))
            # перенаправление на страницу с результатом, с передачей адреса через сессию
        else:
            closest_point = testtask2.is_mkad.closest_point(coords)  # иначе поиск ближайшей точки на МКАД
            distance_to_mkad = testtask2.is_mkad.mkad_distance(coords, closest_point)  # расчет расстояния до МКАД
            session['true_address'] = distance_to_mkad  # передача найденного адреса в сессию
            logger.info(f'{address}, " ", {distance_to_mkad}'.encode('utf-8'))    # запись логов
            return redirect(url_for('.your_address', address=true_address))
        # перенаправление на страницу с результатом, с передачей адреса через сессию
    return render_template('get_distance.html', form=form)  # рендер страницы


@map_page.route('/your_address', methods=['GET', 'POST'])  # страница для получения результата
def your_address() -> str:  # функция вывода адреса
    true_address = session['true_address']  # получение из сессии вычисленного ранее адреса
    return render_template('your_address.html', address=true_address)  # рендер страницы
