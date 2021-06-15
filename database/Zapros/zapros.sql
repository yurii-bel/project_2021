
-- Добавление в нужную таблицу в нужные столбцы информацию
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('1', 'Спал', '360', '2021.03.31', 'Отдых', (NULL)),

-- Вывод информации с любой вам таблицы с любимы\нужными столбцами этой же таблци вместо * 
-- а так же условине что хотите вывести инф пользователя 1
SELECT * FROM "CATEGORY" WHERE USER_ID = '1'

-- Вывод информации по пользователю в заданом промежутке времени\
-- даты с нужными нам таблицами а так же этот запрос можно использовать для графиков
SELECT ACT_TIME, ACT_DATE, CAT_NAME FROM "ACTIVITY" WHERE  ACT_DATE  BETWEEN '2021.04.01' AND '2021.04.30' AND USER_ID = '1'

-- Удаление нужного столбца в нужной таблице
ALTER TABLE "SETTINGS"
DROP COLUMN SET_THEME

-- Удаление таблицы безвозвратно
DROP TABLE "SETTINGS"

-- импорт нужного файла в нужную таблицу в нужные столбцы, 
-- формат цсв обязателен вказывать как здесь так и при экспорте ибо импорт распознает по стандарту формат как txt
COPY "CATEGORY" (USER_ID,CAT_NAME)  FROM  'C:\Users\Game-PC\Desktop\Proekt\neew\MUUSSOR\CATEGORY.csv' (format CSV)

-- Экспорт данных о пользователе с нужного нам запроса а это инфа по пользователю 1 с таблицы категория
-- так же можем задать столбцы которые вытянем из нужной таблицы
COPY (SELECT USER_ID, CAT_NAME FROM "CATEGORY" WHERE USER_ID = 1) TO 'C:\Users\Game-PC\Desktop\Proekt\neew\MUUSSOR\CATEGORY.csv'(format CSV)

-- Обновление данных в таблице сразу пишем что и на что хотим заменить потом условие что мы хотим изменить\
--какой кусок и у какого пользователя
UPDATE "CATEGORY"
SET CAT_NAME = 'БЫТОВУХА' WHERE CAT_NAME = 'Фильмс' AND USER_ID = '1'

-- Проверка на имя пользователя
SELECT USER_N_name  FROM "USER_NAME" WHERE USER_N_name = 'Дмитрий' 

