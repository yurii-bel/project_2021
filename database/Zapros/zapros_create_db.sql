-- Ошибки!
-- Исправить "USER_NAME"(USER_Telegram) Вернуть уникальность!
-- Не проходим проверки уникальности по регистру.


--------------------------
-- Создаем таблицу USER --
--------------------------
CREATE TABLE "USER"(                         -- Создаем таблицу.
	USER_ID SERIAL NOT NULL UNIQUE,          -- Создаем числовой столбец счетчик, не пустой, уникальное значение.
	USER_N_ID VARCHAR (40) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения.
	USER_P_ID VARCHAR (40) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения.
	PRIMARY KEY (USER_ID, USER_N_ID, USER_P_ID) -- Указываем где ключи🔑.
);

-------------------------------
-- Создаем таблицу USER_NAME --
-------------------------------
CREATE TABLE "USER_NAME"(                    -- Создаем таблицу.
	USER_N_ID VARCHAR (40) NOT NULL UNIQUE REFERENCES "USER" (USER_N_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем текстовый столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	USER_name VARCHAR (32) NOT NULL UNIQUE,  -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение.
	USER_Telegram VARCHAR (40) NULL          -- Создаем текстовый столбец.
);

---------------------------------
-- Создаем таблицу USER_PRIVAT --
---------------------------------
CREATE TABLE "USER_PRIVAT"(                  -- Создаем таблицу.
	USER_P_ID VARCHAR (40) NOT NULL UNIQUE REFERENCES "USER" (USER_P_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем текстовый столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	USER_email VARCHAR (64) NOT NULL UNIQUE, -- Создаем текстовый столбец, обязательно для заполнения, уникальное значение.
	USER_password VARCHAR (64) NOT NULL      -- Создаем текстовый столбец, обязательно для заполнения.
);

------------------------------
-- Создаем таблицу SETTINGS --
------------------------------
CREATE TABLE "SETTINGS"(                     -- Создаем таблицу.
	USER_ID INT NOT NULL REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY, -- Создаем числовой столбец, обязательно для заполнения, каскадная связь с таблицей, это ключ🔑.
	SET_theme TEXT NULL,                     -- Создаем текстовый столбец.
	SET_preferences TEXT NULL                -- Создаем текстовый столбец.
);

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
