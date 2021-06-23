-- Экспорт данных о пользователе USER_ID = 1 таблица USER
COPY (SELECT *  FROM "USER" WHERE USER_ID = 1)
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/USER.csv' (format CSV);


-- Экспорт данных о пользователе USER_N_ID = '996MdkMfxhWRZTD8G0F3' таблица USER_NAME
COPY (SELECT *  FROM "USER_NAME" WHERE USER_N_ID = '996MdkMfxhWRZTD8G0F3')
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/USER_NAME.csv' (format CSV);


-- Экспорт данных о пользователе USER_P_ID = 'udP1PlxlVqsWO0N99aVA' таблица USER_PRIVATE
COPY (SELECT * FROM "USER_PRIVATE" WHERE USER_P_ID = 'udP1PlxlVqsWO0N99aVA')
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/USER_PRIVATE.csv' (format CSV);


-- Экспорт данных о пользователе USER_ID = 1 таблица SETTINGS
COPY (SELECT * FROM "SETTINGS" WHERE USER_ID = 1)
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/USER_PRIVATE.csv' (format CSV);


-- Экспорт данных о пользователе USER_ID = 1 таблица CATEGORY
COPY (SELECT "USER".USER_ID , CAT_NAME  FROM "USER"
      LEFT JOIN "CATEGORY" ON "USER".USER_ID="CATEGORY".USER_ID WHERE "USER".USER_ID = 1)
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/CATEGORY.csv' (format CSV);


-- Экспорт данных о пользователе USER_ID = 1 таблица ACTIVITY_LIST
COPY (SELECT "USER".USER_ID, ACTL_NAME,  CAT_NAME   
      FROM "USER"  LEFT JOIN "ACTIVITY_LIST" ON "USER".USER_ID="ACTIVITY_LIST".USER_ID
      WHERE "USER".USER_ID = 1) 
TO 'C:\Users\Game-PC\Desktop\Proekt\neew/ACTIVITY_LIST.csv' (format CSV);


-- Экспорт данных о пользователе USER_ID = 1 таблица ACTIVITY.
COPY (SELECT "USER".USER_ID, ACTL_NAME, ACT_TIME, ACT_DATE, CAT_NAME, ACT_COMMENT
      FROM "USER" LEFT JOIN "ACTIVITY" ON "USER".USER_ID="ACTIVITY".USER_ID
      WHERE "USER".USER_ID = 1
      TO 'C:\Users\Game-PC\Desktop\Proekt\neew\ACTIVITYFJGHJY.csv' (format CSV);
