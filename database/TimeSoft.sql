PGDMP     +    )                y           TimeSoft    13.3    13.2 !    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24576    TimeSoft    DATABASE     g   CREATE DATABASE "TimeSoft" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "TimeSoft";
                postgres    false            �            1259    25843    ACTIVITY    TABLE     
  CREATE TABLE public."ACTIVITY" (
    act_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name character varying(64) NOT NULL,
    act_time integer NOT NULL,
    act_date date NOT NULL,
    cat_name character varying(64) NOT NULL,
    act_comment text
);
    DROP TABLE public."ACTIVITY";
       public         heap    postgres    false            �            1259    25831    ACTIVITY_LIST    TABLE     �   CREATE TABLE public."ACTIVITY_LIST" (
    actl_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name character varying(64) NOT NULL,
    cat_name character varying(64) NOT NULL
);
 #   DROP TABLE public."ACTIVITY_LIST";
       public         heap    postgres    false            �            1259    25829    ACTIVITY_LIST_actl_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY_LIST" ALTER COLUMN actl_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_LIST_actl_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    206            �            1259    25841    ACTIVITY_act_id_seq    SEQUENCE     �   ALTER TABLE public."ACTIVITY" ALTER COLUMN act_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."ACTIVITY_act_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    208            �            1259    25819    CATEGORY    TABLE     �   CREATE TABLE public."CATEGORY" (
    cat_id integer NOT NULL,
    user_id integer NOT NULL,
    cat_name character varying(64) NOT NULL
);
    DROP TABLE public."CATEGORY";
       public         heap    postgres    false            �            1259    25817    CATEGORY_cat_id_seq    SEQUENCE     �   ALTER TABLE public."CATEGORY" ALTER COLUMN cat_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."CATEGORY_cat_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    204            �            1259    25804    SETTINGS    TABLE     o   CREATE TABLE public."SETTINGS" (
    user_id integer NOT NULL,
    set_theme text,
    set_preferences text
);
    DROP TABLE public."SETTINGS";
       public         heap    postgres    false            �            1259    25795    USER    TABLE     �   CREATE TABLE public."USER" (
    user_id integer NOT NULL,
    user_name character varying(32) NOT NULL,
    user_email character varying(64) NOT NULL,
    user_password character varying(64) NOT NULL,
    user_telegram character varying(64)
);
    DROP TABLE public."USER";
       public         heap    postgres    false            �            1259    25793    USER_user_id_seq    SEQUENCE     �   ALTER TABLE public."USER" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."USER_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    201            �          0    25843    ACTIVITY 
   TABLE DATA           k   COPY public."ACTIVITY" (act_id, user_id, actl_name, act_time, act_date, cat_name, act_comment) FROM stdin;
    public          postgres    false    208   G(       �          0    25831    ACTIVITY_LIST 
   TABLE DATA           P   COPY public."ACTIVITY_LIST" (actl_id, user_id, actl_name, cat_name) FROM stdin;
    public          postgres    false    206   d(       �          0    25819    CATEGORY 
   TABLE DATA           ?   COPY public."CATEGORY" (cat_id, user_id, cat_name) FROM stdin;
    public          postgres    false    204   �(       �          0    25804    SETTINGS 
   TABLE DATA           I   COPY public."SETTINGS" (user_id, set_theme, set_preferences) FROM stdin;
    public          postgres    false    202   �(       �          0    25795    USER 
   TABLE DATA           ^   COPY public."USER" (user_id, user_name, user_email, user_password, user_telegram) FROM stdin;
    public          postgres    false    201   �(       �           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."ACTIVITY_LIST_actl_id_seq"', 1, false);
          public          postgres    false    205            �           0    0    ACTIVITY_act_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."ACTIVITY_act_id_seq"', 1, false);
          public          postgres    false    207            �           0    0    CATEGORY_cat_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."CATEGORY_cat_id_seq"', 1, false);
          public          postgres    false    203            �           0    0    USER_user_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."USER_user_id_seq"', 1, false);
          public          postgres    false    200            E           2606    25835     ACTIVITY_LIST ACTIVITY_LIST_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_pkey" PRIMARY KEY (user_id, actl_name, cat_name);
 N   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_pkey";
       public            postgres    false    206    206    206            G           2606    25850    ACTIVITY ACTIVITY_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_pkey" PRIMARY KEY (act_id);
 D   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_pkey";
       public            postgres    false    208            C           2606    25823    CATEGORY CATEGORY_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_pkey" PRIMARY KEY (user_id, cat_name);
 D   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_pkey";
       public            postgres    false    204    204            A           2606    25811    SETTINGS SETTINGS_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_pkey" PRIMARY KEY (user_id);
 D   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_pkey";
       public            postgres    false    202            ;           2606    25799    USER USER_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (user_id);
 <   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_pkey";
       public            postgres    false    201            =           2606    25803    USER USER_user_email_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_email_key" UNIQUE (user_email);
 F   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_email_key";
       public            postgres    false    201            ?           2606    25801    USER USER_user_name_key 
   CONSTRAINT     [   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_name_key" UNIQUE (user_name);
 E   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_name_key";
       public            postgres    false    201            J           2606    25836 1   ACTIVITY_LIST ACTIVITY_LIST_user_id_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey" FOREIGN KEY (user_id, cat_name) REFERENCES public."CATEGORY"(user_id, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey";
       public          postgres    false    204    206    206    2883    204            K           2606    25851 1   ACTIVITY ACTIVITY_user_id_actl_name_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey" FOREIGN KEY (user_id, actl_name, cat_name) REFERENCES public."ACTIVITY_LIST"(user_id, actl_name, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey";
       public          postgres    false    206    206    206    2885    208    208    208            I           2606    25824    CATEGORY CATEGORY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_user_id_fkey";
       public          postgres    false    204    2875    201            H           2606    25812    SETTINGS SETTINGS_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_user_id_fkey";
       public          postgres    false    2875    201    202            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     