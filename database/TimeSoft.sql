PGDMP                         y            TimeSoft    10.17    10.17 1    7           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            8           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            9           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            :           1262    16393    TimeSoft    DATABASE     �   CREATE DATABASE "TimeSoft" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
    DROP DATABASE "TimeSoft";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            ;           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            <           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16434    ACTIVITY    TABLE     �   CREATE TABLE public."ACTIVITY" (
    act_id integer NOT NULL,
    "USER_ID" integer,
    actl_name text,
    time_value integer,
    date_value date,
    cat_name text
);
    DROP TABLE public."ACTIVITY";
       public         postgres    false    3            �            1259    16416    ACTIVITY_LIST    TABLE     �   CREATE TABLE public."ACTIVITY_LIST" (
    actl_id integer NOT NULL,
    "USER_ID" integer NOT NULL,
    actl_name text NOT NULL,
    cat_name text NOT NULL
);
 #   DROP TABLE public."ACTIVITY_LIST";
       public         postgres    false    3            �            1259    16414    ACTIVITY_LIST_actl_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY_LIST" ALTER COLUMN actl_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_LIST_actl_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    201    3            �            1259    16432    ACTIVITY_act_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY" ALTER COLUMN act_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_act_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    3    204            �            1259    16406    CATEGORY    TABLE     |   CREATE TABLE public."CATEGORY" (
    cat_id integer NOT NULL,
    "USER_ID" integer NOT NULL,
    cat_name text NOT NULL
);
    DROP TABLE public."CATEGORY";
       public         postgres    false    3            �            1259    16404    CATEGORY_cat_id_seq    SEQUENCE     �   ALTER TABLE public."CATEGORY" ALTER COLUMN cat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."CATEGORY_cat_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    3    199            �            1259    16460    DATE    TABLE     [   CREATE TABLE public."DATE" (
    date_id integer NOT NULL,
    date_value date NOT NULL
);
    DROP TABLE public."DATE";
       public         postgres    false    3            �            1259    16458    DATE_date_id_seq    SEQUENCE     �   ALTER TABLE public."DATE" ALTER COLUMN date_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."DATE_date_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    209    3            �            1259    16424    SETTINGS    TABLE     �   CREATE TABLE public."SETTINGS" (
    "USER_ID" integer NOT NULL,
    set_theme text,
    set_period text,
    set_measure text
);
    DROP TABLE public."SETTINGS";
       public         postgres    false    3            �            1259    16452    TIME    TABLE     ^   CREATE TABLE public."TIME" (
    time_id integer NOT NULL,
    time_value integer NOT NULL
);
    DROP TABLE public."TIME";
       public         postgres    false    3            �            1259    16450    TIME_time_id_seq    SEQUENCE     �   ALTER TABLE public."TIME" ALTER COLUMN time_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."TIME_time_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    207    3            �            1259    16396    USER    TABLE     �   CREATE TABLE public."USER" (
    user_id integer NOT NULL,
    user_name character(20) NOT NULL,
    user_email character(64) NOT NULL,
    user_password character(64) NOT NULL,
    user_telegram character(64)
);
    DROP TABLE public."USER";
       public         postgres    false    3            �            1259    16394    USER_user_id_seq    SEQUENCE     �   ALTER TABLE public."USER" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."USER_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    197    3            �            1259    16442    comment    TABLE     Q   CREATE TABLE public.comment (
    act_id integer NOT NULL,
    com_value text
);
    DROP TABLE public.comment;
       public         postgres    false    3            /          0    16434    ACTIVITY 
   TABLE DATA               d   COPY public."ACTIVITY" (act_id, "USER_ID", actl_name, time_value, date_value, cat_name) FROM stdin;
    public       postgres    false    204   �1       ,          0    16416    ACTIVITY_LIST 
   TABLE DATA               R   COPY public."ACTIVITY_LIST" (actl_id, "USER_ID", actl_name, cat_name) FROM stdin;
    public       postgres    false    201   �1       *          0    16406    CATEGORY 
   TABLE DATA               A   COPY public."CATEGORY" (cat_id, "USER_ID", cat_name) FROM stdin;
    public       postgres    false    199   �1       4          0    16460    DATE 
   TABLE DATA               5   COPY public."DATE" (date_id, date_value) FROM stdin;
    public       postgres    false    209   �1       -          0    16424    SETTINGS 
   TABLE DATA               S   COPY public."SETTINGS" ("USER_ID", set_theme, set_period, set_measure) FROM stdin;
    public       postgres    false    202   2       2          0    16452    TIME 
   TABLE DATA               5   COPY public."TIME" (time_id, time_value) FROM stdin;
    public       postgres    false    207   02       (          0    16396    USER 
   TABLE DATA               ^   COPY public."USER" (user_id, user_name, user_email, user_password, user_telegram) FROM stdin;
    public       postgres    false    197   M2       0          0    16442    comment 
   TABLE DATA               4   COPY public.comment (act_id, com_value) FROM stdin;
    public       postgres    false    205   j2       =           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."ACTIVITY_LIST_actl_id_seq"', 1, false);
            public       postgres    false    200            >           0    0    ACTIVITY_act_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."ACTIVITY_act_id_seq"', 1, false);
            public       postgres    false    203            ?           0    0    CATEGORY_cat_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."CATEGORY_cat_id_seq"', 1, false);
            public       postgres    false    198            @           0    0    DATE_date_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."DATE_date_id_seq"', 1, false);
            public       postgres    false    208            A           0    0    TIME_time_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."TIME_time_id_seq"', 1, false);
            public       postgres    false    206            B           0    0    USER_user_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."USER_user_id_seq"', 1, false);
            public       postgres    false    196            �
           2606    16423     ACTIVITY_LIST ACTIVITY_LIST_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_pkey" PRIMARY KEY ("USER_ID", actl_name, cat_name);
 N   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_pkey";
       public         postgres    false    201    201    201            �
           2606    16441    ACTIVITY ACTIVITY_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_pkey" PRIMARY KEY (act_id);
 D   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_pkey";
       public         postgres    false    204            �
           2606    16413    CATEGORY CATEGORY_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_pkey" PRIMARY KEY ("USER_ID", cat_name);
 D   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_pkey";
       public         postgres    false    199    199            �
           2606    16464    DATE DATE_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."DATE"
    ADD CONSTRAINT "DATE_pkey" PRIMARY KEY (date_value);
 <   ALTER TABLE ONLY public."DATE" DROP CONSTRAINT "DATE_pkey";
       public         postgres    false    209            �
           2606    16431    SETTINGS SETTINGS_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_pkey" PRIMARY KEY ("USER_ID");
 D   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_pkey";
       public         postgres    false    202            �
           2606    16456    TIME TIME_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."TIME"
    ADD CONSTRAINT "TIME_pkey" PRIMARY KEY (time_value);
 <   ALTER TABLE ONLY public."TIME" DROP CONSTRAINT "TIME_pkey";
       public         postgres    false    207            �
           2606    16400    USER USER_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (user_id);
 <   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_pkey";
       public         postgres    false    197            �
           2606    16449    comment comment_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (act_id);
 >   ALTER TABLE ONLY public.comment DROP CONSTRAINT comment_pkey;
       public         postgres    false    205            �
           1259    16465    datee    INDEX     E   CREATE UNIQUE INDEX datee ON public."DATE" USING btree (date_value);
    DROP INDEX public.datee;
       public         postgres    false    209            �
           1259    16457    timee    INDEX     E   CREATE UNIQUE INDEX timee ON public."TIME" USING btree (time_value);
    DROP INDEX public.timee;
       public         postgres    false    207            �
           1259    16402    user_emaill    INDEX     K   CREATE UNIQUE INDEX user_emaill ON public."USER" USING btree (user_email);
    DROP INDEX public.user_emaill;
       public         postgres    false    197            �
           1259    16401 
   user_namee    INDEX     I   CREATE UNIQUE INDEX user_namee ON public."USER" USING btree (user_name);
    DROP INDEX public.user_namee;
       public         postgres    false    197            �
           1259    16403    user_telegramm    INDEX     Q   CREATE UNIQUE INDEX user_telegramm ON public."USER" USING btree (user_telegram);
 "   DROP INDEX public.user_telegramm;
       public         postgres    false    197            /      x������ � �      ,      x������ � �      *      x������ � �      4      x������ � �      -      x������ � �      2      x������ � �      (      x������ � �      0      x������ � �     