﻿`GB` BigData / [Олег Гладкий](https://gb.ru/users/3837199) // домашнее задание

`262698` __Методы сбора и обработки данных из сети Интернет__:  `08`. Scrapy:__API__ и __Login__

# Scrapy: API и Login

## API

Проект: __api\_test__

Проверка технологии в соответствии с примером по курсу сайта http://quotes.toscrape.com/scroll

<!--  -->

Проект: __api__

1. Получение данных с сайта hh.ru, поддерживающего API, по ключевому слову "python".
   * ключевое слово для выборки передаётся как параметр для паука из скрипта запуска
   * паука анализирует входящие параметры и принимает ключевое слово для парсинга
2. Сохранение полученных данных в базы MongoDB и SQLite
   * Название для БД и таблицы (коллекции), куда будем размещёть полученные вакансии указывается в settings.py 
   * Запрос этих имён выполняется в pipelines.py (как свойства паука) при инициализации классов работы с БД.

## Login
Работа с формами ввода на обычных и динамических сайтах

Проект: __login\_test__



1. Проверка технологии заполнения формы и входа на учебный сайт https://quotes.toscrape.com/login в соответствии с методическими материалом.

2. Попытка входа на сайт рассматривая его как динамический, то есть с использоваением `Splash`. 

   __Внимание!__  
   Здесь почему-то не всё гладко работает: успешно выполняется отправка формы `SplashFormRequest.from_response()` по технологии Splash только в том случае, если загрузка страницы с формой выполняется без Splash-а, то есть просто Request()... -- Глупость какая-то: а как же мы загрузим форму, если она динамическая? 

<!--  -->

Проект: __login\_sandbox__

Регистрация на учебном сайте scrapethissite.com
1. Использование токена csrf
2. С использованием токена и ведение запросов при помощи `Splash` как на динамическом сайте

Прим.: Splash работает успешно везде: и при загрузке формы и при её отправке...
<!--  -->

2023-03-02