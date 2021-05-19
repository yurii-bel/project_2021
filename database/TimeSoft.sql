PGDMP                         y           TimeSoft    13.3    13.2 6    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    25856    TimeSoft    DATABASE     g   CREATE DATABASE "TimeSoft" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "TimeSoft";
                postgres    false            �            1259    26420    ACTIVITY    TABLE     
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
       public         heap    postgres    false            �            1259    26405    ACTIVITY_LIST    TABLE     �   CREATE TABLE public."ACTIVITY_LIST" (
    actl_id integer NOT NULL,
    user_id integer NOT NULL,
    actl_name character varying(64) NOT NULL,
    cat_name character varying(64) NOT NULL
);
 #   DROP TABLE public."ACTIVITY_LIST";
       public         heap    postgres    false            �            1259    26403    ACTIVITY_LIST_actl_id_seq    SEQUENCE     �   CREATE SEQUENCE public."ACTIVITY_LIST_actl_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public."ACTIVITY_LIST_actl_id_seq";
       public          postgres    false    208            �           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public."ACTIVITY_LIST_actl_id_seq" OWNED BY public."ACTIVITY_LIST".actl_id;
          public          postgres    false    207            �            1259    26418    ACTIVITY_act_id_seq    SEQUENCE     �   CREATE SEQUENCE public."ACTIVITY_act_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public."ACTIVITY_act_id_seq";
       public          postgres    false    210            �           0    0    ACTIVITY_act_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public."ACTIVITY_act_id_seq" OWNED BY public."ACTIVITY".act_id;
          public          postgres    false    209            �            1259    26390    CATEGORY    TABLE     �   CREATE TABLE public."CATEGORY" (
    cat_id integer NOT NULL,
    user_id integer NOT NULL,
    cat_name character varying(64) NOT NULL
);
    DROP TABLE public."CATEGORY";
       public         heap    postgres    false            �            1259    26388    CATEGORY_cat_id_seq    SEQUENCE     �   CREATE SEQUENCE public."CATEGORY_cat_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public."CATEGORY_cat_id_seq";
       public          postgres    false    206            �           0    0    CATEGORY_cat_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public."CATEGORY_cat_id_seq" OWNED BY public."CATEGORY".cat_id;
          public          postgres    false    205            �            1259    26375    SETTINGS    TABLE     o   CREATE TABLE public."SETTINGS" (
    user_id integer NOT NULL,
    set_theme text,
    set_preferences text
);
    DROP TABLE public."SETTINGS";
       public         heap    postgres    false            �            1259    26339    USER    TABLE     �   CREATE TABLE public."USER" (
    user_id integer NOT NULL,
    user_n_id character varying(40) NOT NULL,
    user_p_id character varying(40) NOT NULL
);
    DROP TABLE public."USER";
       public         heap    postgres    false            �            1259    26351 	   USER_NAME    TABLE     �   CREATE TABLE public."USER_NAME" (
    user_n_id character varying(40) NOT NULL,
    user_n_name character varying(32) NOT NULL,
    user_n_telegram character varying(40)
);
    DROP TABLE public."USER_NAME";
       public         heap    postgres    false            �            1259    26363    USER_PRIVAT    TABLE     �   CREATE TABLE public."USER_PRIVAT" (
    user_p_id character varying(40) NOT NULL,
    user_p_email character varying(64) NOT NULL,
    user_p_password character varying(64) NOT NULL
);
 !   DROP TABLE public."USER_PRIVAT";
       public         heap    postgres    false            �            1259    26337    USER_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public."USER_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."USER_user_id_seq";
       public          postgres    false    201            �           0    0    USER_user_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."USER_user_id_seq" OWNED BY public."USER".user_id;
          public          postgres    false    200            E           2604    26423    ACTIVITY act_id    DEFAULT     v   ALTER TABLE ONLY public."ACTIVITY" ALTER COLUMN act_id SET DEFAULT nextval('public."ACTIVITY_act_id_seq"'::regclass);
 @   ALTER TABLE public."ACTIVITY" ALTER COLUMN act_id DROP DEFAULT;
       public          postgres    false    209    210    210            D           2604    26408    ACTIVITY_LIST actl_id    DEFAULT     �   ALTER TABLE ONLY public."ACTIVITY_LIST" ALTER COLUMN actl_id SET DEFAULT nextval('public."ACTIVITY_LIST_actl_id_seq"'::regclass);
 F   ALTER TABLE public."ACTIVITY_LIST" ALTER COLUMN actl_id DROP DEFAULT;
       public          postgres    false    208    207    208            C           2604    26393    CATEGORY cat_id    DEFAULT     v   ALTER TABLE ONLY public."CATEGORY" ALTER COLUMN cat_id SET DEFAULT nextval('public."CATEGORY_cat_id_seq"'::regclass);
 @   ALTER TABLE public."CATEGORY" ALTER COLUMN cat_id DROP DEFAULT;
       public          postgres    false    206    205    206            B           2604    26342    USER user_id    DEFAULT     p   ALTER TABLE ONLY public."USER" ALTER COLUMN user_id SET DEFAULT nextval('public."USER_user_id_seq"'::regclass);
 =   ALTER TABLE public."USER" ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    200    201    201            �          0    26420    ACTIVITY 
   TABLE DATA           k   COPY public."ACTIVITY" (act_id, user_id, actl_name, act_time, act_date, cat_name, act_comment) FROM stdin;
    public          postgres    false    210   �A       �          0    26405    ACTIVITY_LIST 
   TABLE DATA           P   COPY public."ACTIVITY_LIST" (actl_id, user_id, actl_name, cat_name) FROM stdin;
    public          postgres    false    208   	B       �          0    26390    CATEGORY 
   TABLE DATA           ?   COPY public."CATEGORY" (cat_id, user_id, cat_name) FROM stdin;
    public          postgres    false    206   &B       �          0    26375    SETTINGS 
   TABLE DATA           I   COPY public."SETTINGS" (user_id, set_theme, set_preferences) FROM stdin;
    public          postgres    false    204   CB       �          0    26339    USER 
   TABLE DATA           ?   COPY public."USER" (user_id, user_n_id, user_p_id) FROM stdin;
    public          postgres    false    201   `B       �          0    26351 	   USER_NAME 
   TABLE DATA           N   COPY public."USER_NAME" (user_n_id, user_n_name, user_n_telegram) FROM stdin;
    public          postgres    false    202   }B       �          0    26363    USER_PRIVAT 
   TABLE DATA           Q   COPY public."USER_PRIVAT" (user_p_id, user_p_email, user_p_password) FROM stdin;
    public          postgres    false    203   �B       �           0    0    ACTIVITY_LIST_actl_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public."ACTIVITY_LIST_actl_id_seq"', 1, false);
          public          postgres    false    207                        0    0    ACTIVITY_act_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."ACTIVITY_act_id_seq"', 1, false);
          public          postgres    false    209                       0    0    CATEGORY_cat_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public."CATEGORY_cat_id_seq"', 1, false);
          public          postgres    false    205                       0    0    USER_user_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."USER_user_id_seq"', 1, false);
          public          postgres    false    200            ]           2606    26412 '   ACTIVITY_LIST ACTIVITY_LIST_actl_id_key 
   CONSTRAINT     i   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_actl_id_key" UNIQUE (actl_id);
 U   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_actl_id_key";
       public            postgres    false    208            _           2606    26410     ACTIVITY_LIST ACTIVITY_LIST_pkey 
   CONSTRAINT     |   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_pkey" PRIMARY KEY (user_id, actl_name, cat_name);
 N   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_pkey";
       public            postgres    false    208    208    208            a           2606    26428    ACTIVITY ACTIVITY_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_pkey" PRIMARY KEY (act_id);
 D   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_pkey";
       public            postgres    false    210            Y           2606    26397    CATEGORY CATEGORY_cat_id_key 
   CONSTRAINT     ]   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_cat_id_key" UNIQUE (cat_id);
 J   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_cat_id_key";
       public            postgres    false    206            [           2606    26395    CATEGORY CATEGORY_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_pkey" PRIMARY KEY (user_id, cat_name);
 D   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_pkey";
       public            postgres    false    206    206            W           2606    26382    SETTINGS SETTINGS_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_pkey" PRIMARY KEY (user_id);
 D   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_pkey";
       public            postgres    false    204            O           2606    26355    USER_NAME USER_NAME_pkey 
   CONSTRAINT     a   ALTER TABLE ONLY public."USER_NAME"
    ADD CONSTRAINT "USER_NAME_pkey" PRIMARY KEY (user_n_id);
 F   ALTER TABLE ONLY public."USER_NAME" DROP CONSTRAINT "USER_NAME_pkey";
       public            postgres    false    202            Q           2606    26357 #   USER_NAME USER_NAME_user_n_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public."USER_NAME"
    ADD CONSTRAINT "USER_NAME_user_n_name_key" UNIQUE (user_n_name);
 Q   ALTER TABLE ONLY public."USER_NAME" DROP CONSTRAINT "USER_NAME_user_n_name_key";
       public            postgres    false    202            S           2606    26367    USER_PRIVAT USER_PRIVAT_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public."USER_PRIVAT"
    ADD CONSTRAINT "USER_PRIVAT_pkey" PRIMARY KEY (user_p_id);
 J   ALTER TABLE ONLY public."USER_PRIVAT" DROP CONSTRAINT "USER_PRIVAT_pkey";
       public            postgres    false    203            U           2606    26369 (   USER_PRIVAT USER_PRIVAT_user_p_email_key 
   CONSTRAINT     o   ALTER TABLE ONLY public."USER_PRIVAT"
    ADD CONSTRAINT "USER_PRIVAT_user_p_email_key" UNIQUE (user_p_email);
 V   ALTER TABLE ONLY public."USER_PRIVAT" DROP CONSTRAINT "USER_PRIVAT_user_p_email_key";
       public            postgres    false    203            G           2606    26344    USER USER_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_pkey" PRIMARY KEY (user_id, user_n_id, user_p_id);
 <   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_pkey";
       public            postgres    false    201    201    201            I           2606    26346    USER USER_user_id_key 
   CONSTRAINT     W   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_id_key" UNIQUE (user_id);
 C   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_id_key";
       public            postgres    false    201            K           2606    26348    USER USER_user_n_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_n_id_key" UNIQUE (user_n_id);
 E   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_n_id_key";
       public            postgres    false    201            M           2606    26350    USER USER_user_p_id_key 
   CONSTRAINT     [   ALTER TABLE ONLY public."USER"
    ADD CONSTRAINT "USER_user_p_id_key" UNIQUE (user_p_id);
 E   ALTER TABLE ONLY public."USER" DROP CONSTRAINT "USER_user_p_id_key";
       public            postgres    false    201            f           2606    26413 1   ACTIVITY_LIST ACTIVITY_LIST_user_id_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY_LIST"
    ADD CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey" FOREIGN KEY (user_id, cat_name) REFERENCES public."CATEGORY"(user_id, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY_LIST" DROP CONSTRAINT "ACTIVITY_LIST_user_id_cat_name_fkey";
       public          postgres    false    208    206    2907    208    206            g           2606    26429 1   ACTIVITY ACTIVITY_user_id_actl_name_cat_name_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."ACTIVITY"
    ADD CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey" FOREIGN KEY (user_id, actl_name, cat_name) REFERENCES public."ACTIVITY_LIST"(user_id, actl_name, cat_name) ON UPDATE CASCADE ON DELETE CASCADE;
 _   ALTER TABLE ONLY public."ACTIVITY" DROP CONSTRAINT "ACTIVITY_user_id_actl_name_cat_name_fkey";
       public          postgres    false    210    2911    208    208    208    210    210            e           2606    26398    CATEGORY CATEGORY_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."CATEGORY"
    ADD CONSTRAINT "CATEGORY_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."CATEGORY" DROP CONSTRAINT "CATEGORY_user_id_fkey";
       public          postgres    false    201    2889    206            d           2606    26383    SETTINGS SETTINGS_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."SETTINGS"
    ADD CONSTRAINT "SETTINGS_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."USER"(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
 L   ALTER TABLE ONLY public."SETTINGS" DROP CONSTRAINT "SETTINGS_user_id_fkey";
       public          postgres    false    2889    204    201            b           2606    26358 "   USER_NAME USER_NAME_user_n_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."USER_NAME"
    ADD CONSTRAINT "USER_NAME_user_n_id_fkey" FOREIGN KEY (user_n_id) REFERENCES public."USER"(user_n_id) ON UPDATE CASCADE ON DELETE CASCADE;
 P   ALTER TABLE ONLY public."USER_NAME" DROP CONSTRAINT "USER_NAME_user_n_id_fkey";
       public          postgres    false    202    2891    201            c           2606    26370 &   USER_PRIVAT USER_PRIVAT_user_p_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."USER_PRIVAT"
    ADD CONSTRAINT "USER_PRIVAT_user_p_id_fkey" FOREIGN KEY (user_p_id) REFERENCES public."USER"(user_p_id) ON UPDATE CASCADE ON DELETE CASCADE;
 T   ALTER TABLE ONLY public."USER_PRIVAT" DROP CONSTRAINT "USER_PRIVAT_user_p_id_fkey";
       public          postgres    false    201    2893    203            �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �      �      x������ � �     