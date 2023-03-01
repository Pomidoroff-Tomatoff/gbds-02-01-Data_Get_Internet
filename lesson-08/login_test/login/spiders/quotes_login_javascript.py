''' Тренируемся использовать формы в паучках Скрейпи совместно с плагином Сплэш.
    Несмотря на то, что на данном ресурсе javascript не используется и рендеринг не нужен,
    зато этот ресурс успешно обкатан паучком quotes_login используя стандартные
    методы Скрейпи.
    Но теперь, уже на проверенном ресурсе, мы хотим расширить наши знания и применить
    технологию работы с формами на основе плагина Splash.

    Соответствует методичке.
    Итак!
'''

import scrapy
from scrapy import Request, FormRequest
from scrapy_splash import SplashRequest, SplashFormRequest


class QuotesLoginJavascriptSpider(scrapy.Spider):
    name = 'quotes_login_javascript'
    allowed_domains = ['quotes.toscrape.com']
    start_url = 'https://quotes.toscrape.com/login'

    script = '''
        function main(splash, args)
            splash:init_cookies(splash.args.cookies)
            splash.resource_timeout = 10
            splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36")
            assert(splash:go(args.url))
            assert(splash:wait{time=0.5, cancel_on_redirect=false})
            return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
                cookies = splash:get_cookies(),
                url = splash:url(),
            }
        end
    '''     # https://splash.readthedocs.io/en/stable/scripting-ref.html

    def start_requests(self):
        ''' Первый запрос к ресурсу должен нас обеспечить ответом, который в дальнейшем анализируется
            методом parse() для ввода и отправки формы.

            Внимание:
                >  SplashRequest()
                   Если этот 1-ый запрос выполнять (рендерить) при помощи SplashRequest(),
                   то, во-первых, в дальнейшей роботе parse() возникают проблемы:
                   хотя мы и видим csrf_token (всё в порядке),
                   но отправка формы с этим csrf_token не только не возвращает нас
                   к цитатам (метод after_login()) -- мы остаёмся на сайте логина (https://quotes.toscrape.com/login).
                   Но, во-вторых, мы не видим цитат -- последний метод (проверки) after_login()
                   их не находит (цитат = 0)...

                >  Request()
                   А если 1-ый запрос выполнять стандартными средствами Скрэйпи, то несмотря на
                   ошибку адреса в методе after_login() (по прежнему это страницы логина),
                   результат ПОЛОЖИТЕЛЬНЫЙ: цитат = 10.
            Мысли:
                Так как вообще без Сплэша (паук quotes_login) работает ожидаемо правильно и успешно,
                то есть подозрений к следующему:
                    >> Мы теряем куки -- Сплэш их не возвращает?...
                    >> Теряем текущий токен?...
                    >> Настройки settings.py не все включены? Какие-то хитрые...
                    >> Windows-7: старая версия ОС и Сплэша...
        '''
        if not True:
            print(f"start_request: SCRAPY + SPLASH-plugin:\n  start_url =   {self.start_url}")
            request = SplashRequest(
                url=self.start_url,
                endpoint='execute',
                args={
                    'lua_source': self.script,
                    'endpoint': 'execute',
                    'wait': 1,
                },
                callback=self.parse
            )
        else:
            print(f"start_request(): Scrapy только:\n  start_url =   {self.start_url}")
            request = Request(
                url=self.start_url,
                callback=self.parse
            )
        yield request
        return None

    def parse(self, response):
        ''' Работаем с формой: получаем токен, вводим данные и отправляем '''

        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        username, password = ('admin', 'admin')
        print(f"Метод parse(): SCRAPY + SPLASH-plugin, заполняем и отправляем форму\n  {csrf_token=}\n  {username=}\n  {password=}\n  {response.url=}")

        form = SplashFormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': username,
                'password': password,
            },
            # <input type="submit" value="Login" class="btn btn-primary">
            # clickdata={'value': 'Login'}, # https://stackoverflow.com/questions/28038950/how-to-submit-a-form-in-scrapy
            args={
                'lua_source': self.script,
                'endpoint': 'execute',
                'wait': 1,
            },
            callback=self.after_login
        )
        yield form
        return None

    def after_login(self, response):
        ''' Проверка '''
        quotes = response.xpath('//div[@class="quote"]')
        print(f"Метод after_login(): Результат входа на сайт:\n  {response.url=} \n  НАЙДЕНО ЦИТАТ {len(quotes)=}")
        return None
