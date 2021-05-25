
-- Вывод информации по пользователю в заданом промежутке даты с нужными нам таблицами а так же можно использовать для построения графика
SELECT ACT_TIME, ACT_DATE, CAT_NAME FROM "ACTIVITY" WHERE  ACT_DATE  BETWEEN '2021.04.01' AND '2021.04.30' AND USER_ID = '1'
-- /
