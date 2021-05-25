
-- Вывод информации по пользователю в заданом промежутке времени с нужными нам таблицами
SELECT ACT_TIME, ACT_DATE, CAT_NAME FROM "ACTIVITY" WHERE  ACT_DATE  BETWEEN '2021.04.01' AND '2021.04.30' AND USER_ID = '1'
-- /