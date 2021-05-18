PGDMP     	    0                y           TimeSoft    13.3    13.2 3    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24576    TimeSoft    DATABASE     g   CREATE DATABASE "TimeSoft" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "TimeSoft";
                postgres    false            �            1259    25563    ACTIVITY    TABLE     �   CREATE TABLE public."ACTIVITY" (
    act_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name character varying(64) NOT NULL,
    time_value integer NOT NULL,
    date_value date NOT NULL,
    cat_name character varying(64) NOT NULL
);
    DROP TABLE public."ACTIVITY";
       public         heap    postgres    false            �            1259    25532    ACTIVITY_LIST    TABLE     �   CREATE TABLE public."ACTIVITY_LIST" (
    actl_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name character varying(64) NOT NULL,
    cat_name character varying(64) NOT NULL
);
 #   DROP TABLE public."ACTIVITY_LIST";
       public         heap    postgres    false            �            1259    25530    ACTIVITY_LIST_actl_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY_LIST" ALTER COLUMN actl_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_LIST_actl_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    206            �            1259    25561    ACTIVITY_act_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY" ALTER COLUMN act_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_act_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    212            �            1259    25520    CATEGORY    TABLE     �   CREATE TABLE public."CATEGORY" (
    cat_id integer NOT NULL,
    user_id integer NOT NULL,
    cat_name character varying(64) NOT NULL
);
    DROP TABLE public."CATEGORY";
       public         heap    postgres    false            �            1259    25518    CATEGORY_cat_id_seq    SEQUENCE     �   ALTER TABLE public."CATEGORY" ALTER COLUMN cat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."CATEGORY_cat_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    204            �            1259    25588    COMMENT    TABLE     S   CREATE TABLE public."COMMENT" (
    act_id integer NOT NULL,
    com_value text
);
    DROP TABLE public."COMMENT";
       public         heap    postgres    false            �            1259    25556    DATE    TABLE     [   CREATE TABLE public."DATE" (
    date_id integer NOT NULL,
    date_value date NOT NULL
);
    DROP TABLE public."DATE";
       public         heap    postgres    false            �            1259    25554    DATE_date_id_seq    SEQUENCE     �   ALTER TABLE public."DATE" ALTER COLUMN date_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."DATE_date_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    210            �            1259    25505    SETTINGS    TABLE     o   CREATE TABLE public."SETTINGS" (
    user_id integer NOT NULL,
    set_theme text,
    set_preferences text
);
    DROP TABLE public."SETTINGS";
       public         heap    postgres    false            �            1259    25549    TIME    TABLE     ^   CREATE TABLE public."TIME" (
    time_id integer NOT NULL,
    time_value integer NOT NULL
);
    DROP TABLE public."TIME";
       public         heap    postgres    false            �            1259    25547    TIME_time_id_seq    SEQUENCE     �   ALTER TABLE public."TIME" ALTER COLUMN time_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."TIME_time_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    208            �            1259    25496    USER    TABLE     �   CREATE TABLE public."USER" (
    user_id integer NOT NULL,
    user_name character varying(32) NOT NULL,
    user_email character varying(64) NOT NULL,
    user_password character varying(64) NOT NULL,
    user_telegram character varying(64)
);
    DROP TABLE public."USER";
       public         heap    postgres    false            �            1259    25494    USER_user_id_seq    SEQUENCE     �   ALTER TABLE public."USER" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."USER_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    201            �          0    25563    ACTIVITY 
   TABLE DATA           b   COPY public."ACTIVITY" (act_id, user_id, actl_name, time_value, date_value, cat_name) FROM stdin;
    public          postgres    false    212   �=       �          0    25532    ACTIVITY_LIST 
   TABLE DATA           P   COPY public."ACTIVITY_LIST" (actl_id, user_id, actl_name, cat_name) FROM stdin;
    public          postgres    false    206   
>       �          0    25520    CATEGORY 
   TABLE DATA           ?   COPY public."CATEGORY" (cat_id, user_id, cat_name) FROM stdin;
    public          postgres    false    204   '>       �          0    25588    COMMENT 
   TABLE DATA           6   COPY public."COMMENT" (act_id, com_value) FROM stdin;
    public          postgres    false    213   D>       �          0    25556    DATE 
   TABLE DATA           5   COPY public."DATE" (date_id, date_value) FROM stdin;
    public          postgres    false    210   a>       �          0    25505    SETTINGS 
   TABLE DATA           I   COPY public."SETTINGS" (user_id, set_theme, set_preferences) FROM stdin;
    public          postgres    false    202   ~>       �          0    25549    TIME 
   TABLE DATA           5   COPY public."TIME" (time_id, time_value) FROM stdin;
    public          postgres    false    208   �>       �          0    25496    USER 
   TABLE DATA           ^   COPY public."USER" (user_id, user_name, user_email, user_password, user_telegram) FROM stdin;
    public          postgres    false    201   �>       �           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."ACTIVITY_LIST_actl_id_seq"', 1, false);
          public          postgres    false    205            �           0    0    ACTIVITY_act_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."ACTIVITY_act_id_seq"', 1, false);
          public          postgres    false    211            �           0    0    CATEGORY_cat_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."CATEGORY_cat_id_seq"', 1, false);
          public          postgres    false    203                        0    0    DATE_date_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."DATE_date_id_seq"', 1, false);
          public          postgres    false    209                       0    0    TIME_time_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."TIME_time_id_seq"', 1, false);
          public          postgres    false    207                       0    0    USER_user_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."USER_user_id_seq"', 1, false);
          public          postgres    false    200            U           2606    25536     ACTIVITY_LIST ACTIVITY_LIST_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_pkey" PRIMARY KEY (user_id, actl_name, cat_name);
 N   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_pkey";
       public            postgres    false    206    206    206            [           2606    25567    ACTIVITY ACTIVITY_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_pkey" PRIMARY KEY (act_id);
 D   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_pkey";
       public            postgres    false    212            S           2606    25524    CATEGORY CATEGORY_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_pkey" PRIMARY KEY (user_id, cat_name);
 D   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_pkey";
       public            postgres    false    204    204            ]           2606    25595    COMMENT COMMENT_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public."COMMENT"
    ADD CONSTRAINT "COMMENT_pkey" PRIMARY KEY (act_id);
 B   ALTER TABLE ONLY public."COMMENT" DROP CONSTRAINT "COMMENT_pkey";
       public            postgres    false    213            Y           2606    25560    DATE DATE_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."DATE"
    ADD CONSTRAINT "DATE_pkey" PRIMARY KEY (date_value);
 <   ALTER TABLE ONLY public."DATE" DROP CONSTRAINT "DATE_pkey";
       public            postgres    false    210            Q           2606    25512    SETTINGS SETTINGS_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_pkey" PRIMARY KEY (user_id);
 D   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_pkey";
       public            postgres    false    202            W           2606    25553    TIME TIME_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public."TIME"
    ADD CONSTRAINT "TIME_pkey" PRIMARY KEY (time_value);
 <   ALTER TABLE ONLY public."TIME" DROP CONSTRAINT "TIME_pkey";
       public            postgres    false    208            K           2606    25500    USER USER_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (user_id);
 <   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_pkey";
       public            postgres    false    201            M           2606    25504    USER USER_user_email_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_email_key" UNIQUE (user_email);
 F   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_email_key";
       public            postgres    false    201            O           2606    25502    USER USER_user_name_key 
   CONSTRAINT     [   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_name_key" UNIQUE (user_name);
 E   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_name_key";
       public            postgres    false    201            a           2606    25542 1   ACTIVITY_LIST ACTIVITY_LIST_user_id_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey" FOREIGN KEY (user_id, cat_name) REFERENCES public."CATEGORY"(user_id, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey";
       public          postgres    false    206    206    204    204    2899            `           2606    25537 (   ACTIVITY_LIST ACTIVITY_LIST_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 V   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_fkey";
       public          postgres    false    2891    206    201            e           2606    25583 !   ACTIVITY ACTIVITY_date_value_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_date_value_fkey" FOREIGN KEY (date_value) REFERENCES public."DATE"(date_value) ON UPDATE CASCADE ON DELETE CASCADE;
 O   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_date_value_fkey";
       public          postgres    false    210    2905    212            d           2606    25578 !   ACTIVITY ACTIVITY_time_value_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_time_value_fkey" FOREIGN KEY (time_value) REFERENCES public."TIME"(time_value) ON UPDATE CASCADE ON DELETE CASCADE;
 O   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_time_value_fkey";
       public          postgres    false    212    208    2903            c           2606    25573 1   ACTIVITY ACTIVITY_user_id_actl_name_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey" FOREIGN KEY (user_id, actl_name, cat_name) REFERENCES public."ACTIVITY_LIST"(user_id, actl_name, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey";
       public          postgres    false    212    212    206    206    206    212    2901            b           2606    25568    ACTIVITY ACTIVITY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_fkey";
       public          postgres    false    212    201    2891            _           2606    25525    CATEGORY CATEGORY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_user_id_fkey";
       public          postgres    false    204    2891    201            f           2606    25596    COMMENT COMMENT_act_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."COMMENT"
    ADD CONSTRAINT "COMMENT_act_id_fkey" FOREIGN KEY (act_id) REFERENCES public."ACTIVITY"(act_id) ON UPDATE CASCADE ON DELETE CASCADE;
 I   ALTER TABLE ONLY public."COMMENT" DROP CONSTRAINT "COMMENT_act_id_fkey";
       public          postgres    false    213    2907    212            ^           2606    25513    SETTINGS SETTINGS_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_user_id_fkey";
       public          postgres    false    201    2891    202            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     