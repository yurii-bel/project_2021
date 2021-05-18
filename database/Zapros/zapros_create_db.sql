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

------------------------------
-- Создаем таблицу SETTINGS --
------------------------------
CREATE TABLE "SETTINGS"(                     -- Создаем таблицу.
	USER_ID INT NOT NULL PRIMARY KEY REFERENCES "USER" (USER_ID) ON DELETE CASCADE ON UPDATE CASCADE, -- Создаем числовой столбец, это ключ🔑, обязательно для заполнения, каскадная связь с таблицей.
	SET_theme TEXT NULL,                     -- Создаем текстовый столбец.
	SET_preferences TEXT NULL                -- Создаем текстовый столбец.
);

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

-----------------------------------
-- Создаем таблицу ACTIVITY_LIST --
-----------------------------------
CREATE TABLE "ACTIVITY_LIST"(                -- Создаем таблицу.
	ACTL_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY,   -- Создаем числовой столбец, подключаем счетчик.
	USER_ID INT NOT NULL,                    -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,          -- Создаем текстовый столбец, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,           -- Создаем текстовый столбец, обязательно для заполнения.
	FOREIGN KEY (USER_ID, CAT_name)	REFERENCES "CATEGORY" (USER_ID, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE, -- Указываем на связь с другой талблицей.
	PRIMARY KEY (USER_ID, ACTL_name, CAT_name), -- Указываем где ключи🔑.
	UNIQUE (USER_ID, ACTL_name, CAT_name)       -- Указываем где уникальное значение обязательно, зависит от всех перечисленных столбцов.
);

------------------------------
-- Создаем таблицу ACTIVITY --
------------------------------
CREATE TABLE "ACTIVITY"(                        -- Создаем таблицу.
	ACT_ID INT NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Создаем числовой столбец, подключаем счетчик, это ключ🔑.
	USER_ID INT NOT NULL,                       -- Создаем числовой столбец, обязательно для заполнения.
	ACTL_name VARCHAR(64) NOT NULL,             -- Создаем текстовый столбец, обязательно для заполнения.
	ACT_time INT NOT NULL,                      -- Создаем числовой столбец, обязательно для заполнения.
	ACT_date DATE NOT NULL,                     -- Создаем столбец даты, обязательно для заполнения.
	CAT_name VARCHAR(64) NOT NULL,              -- Создаем текстовый столбец, обязательно для заполнения.
	ACT_comment TEXT NULL,                           -- Создаем текстовый столбец.
	FOREIGN KEY (USER_ID, ACTL_name, CAT_name) REFERENCES "ACTIVITY_LIST" (USER_ID, ACTL_name, CAT_name) ON DELETE CASCADE ON UPDATE CASCADE -- Указываем на связь с другой талблицей.
);
