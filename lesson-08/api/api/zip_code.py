''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing, https://gb.ru/lessons/262705/
    ДЗ-8: Scrapy API & Login
    https://habr.com/ru/company/hh/blog/303168/
'''

    # ЗАПАС...

def my_zip_code():
    ''' Запас кода...
        curl -k -H "User-Agent: api-test-agent" "https://api.hh.ru/vacancies"
    '''
    # Сопроводительные данные (заголовки) ответа JSON:
    var_res_env = {
        "items": [],
        "found": 1004930,
        "pages": 100,
        "per_page": 20,
        "page": 0,
        "clusters": null,
        "arguments": null,
        "alternate_url":"https://hh.ru/search/vacancy?enable_snippets=true"
    }
    # Cтруктура item в ответе:
    var_res = {
        "id": "77186993",
        "premium": false,
        "name": "Продавец - консультант в Mustang (ТРЦ Планета)",
        "department": null,
        "has_test": false,
        "response_letter_required": false,
        "area": {"id": "54", "name": "Красноярск", "url": "https://api.hh.ru/areas/54"},
        "salary": {"from": 40000, "to": 50000, "currency": "RUR", "gross": false},
        "type": {"id": "open", "name": "Открытая"},
        "address": {
            "city": "Красноярск",
            "street": "улица 9 Мая",
            "building": "77",
            "lat": 56.050933,
            "lng": 92.904378,
            "description": null,
            "raw": "Красноярск, улица 9 Мая, 77",
            "metro": null,
            "metro_stations": [],
            "id": "679812"
        },
        "response_url": null,
        "sort_point_distance": null,
        "published_at": "2023-02-20T07:04:54+0300",
        "created_at": "2023-02-20T07:04:54+0300",
        "archived": false,
        "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=77186993",
        "insider_interview": null,
        "url": "https://api.hh.ru/vacancies/77186993?host=hh.ru",
        "adv_response_url": null,
        "alternate_url": "https://hh.ru/vacancy/77186993",
        "relations": [],
        "employer": {
            "id": "898175",
            "name": "Лемарон",
            "url": "https://api.hh.ru/employers/898175",
            "alternate_url": "https://hh.ru/employer/898175",
            "logo_urls": null,
            "vacancies_url": "https://api.hh.ru/vacancies?employer_id=898175",
            "trusted": true
        },
        "snippet": {
            "requirement": "Встречать покупателя с улыбкой и готовностью подобрать идеальный образ на любой случай. Поддерживатьпорядок в магазине. Требование к кандидату: Желание...",
            "responsibility": "Вашей задачей будет общаться с покупателем и подбирать им необходимую одежду. Обслуживать покупателей на кассе. Принимать участие в приеме товара. "
        },
        "contacts": null,
        "schedule": {"id": "shift", "name": "Сменный график"},
        "working_days": [],
        "working_time_intervals": [],
        "working_time_modes": [],
        "accept_temporary": false,
        "professional_roles": [{"id": "97", "name": "Продавец-консультант, продавец-кассир"}],
        "accept_incomplete_resumes": true,

    }
    pass
