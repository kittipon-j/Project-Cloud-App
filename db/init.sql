-- Step 1: Create Database
CREATE DATABASE "Coe_Access_control"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "Coe_Access_control"
    IS 'For Cloud Application Class';

-- Step 2: Connect to the newly created database
\c Coe_Access_control

-- Step 3: Create Schema
CREATE SCHEMA IF NOT EXISTS "Access_Control"
    AUTHORIZATION postgres;

-- Step 4: Create Sequences (if not already created)
CREATE SEQUENCE IF NOT EXISTS "Access_Control".user_log_log_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE IF NOT EXISTS "Access_Control".car_log_log_id_seq
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO MAXVALUE
    CACHE 1;

-- Step 5: Create Tables

-- Table: Access_Control.user_info
CREATE TABLE IF NOT EXISTS "Access_Control".user_info
(
    user_id character varying(15) COLLATE pg_catalog."default" NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    lastname character varying(150) COLLATE pg_catalog."default" NOT NULL,
    upd_date date NOT NULL,
    image_path character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT student_info_pkey PRIMARY KEY (user_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS "Access_Control".user_info
    OWNER to postgres;

-- Table: Access_Control.user_log
CREATE TABLE IF NOT EXISTS "Access_Control".user_log
(
    log_id integer NOT NULL DEFAULT nextval('"Access_Control".user_log_log_id_seq'::regclass),
    user_id character varying(15) COLLATE pg_catalog."default" NOT NULL,
    time_stamp timestamp without time zone NOT NULL,
    room smallint NOT NULL,
    CONSTRAINT student_log_pkey PRIMARY KEY (log_id),
    CONSTRAINT student_log_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES "Access_Control".user_info (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS "Access_Control".user_log
    OWNER to postgres;

-- Table: Access_Control.car_log
CREATE TABLE IF NOT EXISTS "Access_Control".car_log
(
    log_id integer NOT NULL DEFAULT nextval('"Access_Control".car_log_log_id_seq'::regclass),
    plate character varying(50) COLLATE pg_catalog."default" NOT NULL,
    time_stamp timestamp without time zone NOT NULL,
    CONSTRAINT car_log_pkey PRIMARY KEY (log_id)
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS "Access_Control".car_log
    OWNER to postgres;