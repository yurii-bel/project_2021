PGDMP     1                    y            TimeSoft    10.17    10.17 B    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false            O           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false            P           1262    16393    TimeSoft    DATABASE     �   CREATE DATABASE "TimeSoft" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
    DROP DATABASE "TimeSoft";
             postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
             postgres    false            Q           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                  postgres    false    3                        3079    12924    plpgsql 	   EXTENSION     ?   CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
    DROP EXTENSION plpgsql;
                  false            R           0    0    EXTENSION plpgsql    COMMENT     @   COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
                       false    1            �            1259    16828    ACTIVITY    TABLE     �   CREATE TABLE public."ACTIVITY" (
    act_id integer NOT NULL,
    user_id integer,
    actl_name text,
    time_value integer,
    date_value date,
    cat_name text
);
    DROP TABLE public."ACTIVITY";
       public         postgres    false    3            �            1259    16745    ACTIVITY_LIST    TABLE     �   CREATE TABLE public."ACTIVITY_LIST" (
    actl_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name text NOT NULL,
    cat_name text NOT NULL
);
 #   DROP TABLE public."ACTIVITY_LIST";
       public         postgres    false    3            �            1259    16743    ACTIVITY_LIST_actl_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY_LIST" ALTER COLUMN actl_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_LIST_actl_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    206    3            �            1259    16826    ACTIVITY_act_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY" ALTER COLUMN act_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_act_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    208    3            �            1259    16622    CATEGORY    TABLE     z   CREATE TABLE public."CATEGORY" (
    cat_id integer NOT NULL,
    user_id integer NOT NULL,
    cat_name text NOT NULL
);
    DROP TABLE public."CATEGORY";
       public         postgres    false    3            �            1259    16620    CATEGORY_cat_id_seq    SEQUENCE     �   ALTER TABLE public."CATEGORY" ALTER COLUMN cat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."CATEGORY_cat_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    200    3            �            1259    16866    COMMENT    TABLE     S   CREATE TABLE public."COMMENT" (
    act_id integer NOT NULL,
    com_value text
);
    DROP TABLE public."COMMENT";
       public         postgres    false    3            �            1259    16699    DATE    TABLE     [   CREATE TABLE public."DATE" (
    date_id integer NOT NULL,
    date_value date NOT NULL
);
    DROP TABLE public."DATE";
       public         postgres    false    3            �            1259    16697    DATE_date_id_seq    SEQUENCE     �   ALTER TABLE public."DATE" ALTER COLUMN date_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."DATE_date_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    204    3            �            1259    16501    SETTINGS    TABLE     �   CREATE TABLE public."SETTINGS" (
    user_id integer NOT NULL,
    set_theme text,
    set_period text,
    set_measure text
);
    DROP TABLE public."SETTINGS";
       public         postgres    false    3            �            1259    16691    TIME    TABLE     ^   CREATE TABLE public."TIME" (
    time_id integer NOT NULL,
    time_value integer NOT NULL
);
    DROP TABLE public."TIME";
       public         postgres    false    3            �            1259    16689    TIME_time_id_seq    SEQUENCE     �   ALTER TABLE public."TIME" ALTER COLUMN time_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."TIME_time_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    202    3            �            1259    16480    USER    TABLE     �   CREATE TABLE public."USER" (
    user_id integer NOT NULL,
    user_name character(20) NOT NULL,
    user_email character(64) NOT NULL,
    user_password character(64) NOT NULL,
    user_telegram character(64)
);
    DROP TABLE public."USER";
       public         postgres    false    3            �            1259    16478    USER_user_id_seq    SEQUENCE     �   ALTER TABLE public."USER" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."USER_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public       postgres    false    197    3            I          0    16828    ACTIVITY 
   TABLE DATA               b   COPY public."ACTIVITY" (act_id, user_id, actl_name, time_value, date_value, cat_name) FROM stdin;
    public       postgres    false    208   �L       G          0    16745    ACTIVITY_LIST 
   TABLE DATA               P   COPY public."ACTIVITY_LIST" (actl_id, user_id, actl_name, cat_name) FROM stdin;
    public       postgres    false    206   M       A          0    16622    CATEGORY 
   TABLE DATA               ?   COPY public."CATEGORY" (cat_id, user_id, cat_name) FROM stdin;
    public       postgres    false    200   6M       J          0    16866    COMMENT 
   TABLE DATA               6   COPY public."COMMENT" (act_id, com_value) FROM stdin;
    public       postgres    false    209   SM       E          0    16699    DATE 
   TABLE DATA               5   COPY public."DATE" (date_id, date_value) FROM stdin;
    public       postgres    false    204   pM       ?          0    16501    SETTINGS 
   TABLE DATA               Q   COPY public."SETTINGS" (user_id, set_theme, set_period, set_measure) FROM stdin;
    public       postgres    false    198   �M       C          0    16691    TIME 
   TABLE DATA               5   COPY public."TIME" (time_id, time_value) FROM stdin;
    public       postgres    false    202   �M       >          0    16480    USER 
   TABLE DATA               ^   COPY public."USER" (user_id, user_name, user_email, user_password, user_telegram) FROM stdin;
    public       postgres    false    197   �M       S           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."ACTIVITY_LIST_actl_id_seq"', 1, false);
            public       postgres    false    205            T           0    0    ACTIVITY_act_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."ACTIVITY_act_id_seq"', 1, false);
            public       postgres    false    207            U           0    0    CATEGORY_cat_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."CATEGORY_cat_id_seq"', 1, false);
            public       postgres    false    199            V           0    0    DATE_date_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."DATE_date_id_seq"', 1, false);
            public       postgres    false    203            W           0    0    TIME_time_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."TIME_time_id_seq"', 1, false);
            public       postgres    false    201            X           0    0    USER_user_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."USER_user_id_seq"', 1, false);
            public       postgres    false    196            �
           2606    16756 )   ACTIVITY_LIST ACTIVITY_LIST_actl_name_key 
   CONSTRAINT     m   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_actl_name_key" UNIQUE (actl_name);
 W   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_actl_name_key";
       public         postgres    false    206            �
           2606    16758 (   ACTIVITY_LIST ACTIVITY_LIST_cat_name_key 
   CONSTRAINT     k   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_cat_name_key" UNIQUE (cat_name);
 V   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_cat_name_key";
       public         postgres    false    206            �
           2606    16752     ACTIVITY_LIST ACTIVITY_LIST_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_pkey" PRIMARY KEY (user_id, actl_name, cat_name);
 N   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_pkey";
       public         postgres    false    206    206    206            �
           2606    16754 '   ACTIVITY_LIST ACTIVITY_LIST_user_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_key" UNIQUE (user_id);
 U   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_key";
       public         postgres    false    206            �
           2606    16835    ACTIVITY ACTIVITY_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_pkey" PRIMARY KEY (act_id);
 D   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_pkey";
       public         postgres    false    208            �
           2606    16633    CATEGORY CATEGORY_cat_name_key 
   CONSTRAINT     a   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_cat_name_key" UNIQUE (cat_name);
 L   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_cat_name_key";
       public         postgres    false    200            �
           2606    16629    CATEGORY CATEGORY_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_pkey" PRIMARY KEY (user_id, cat_name);
 D   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_pkey";
       public         postgres    false    200    200            �
           2606    16631    CATEGORY CATEGORY_user_id_key 
   CONSTRAINT     _   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_user_id_key" UNIQUE (user_id);
 K   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_user_id_key";
       public         postgres    false    200            �
           2606    16873    COMMENT COMMENT_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public."COMMENT"
    ADD CONSTRAINT "COMMENT_pkey" PRIMARY KEY (act_id);
 B   ALTER TABLE ONLY public."COMMENT" DROP CONSTRAINT "COMMENT_pkey";
       public         postgres    false    209            �
           2606    16703    DATE DATE_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."DATE"
    ADD CONSTRAINT "DATE_pkey" PRIMARY KEY (date_value);
 <   ALTER TABLE ONLY public."DATE" DROP CONSTRAINT "DATE_pkey";
       public         postgres    false    204            �
           2606    16508    SETTINGS SETTINGS_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_pkey" PRIMARY KEY (user_id);
 D   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_pkey";
       public         postgres    false    198            �
           2606    16695    TIME TIME_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."TIME"
    ADD CONSTRAINT "TIME_pkey" PRIMARY KEY (time_value);
 <   ALTER TABLE ONLY public."TIME" DROP CONSTRAINT "TIME_pkey";
       public         postgres    false    202            �
           2606    16484    USER USER_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (user_id);
 <   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_pkey";
       public         postgres    false    197            �
           1259    16704    datee    INDEX     E   CREATE UNIQUE INDEX datee ON public."DATE" USING btree (date_value);
    DROP INDEX public.datee;
       public         postgres    false    204            �
           1259    16696    timee    INDEX     E   CREATE UNIQUE INDEX timee ON public."TIME" USING btree (time_value);
    DROP INDEX public.timee;
       public         postgres    false    202            �
           1259    16486    user_emaill    INDEX     K   CREATE UNIQUE INDEX user_emaill ON public."USER" USING btree (user_email);
    DROP INDEX public.user_emaill;
       public         postgres    false    197            �
           1259    16485 
   user_namee    INDEX     I   CREATE UNIQUE INDEX user_namee ON public."USER" USING btree (user_name);
    DROP INDEX public.user_namee;
       public         postgres    false    197            �
           1259    16487    user_telegramm    INDEX     Q   CREATE UNIQUE INDEX user_telegramm ON public."USER" USING btree (user_telegram);
 "   DROP INDEX public.user_telegramm;
       public         postgres    false    197            �
           2606    16769 )   ACTIVITY_LIST ACTIVITY_LIST_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_cat_name_fkey" FOREIGN KEY (cat_name) REFERENCES public."CATEGORY"(cat_name);
 W   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_cat_name_fkey";
       public       postgres    false    200    206    2721            �
           2606    16759 (   ACTIVITY_LIST ACTIVITY_LIST_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 V   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_fkey";
       public       postgres    false    206    197    2714            �
           2606    16764 )   ACTIVITY_LIST ACTIVITY_LIST_user_id_fkey1    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_fkey1" FOREIGN KEY (user_id) REFERENCES public."CATEGORY"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 W   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_fkey1";
       public       postgres    false    200    2725    206            �
           2606    16846     ACTIVITY ACTIVITY_actl_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_actl_name_fkey" FOREIGN KEY (actl_name) REFERENCES public."ACTIVITY_LIST"(actl_name) ON UPDATE CASCADE ON DELETE CASCADE;
 N   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_actl_name_fkey";
       public       postgres    false    206    208    2733            �
           2606    16861    ACTIVITY ACTIVITY_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_cat_name_fkey" FOREIGN KEY (cat_name) REFERENCES public."ACTIVITY_LIST"(cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 M   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_cat_name_fkey";
       public       postgres    false    208    2735    206            �
           2606    16856 !   ACTIVITY ACTIVITY_date_value_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_date_value_fkey" FOREIGN KEY (date_value) REFERENCES public."DATE"(date_value) ON UPDATE CASCADE ON DELETE CASCADE;
 O   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_date_value_fkey";
       public       postgres    false    2730    204    208            �
           2606    16851 !   ACTIVITY ACTIVITY_time_value_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_time_value_fkey" FOREIGN KEY (time_value) REFERENCES public."TIME"(time_value) ON UPDATE CASCADE ON DELETE CASCADE;
 O   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_time_value_fkey";
       public       postgres    false    202    2727    208            �
           2606    16836    ACTIVITY ACTIVITY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_fkey";
       public       postgres    false    2714    197    208            �
           2606    16841    ACTIVITY ACTIVITY_user_id_fkey1    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_fkey1" FOREIGN KEY (user_id) REFERENCES public."ACTIVITY_LIST"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 M   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_fkey1";
       public       postgres    false    2739    206    208            �
           2606    16634    CATEGORY CATEGORY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_user_id_fkey";
       public       postgres    false    2714    200    197            �
           2606    16874    COMMENT COMMENT_act_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."COMMENT"
    ADD CONSTRAINT "COMMENT_act_id_fkey" FOREIGN KEY (act_id) REFERENCES public."ACTIVITY"(act_id) ON UPDATE CASCADE ON DELETE CASCADE;
 I   ALTER TABLE ONLY public."COMMENT" DROP CONSTRAINT "COMMENT_act_id_fkey";
       public       postgres    false    2741    208    209            �
           2606    16509    SETTINGS SETTINGS_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_user_id_fkey";
       public       postgres    false    198    197    2714            I      x������ � �      G      x������ � �      A      x������ � �      J      x������ � �      E      x������ � �      ?      x������ � �      C      x������ � �      >      x������ � �     