-- Ошибки!
-- Исправить "USER_NAME"(USER_Telegram) Вернуть уникальность!
-- Не проходим проверку уникальности по регистру.


--------------------------
-- Создаем таблицу USER --
--------------------------
CREATE TABLE "USER"(                         -- Создаем таблицу.
	USER_ID SERIAL NOT NULL UNIQUE,          -- Создаем числовой столбец счетчик, не пустой, уникальное значение.
	USER_N_ID VARCHAR (64) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения.
	USER_P_ID VARCHAR (64) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения.
	PRIMARY KEY (USER_ID, USER_N_ID, USER_P_ID) -- Указываем где ключи🔑.
);

-- Добавляем немного данных в таблицу USER.
INSERT INTO "USER" (USER_N_ID, USER_P_ID) VALUES ('N1', 'P1'), ('N2', 'P2'), ('N3', 'P3'), ('N4', 'P4'), ('N5', 'P5')

-- Проводим проверку корректности ввода в таблицу USER.
INSERT INTO "USER" (USER_N_ID, USER_P_ID) VALUES ('N2', 'P9') -- Проверка уникальности USER_N_ID.
INSERT INTO "USER" (USER_N_ID, USER_P_ID) VALUES ('N9', 'P2') -- Проверка уникальности USER_P_ID.
INSERT INTO "USER" (USER_N_ID, USER_P_ID) VALUES ('n2', 'p2') -- Проверка уникальности по регистру. !! - Ошибка - !!

SELECT * FROM "USER"                         -- Проверяем таблицу USER.

-------------------------------
-- Создаем таблицу USER_NAME --
-------------------------------
CREATE TABLE "USER_NAME"(                    -- Создаем таблицу.
	USER_N_ID VARCHAR (64) NOT NULL UNIQUE REFERENCES "USER" (USER_N_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем текстовый столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	USER_N_name VARCHAR (64) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение.
	USER_N_Telegram VARCHAR (64) NULL          -- Создаем текстовый столбец.
);

-- Добавляем немного данных в таблицу USER_NAME.
INSERT INTO "USER_NAME" (USER_N_ID, USER_N_name, USER_N_Telegram) VALUES ('N1', 'Sif', 'qwerty:Telegram'), ('N2', 'NO-Sif', '')

-- Проводим проверку корректности ввода в таблицу USER_NAME.
INSERT INTO "USER_NAME" (USER_N_ID, USER_N_name, USER_N_Telegram) VALUES ('N9', 'Sim', 'qwerty:TelegramSim') -- Проверка несуществующего USER_N_ID.
INSERT INTO "USER_NAME" (USER_N_ID, USER_N_name, USER_N_Telegram) VALUES ('N5', 'Sif', '') -- Проверка уникальности USER_N_name.
INSERT INTO "USER_NAME" (USER_N_ID, USER_N_name, USER_N_Telegram) VALUES ('N5', 'SIF', '') -- Проверка уникальности по регистру. !! - Ошибка - !!

SELECT * FROM "USER_NAME"                    -- Проверяем таблицу USER_NAME.

---------------------------------
-- Создаем таблицу USER_PRIVAT --
---------------------------------
CREATE TABLE "USER_PRIVAT"(                  -- Создаем таблицу.
	USER_P_ID VARCHAR (64) NOT NULL UNIQUE REFERENCES "USER" (USER_P_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем текстовый столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	USER_P_email VARCHAR (64) NOT NULL UNIQUE, -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение.
	USER_P_password VARCHAR (64) NOT NULL      -- Создаем текстовый столбец, обязательно для заполнения.
);

-- Добавляем немного данных в таблицу USER_PRIVAT.
INSERT INTO "USER_PRIVAT" (USER_P_ID, USER_P_email, USER_P_password) VALUES ('P1', 'Sif@gmail.ua', 'qwerty'), ('P2', 'NO-Sif@gmail.ua', 'qwerty')

-- Проводим проверку корректности ввода в таблицу USER_PRIVAT.
INSERT INTO "USER_PRIVAT" (USER_P_ID, USER_P_email, USER_P_password) VALUES ('P9', 'oldil@email.su', 'qwerty') -- Проверка уникальности USER_P_ID.
INSERT INTO "USER_PRIVAT" (USER_P_ID, USER_P_email, USER_P_password) VALUES ('P3', 'Sif@gmail.ua', 'qwerty')   -- Проверка уникальности USER_P_email.
INSERT INTO "USER_PRIVAT" (USER_P_ID, USER_P_email, USER_P_password) VALUES ('P4', 'EMAIL@GMAIL.UA', 'qwerty') -- Проверка уникальности по регистру. !! - Ошибка - !!

SELECT * FROM "USER_PRIVAT"                  -- Проверяем таблицу USER.

------------------------------
-- Создаем таблицу SETTINGS --
------------------------------
CREATE TABLE "SETTINGS"(                     -- Создаем таблицу.
	USER_ID INT NOT NULL REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем числовой столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	SET_theme TEXT NULL,                     -- Создаем текстовый столбец.
	SET_preferences TEXT NULL                -- Создаем текстовый столбец.
);

-- Проводим проверку корректности ввода в таблицу SETTINGS.
INSERT INTO "SETTINGS" (USER_ID, SET_theme, SET_preferences) VALUES ('1', 'Моя личная тема', 'Мои предпочтения')

SELECT * FROM "SETTINGS"                     -- Проверяем таблицу SETTINGS.

------------------------------
-- Создаем таблицу CATEGORY --
------------------------------
CREATE TABLE "CATEGORY"(                     -- Создаем таблицу.
	CAT_ID SERIAL NOT NULL UNIQUE,           -- Создаем числовой столбец счетчик, не пустой, уникальное значение.
	USER_ID INT NOT NULL REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE,  -- создаем числовой столбец, обязательно для заполнения, каскадная связь с таблицей.
	CAT_name VARCHAR (64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	PRIMARY KEY (USER_ID, CAT_name),         -- Указываем где ключи🔑.
	UNIQUE (USER_ID, CAT_name)               -- Указываем где уникальное значение, зависит от всех перечисленных столбцов.
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
	ACTL_ID SERIAL NOT NULL UNIQUE,          -- Создаем числовой столбец счетчик, не пустой, уникальное значение.
	USER_ID INT NOT NULL,                    -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,           -- Создаем текстовый столбец, обязательно для заполнения.
	FOREIGN KEY (USER_ID, CAT_name)	REFERENCES "CATEGORY" (USER_ID, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE, -- Указываем на связь с другой талблицей.
	PRIMARY KEY (USER_ID, ACTL_name, CAT_name), -- Указываем где ключи🔑.
	UNIQUE (USER_ID, ACTL_name, CAT_name)    -- Указываем где уникальное значение, зависит от всех перечисленных столбцов.
);

-- Добавляем немного данных в таблицу ACTIVITY_LIST.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('1', 'Сон', 'Отдых'), ('1', 'Бег', 'Спорт'), ('2', 'Сон', 'Отдых'), ('2', 'Чтение', 'Обучение')

-- Проводим проверку корректности ввода в таблицу ACTIVITY_LIST.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('2', 'Создание БД', 'Работа')  -- Проверяем связь USER_ID и CAT_name.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('2', 'Небывалое', 'Небывалое') -- Проверяем на CAT_name.
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('9', 'Сон', 'Отдых')           -- Проверяем на уникальность USER_ID. 
INSERT INTO "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) VALUES ('1', 'Сон', 'Отдых')           -- Проверяем на повторный ввод.

SELECT * FROM "ACTIVITY_LIST"                -- Проверяем таблицу ACTIVITY_LIST.

------------------------------
-- Создаем таблицу ACTIVITY --
------------------------------
CREATE TABLE "ACTIVITY"(                     -- Создаем таблицу.
	ACT_ID SERIAL NOT NULL UNIQUE PRIMARY KEY, -- Создаем числовой столбец счетчик, не пустой, уникальное значение, это ключ🔑.
	USER_ID INT NOT NULL,                    -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	ACT_time INT NOT NULL,                   -- Создаем числовой столбец, обязательно для заполнения.
	ACT_date DATE NOT NULL,                  -- Создаем столбец даты, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,           -- Создаем текстовый столбец, обязательно для заполнения.
	ACT_comment TEXT NULL,                   -- Создаем текстовый столбец.
	FOREIGN KEY (USER_ID, ACTL_name, CAT_name) REFERENCES "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE -- Указываем на связь с другой талблицей.
);

-- Добавляем немного данных в таблицу COMMENT.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES 
('1', 'Сон', '120', '2021.05.17', 'Отдых', ''),
('1', 'Бег', '30', '2021.5.10', 'Спорт', 'Тестовая запись'),
('2', 'Сон', '50', '9.5.2021', 'Отдых', 'Тестовая запись')

-- Проводим проверку корректности ввода в таблицу COMMENT.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('', 'Сон', '120', '2021.05.17', 'Отдых', '')  -- Пустой USER_ID
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('2', '', '120', '2021.05.17', 'Отдых', '')    -- Пустой ACTL_name
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('2', 'Сон', '', '2021.05.17', 'Отдых', '')    -- Пустой TIME_value
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('2', 'Бег', '120', '', 'Отдых', '')           -- Пустой DATE_value
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('2', 'Сон', '120', '2021.05.17', '', '')      -- Пустой CAT_name
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('3', 'Сон', '120', '2021.05.17', 'Отдых', '') -- Смена USER_ID.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('1', 'Летал во сне', '120', '2021.05.17', 'Отдых', '')       -- Смена ACTL_name.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('1', 'Бег', '120', '2000.01.01', 'Отдых', '') -- Смена CAT_name.
INSERT INTO "ACTIVITY" (USER_ID, ACTL_name, ACT_time, ACT_date, CAT_name, ACT_comment) VALUES ('1', 'Бег', '120', '2000.01.01', 'Отдых', 'Тестовая запись') -- Смена ACT_comment.

SELECT * FROM "ACTIVITY"                     -- Проверяем таблицу COMMENT.

-- Удаление таблиц в черезвычайной ситуации.
DROP TABLE "ACTIVITY" ;
DROP TABLE "ACTIVITY_LIST" ;
DROP TABLE "CATEGORY" ;
DROP TABLE "SETTINGS" ;
DROP TABLE "USER_NAME" ;
DROP TABLE "USER_PRIVAT" ;
DROP TABLE "USER" ;
