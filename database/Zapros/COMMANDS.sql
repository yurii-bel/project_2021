-- Обновление данных в таблице сразу пишем, что и на что хотим заменить
-- потом условие что мы хотим изменить какой кусок и у какого пользователя.
UPDATE "CATEGORY" SET CAT_NAME = 'БЫТОВУХА' WHERE CAT_NAME = 'Фильмс' AND USER_ID = '1'

-- Проверка на имя пользователя.
SELECT USER_N_name FROM "USER_NAME" WHERE USER_N_name = 'Дмитрий'

-- Создаем таблицу.
-- Создаем числовой столбец счетчик, не пустой, уникальное значение, это ключ.
-- Создаем числовой столбец, обязательно для заполнения.
-- Создаем текстовый столбец, обязательно для заполнения.
-- Создаем числовой столбец, обязательно для заполнения.
-- Создаем столбец даты, обязательно для заполнения.
-- Создаем текстовый столбец, обязательно для заполнения.
-- Создаем текстовый столбец.
-- Указываем на связь с другой талблицей.


CREATE TABLE "ACTIVITY"(

	ACT_ID SERIAL NOT NULL UNIQUE PRIMARY KEY,
	USER_ID INT NOT NULL,
	ACTL_name VARCHAR(64) NOT NULL,
	ACT_time INT NOT NULL,
	ACT_date DATE NOT NULL,
	CAT_name VARCHAR(64) NOT NULL,
	ACT_comment TEXT NULL,
	FOREIGN KEY (USER_ID, ACTL_name, CAT_name) 
	REFERENCES "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) 
	ON DELETE CASCADE ON UPDATE CASCADE
);

--------------------------------
-- Добавляем данные в таблицу --
--------------------------------

-- Добавляем данные в таблицу USER.
INSERT INTO "USER" (USER_N_ID, USER_P_ID) VALUES 
('N1', 'P1'), 
('N2', 'P2')

-- Добавляем данные в таблицу USER_NAME.
INSERT INTO "USER_NAME" (USER_N_ID, USER_N_name, USER_N_Telegram) VALUES 
('N1', 'Sif', '5646511561'), 
('N2', 'NO-Sif', '')

-- Добавляем данные в таблицу USER_PRIVAT.
INSERT INTO "USER_PRIVAT" (USER_P_ID, USER_P_email, USER_P_password) VALUES 
('P1', 'Sif@gmail.ua', 'qwerty'), 
('P2', 'NO-Sif@gmail.ua', 'qwerty')

-- Добавляем данные в таблицу SETTINGS.
INSERT INTO "SETTINGS" (USER_ID, SET_theme, SET_preferences) VALUES 
('1', 'Темная тема', 'Разные настройки'),
('2', 'Светлая тема', 'Другие настройки')

-- Добавляем данные в таблицу CATEGORY.
INSERT INTO "CATEGORY" (USER_ID, CAT_name) VALUES 
('1', 'Отдых'), 
('1', 'Спорт'), 
('2', 'Обучение')

-- Добавляем данные в таблицу ACTIVITY_LIST.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES 
('1', 'Сон', 'Отдых'), 
('1', 'Бег', 'Спорт'), 
('2', 'Чтение', 'Обучение')

-- Добавляем данные в таблицу ACTIVITY.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES 
('1', 'Сон', '120', '2021.05.17', 'Отдых', (NULL)),
('1', 'Бег', '30', '2021.5.10', 'Спорт', 'Тестовая запись'),
('2', 'Смотрел Ютуб', '153', '2021.04.05', 'Отдых', 'Мультик «Навсикая из долины ветров»')

--------------
-- Удаление --
--------------

-- Удаление таблиц в черезвычайной ситуации (безвозвратно).
DROP TABLE "ACTIVITY" ;
DROP TABLE "ACTIVITY_LIST" ;
DROP TABLE "CATEGORY" ;
DROP TABLE "SETTINGS" ;
DROP TABLE "USER_NAME" ;
DROP TABLE "USER_PRIVATE" ;
DROP TABLE "USER" ;

-- Удаление нужного столбца в нужной таблице.
ALTER TABLE "SETTINGS" DROP COLUMN SET_THEME

-----------
-- Вывод --
-----------

-- Вывод всего из таблицы ACTIVITY.
SELECT * FROM "ACTIVITY"

-- Вывод информации с любой вам таблицы с любимы\нужными столбцами этой же 
-- таблци вместо *, а так же условине что хотите вывести инф. пользователя 1.
SELECT * FROM "CATEGORY" WHERE USER_ID = '1'

-- Вывод информации по пользователю в заданом промежутке времени\даты 
-- с нужными нам таблицами а так же этот запрос можно использовать для графиков.
SELECT ACT_TIME, ACT_DATE, CAT_NAME FROM "ACTIVITY" WHERE ACT_DATE 
BETWEEN '2021.04.01' AND '2021.04.30' AND USER_ID = '1'

-- Вывод информации.
SELECT "USER".USER_ID == (1) , USER_NAME , CAT_NAME FROM "USER" 
LEFT JOIN "ACTIVITY_LIST" ON "USER".USER_ID="ACTIVITY_LIST".USER_ID 

SELECT "USER_NAME".user_n_name = 'NO-Sif' FROM "USER_NAME"

SELECT "USER_NAME".user_n_name = FROM "USER_NAME"

--------------------
-- Экспорт/Импорт --
--------------------

-- Импорт нужного файла в нужную таблицу в нужные столбцы, формат csv обязателено 
-- указывать ибо импорт распознает по стандарту формат как txt.
COPY "CATEGORY" (USER_ID,CAT_NAME) 
FROM 'C:\Users\Game-PC\Desktop\Proekt\neew\MUUSSOR\CATEGORY.csv' (format CSV)

-- Экспорт данных о пользователе с нужного нам запроса а это инфа по пользователю 1 
-- с таблицы категория так же можем задать столбцы которые вытянем из нужной таблицы.
COPY (SELECT USER_ID, CAT_NAME FROM "CATEGORY" WHERE USER_ID = 1) 
TO 'C:\Users\Game-PC\Desktop\Proekt\neew\MUUSSOR\CATEGORY.csv'(format CSV)
