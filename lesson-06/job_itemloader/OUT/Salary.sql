/* Пытаемся найти записи, в которых минимальная зарплата отсутствует (Null), а максимальная указана. 
 * 
 * Мы предполагаем, что таких записей мы не найдём, потому что они потерялись в связи с особенностью обработки.
 * А имено: мы получаем строку с данными только в поле salary_min и при отсутствии для этого поля значений 
 * теряем значения для остальных полей...  
 * 
 */

SELECT * FROM vacancies_list_itemloader AS vli WHERE salary_min IS NULL AND salary_min IS NOT NULL;  

SELECT * FROM vacancies_list_itemloader AS vli WHERE salary_min IS NULL;