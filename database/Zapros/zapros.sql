-- Ошибки!
-- Исправить "USER"(USER_Telegram) Вернуть уникальность!


--------------------------
-- Создаем таблицу USER --
--------------------------
CREATE TABLE "USER"(                         -- Создаем таблицу.
	USER_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Создаем числовой столбец, обязательно для заполнения, подключаем счетчик, это ключ🔑.
	USER_name VARCHAR (32) NOT null UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение обязательно.
	USER_email VARCHAR (64) NOT null UNIQUE, -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение обязательно.
	USER_password VARCHAR (64) NOT null,     -- Создаем текстовый столбец, обязательно для заполнения.
	USER_Telegram VARCHAR (64)               -- Создаем текстовый столбец, уникальное значение обязательно. Вернуть уникальность!
);

-- Добавляем немного данных в таблицу USER.
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) VALUES ('Sif', 'email@gmail.ua', 'qwerty', 'qwerty:Telegram'), ('NO-Sif', 'email2@gmail.ua', 'qwerty', '')

-- Проводим проверку корректности ввода в таблицу USER.
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) 
VALUES ('Sim', 'email@gmail.ua', 'qwerty', 'qwerty:TelegramSim')         -- Проверка уникальности USER_email.
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) 
VALUES ('Sif', 'emailSif@gmail.ua', 'qwerty', 'qwerty:TelegramSif')      -- Проверка уникальности USER_ID.
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) 
VALUES ('Sim', 'emailSif@gmail.ua', 'qwerty', 'qwerty:Telegram')         -- Проверка уникальности USER_Telegram.
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) 
VALUES ('SIF', 'EMAIL@gmail.ua', 'qwerty', 'qwerty:TELEGRAM')            -- Проверка на регистр. Ошибка!
INSERT INTO "USER" (USER_name, USER_email, USER_password, USER_Telegram) 
VALUES ('siF', 'Email@gmail.ua', 'qwerty', '')                           -- Проверка, можно ли пропустить ввод в USER_Telegram. Ошибка! Пустое поле, не может повторяться.

SELECT * FROM "USER"                         -- Проверяем таблицу USER.

------------------------------
-- Создаем таблицу SETTINGS --
------------------------------
CREATE TABLE "SETTINGS"(                     -- Создаем таблицу.
	USER_ID INT NOT NULL PRIMARY KEY REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE, -- Создаем числовой столбец, это ключ🔑, обязательно для заполнения, каскадная связь с таблицей.
	SET_theme TEXT,                          -- Создаем текстовый столбец.
	SET_preferences TEXT                     -- Создаем текстовый столбец.
);

-- Проводим проверку корректности ввода в таблицу SETTINGS.
INSERT INTO "SETTINGS" (USER_ID, SET_theme, SET_preferences) VALUES ('1', 'Моя личная тема', 'Мои предпочтения')

SELECT * FROM "SETTINGS"                     -- Проверяем таблицу SETTINGS.

------------------------------
-- Создаем таблицу CATEGORY --
------------------------------
CREATE TABLE "CATEGORY"(                     -- Создаем таблицу.
	CAT_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Создаем числовой столбец, подключаем счетчик.
	USER_ID INT NOT NULL REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,  -- создаем числовой столбец, обязательно для заполнения, каскадная связь с таблицей.
	CAT_name VARCHAR (64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	PRIMARY KEY (USER_ID, CAT_name),         -- Указываем где ключи🔑.
	UNIQUE (USER_ID, CAT_name)               -- Указываем где уникальное значение обязательно, зависит от всех перечисленных столбцов.
);

-- Добавляем немного данных в таблицу CATEGORY.
INSERT INTO "CATEGORY" (USER_ID, CAT_name) VALUES ('1', 'Отдых'), ('1', 'Спорт'), ('2', 'Отдых'), ('1', 'Работа'), ('1', 'Семья'), ('2', 'Обучение')

-- Проводим проверку корректности ввода в таблицу ACTIVITY_LIST.
INSERT INTO "CATEGORY" (USER_ID, CAT_name) VALUES ('1', 'Отдых')     -- Проверка на повтор CAT_name.
INSERT INTO "CATEGORY" (USER_ID, CAT_name) VALUES ('666', 'АД ТУТ!') -- Проверка на несуществующий USER_ID.

SELECT * FROM "CATEGORY"                     -- Проверяем таблицу CATEGORY.

-----------------------------------
-- Создаем таблицу ACTIVITY_LIST --
-----------------------------------
CREATE TABLE "ACTIVITY_LIST"(                -- Создаем таблицу.
	ACTL_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY,   -- Создаем числовой столбец, подключаем счетчик.
	USER_ID INT NOT NULL,                    -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,           -- Создаем текстовый столбец, обязательно для заполнения.
	FOREIGN KEY (USER_ID) REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,                         -- Указываем на связь с другой талблицей.
	FOREIGN KEY (USER_ID, CAT_name)	REFERENCES "CATEGORY" (USER_ID, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE, -- Указываем на связь с другой талблицей.
	PRIMARY KEY (USER_ID, ACTL_name, CAT_name), -- Указываем где ключи🔑.
	UNIQUE (USER_ID, ACTL_name, CAT_name)       -- Указываем где уникальное значение обязательно, зависит от всех перечисленных столбцов.
);

-- Добавляем немного данных в таблицу ACTIVITY_LIST.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('1', 'Сон', 'Отдых'), ('1', 'Бег', 'Спорт'), ('2', 'Сон', 'Отдых'), ('2', 'Чтение', 'Обучение')

-- Проводим проверку корректности ввода в таблицу ACTIVITY_LIST.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('2', 'Создание БД', 'Работа')  -- Проверяем связь USER_ID и CAT_name.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('2', 'Небывалое', 'Небывалое') -- Проверяем на CAT_name.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('9', 'Сон', 'Отдых')           -- Проверяем на уникальность USER_ID. 
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('1', 'Сон', 'Отдых')           -- Проверяем на повторный ввод.

SELECT * FROM "ACTIVITY_LIST"                   -- Проверяем таблицу ACTIVITY_LIST.

--------------------------
-- Создаем таблицу TIME --
--------------------------
CREATE TABLE "TIME"(                            -- Создаем таблицу.
	TIME_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Создаем числовой столбец, подключаем счетчик.
	TIME_value INT NOT NULL UNIQUE PRIMARY KEY  -- Создаем столбец даты, уникальное значение обязательно, это ключ🔑.
);

-- Добавляем немного данных в таблицу TIME.
INSERT INTO "TIME" (TIME_value) VALUES ('5'), ('10'), ('15'), ('20'), ('25'), ('30'), ('40'), ('45'), ('50'), ('60'), ('90'), ('100'), ('120'), ('150')

-- Проводим проверку корректности ввода в таблицу ACTIVITY_LIST.
INSERT INTO "TIME" (TIME_value) VALUES ('10')    -- Проверяем на повторный ввод.
INSERT INTO "TIME" (TIME_value) VALUES ('Текст') -- Проверяем на ввоб текста.

SELECT * FROM "TIME"                             -- Проверяем таблицу TIME.

--------------------------
-- Создаем таблицу DATE --
--------------------------
CREATE TABLE "DATE"(                             -- Создаем таблицу.
	DATE_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY, -- Создаем числовой столбец, подключаем счетчик.
	DATE_value DATE NOT NULL UNIQUE PRIMARY KEY  -- Создаем столбец даты, уникальное значение обязательно, это ключ🔑.
);

-- Добавляем немного данных в таблицу DATE.
INSERT INTO "DATE" (DATE_value) VALUES ('2021.5.9'), ('10.5.2021'), ('11.05.2021'), ('12.05.2021'), ('13.05.2021'), ('14.05.2021'), ('15.05.2021'), ('16.05.2021'), ('17.05.2021'), ('18.05.2021')

-- Проводим проверку корректности ввода в таблицу DATE.
INSERT INTO "DATE" (DATE_value) VALUES ('10.05.2021') -- Проверяем на повторный ввод.
INSERT INTO "DATE" (DATE_value) VALUES ('Текст') -- Проверяем на ввоб текста.

SELECT * FROM "DATE"                             -- Проверяем таблицу DATE.

------------------------------
-- Создаем таблицу ACTIVITY --
------------------------------
CREATE TABLE "ACTIVITY"(                         -- Создаем таблицу.
	ACT_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Создаем числовой столбец, подключаем счетчик, это ключ🔑.
	USER_ID INT NOT NULL,                        -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,              -- Создаем текстовый столбец, обязательно для заполнения.
	TIME_value INT NOT NULL,                     -- Создаем числовой столбец, обязательно для заполнения.
	DATE_value DATE NOT NULL,                    -- Создаем столбец даты, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,               -- Создаем текстовый столбец, обязательно для заполнения.
	FOREIGN KEY (USER_ID) REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,       -- Указываем на связь с другой талблицей.
	FOREIGN KEY (USER_ID, ACTL_name, CAT_name) REFERENCES "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE, -- Указываем на связь с другой талблицей.
	FOREIGN KEY (TIME_value) REFERENCES "TIME" (TIME_valuE) ON DELETE CASCADE ON UPDATE CASCADE, -- Указываем на связь с другой талблицей.
	FOREIGN KEY (DATE_value) REFERENCES "DATE" (DATE_vaLue) ON DELETE CASCADE ON UPDATE CASCADE  -- Указываем на связь с другой талблицей.	
);

-- Добавляем немного данных в таблицу COMMENT.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES 
('1', 'Сон', '120', '2021.05.17', 'Отдых'),
('1', 'Бег', '30', '2021.05.10', 'Спорт'),
('2', 'Сон', '50', '2021.05.15', 'Отдых')

-- Проводим проверку корректности ввода в таблицу COMMENT.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('', 'Сон', '120', '2021.05.17', 'Отдых')  -- Пустой USER_ID
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('2', '', '120', '2021.05.17', 'Отдых')    -- Пустой ACTL_name
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('2', 'Сон', '', '2021.05.17', 'Отдых')    -- Пустой TIME_value
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('2', 'Бег', '120', '', 'Отдых')           -- Пустой DATE_value
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('2', 'Сон', '120', '2021.05.17', '')      -- Пустой CAT_name
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('3', 'Сон', '120', '2021.05.17', 'Отдых') -- Смена USER_ID.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('1', 'Летал во сне', '120', '2021.05.17', 'Отдых') -- Смена ACTL_name.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('1', 'Сон', '666', '2021.05.17', 'Отдых') -- Смена DATE_value.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, TIME_value, DATE_value, CAT_name) VALUES ('1', 'Бег', '120', '2000.01.01', 'Отдых') -- Смена CAT_name.

SELECT * FROM "ACTIVITY"                         -- Проверяем таблицу COMMENT.



------------------------------
-- Создаем таблицу COMMENT --
------------------------------
CREATE TABLE "COMMENT"(                         -- Создаем таблицу.
	ACT_ID INT NOT NULL PRIMARY KEY REFERENCES "ACTIVITY" (ACT_ID) ON DELETE CASCADE ON UPDATE CASCADE, -- Создаем числовой столбец, это ключ🔑, обязательно для заполнения, каскадная связь с таблицей.
	COM_value TEXT                              -- Создаем текстовый столбец.
);

-- Добавляем немного данных в таблицу COMMENT.
INSERT INTO "COMMENT" (ACT_ID, COM_value) VALUES ('2', ''), ('3', 'Тестовый комментарий')

INSERT INTO "COMMENT" (ACT_ID, COM_value) VALUES ('1', 'Тестовый комментарий') -- Проверка на уникальность текста.
INSERT INTO "COMMENT" (ACT_ID, COM_value) VALUES ('3', 'Новый комментарий')    -- Проверка на замену текста.

SELECT * FROM "COMMENT"                         -- Проверяем таблицу COMMENT.


DROP TABLE "COMMENT" ;
DROP TABLE "ACTIVITY" ;
DROP TABLE "DATE" ;
DROP TABLE "TIME" ;
DROP TABLE "ACTIVITY_LIST" ;
DROP TABLE "CATEGORY" ;
DROP TABLE "SETTINGS" ;
DROP TABLE "USER" ;
 