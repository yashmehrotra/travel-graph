--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: doobie; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE doobie (
    doobie_id bigint NOT NULL,
    type bigint,
    mapping_id integer NOT NULL
);


ALTER TABLE public.doobie OWNER TO yash;

--
-- Name: COLUMN doobie.type; Type: COMMENT; Schema: public; Owner: yash
--

COMMENT ON COLUMN doobie.type IS 'comes from doobie_type.id';


--
-- Name: COLUMN doobie.mapping_id; Type: COMMENT; Schema: public; Owner: yash
--

COMMENT ON COLUMN doobie.mapping_id IS 'comes from doobie_xxx.id';


--
-- Name: doobie_answers; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE doobie_answers (
    answer_id bigint NOT NULL,
    answer text NOT NULL,
    question_id bigint NOT NULL,
    user_id bigint NOT NULL,
    created_ts timestamp without time zone NOT NULL,
    updated_ts timestamp without time zone
);


ALTER TABLE public.doobie_answers OWNER TO yash;

--
-- Name: doobie_answers_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_answers_answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_answers_answer_id_seq OWNER TO yash;

--
-- Name: doobie_answers_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_answers_answer_id_seq OWNED BY doobie_answers.answer_id;


--
-- Name: doobie_doobie_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_doobie_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_doobie_id_seq OWNER TO yash;

--
-- Name: doobie_doobie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_doobie_id_seq OWNED BY doobie.doobie_id;


--
-- Name: doobie_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_mapping_id_seq OWNER TO yash;

--
-- Name: doobie_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_mapping_id_seq OWNED BY doobie.mapping_id;


--
-- Name: doobie_questions; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE doobie_questions (
    question_id bigint NOT NULL,
    title text NOT NULL,
    description text,
    user_id bigint NOT NULL,
    created_ts timestamp without time zone NOT NULL,
    updated_ts timestamp without time zone
);


ALTER TABLE public.doobie_questions OWNER TO yash;

--
-- Name: doobie_questions_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_questions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_questions_id_seq OWNER TO yash;

--
-- Name: doobie_questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_questions_id_seq OWNED BY doobie_questions.question_id;


--
-- Name: doobie_tags_mapping; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE doobie_tags_mapping (
    id bigint NOT NULL,
    doobie_type bigint NOT NULL,
    mapping_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.doobie_tags_mapping OWNER TO yash;

--
-- Name: doobie_tags_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_tags_mapping_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_tags_mapping_id_seq OWNER TO yash;

--
-- Name: doobie_tags_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_tags_mapping_id_seq OWNED BY doobie_tags_mapping.id;


--
-- Name: doobie_type; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE doobie_type (
    id bigint NOT NULL,
    name text NOT NULL,
    table_name text
);


ALTER TABLE public.doobie_type OWNER TO yash;

--
-- Name: COLUMN doobie_type.name; Type: COMMENT; Schema: public; Owner: yash
--

COMMENT ON COLUMN doobie_type.name IS 'eg. Questions, Answers, Blog';


--
-- Name: doobie_type_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE doobie_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doobie_type_id_seq OWNER TO yash;

--
-- Name: doobie_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE doobie_type_id_seq OWNED BY doobie_type.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE tags (
    tag_id bigint NOT NULL,
    type text,
    name text NOT NULL
);


ALTER TABLE public.tags OWNER TO yash;

--
-- Name: tag_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE tag_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_tag_id_seq OWNER TO yash;

--
-- Name: tag_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE tag_tag_id_seq OWNED BY tags.tag_id;


--
-- Name: tag_type; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE tag_type (
    id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.tag_type OWNER TO yash;

--
-- Name: tag_type_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE tag_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_type_id_seq OWNER TO yash;

--
-- Name: tag_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE tag_type_id_seq OWNED BY tag_type.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE "user" (
    user_id bigint NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    profile_photo text,
    facebook_token text,
    google_token text,
    created_ts timestamp without time zone NOT NULL,
    updated_ts timestamp without time zone,
    login_ts timestamp without time zone,
    bio text
);


ALTER TABLE public."user" OWNER TO yash;

--
-- Name: user_follows; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE user_follows (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    follows_user_id bigint NOT NULL,
    created_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.user_follows OWNER TO yash;

--
-- Name: user_follows_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE user_follows_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_follows_id_seq OWNER TO yash;

--
-- Name: user_follows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE user_follows_id_seq OWNED BY user_follows.id;


--
-- Name: user_doobie_follows; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE user_doobie_follows (
    id bigint DEFAULT nextval('user_follows_id_seq'::regclass) NOT NULL,
    user_id bigint NOT NULL,
    doobie_id bigint NOT NULL,
    created_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.user_doobie_follows OWNER TO yash;

--
-- Name: user_tags_follows; Type: TABLE; Schema: public; Owner: yash; Tablespace: 
--

CREATE TABLE user_tags_follows (
    id bigint DEFAULT nextval('user_follows_id_seq'::regclass) NOT NULL,
    user_id bigint NOT NULL,
    tag_id bigint NOT NULL,
    created_ts timestamp without time zone NOT NULL
);


ALTER TABLE public.user_tags_follows OWNER TO yash;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: yash
--

CREATE SEQUENCE user_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_user_id_seq OWNER TO yash;

--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: yash
--

ALTER SEQUENCE user_user_id_seq OWNED BY "user".user_id;


--
-- Name: doobie_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie ALTER COLUMN doobie_id SET DEFAULT nextval('doobie_doobie_id_seq'::regclass);


--
-- Name: mapping_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie ALTER COLUMN mapping_id SET DEFAULT nextval('doobie_mapping_id_seq'::regclass);


--
-- Name: answer_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie_answers ALTER COLUMN answer_id SET DEFAULT nextval('doobie_answers_answer_id_seq'::regclass);


--
-- Name: question_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie_questions ALTER COLUMN question_id SET DEFAULT nextval('doobie_questions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie_tags_mapping ALTER COLUMN id SET DEFAULT nextval('doobie_tags_mapping_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY doobie_type ALTER COLUMN id SET DEFAULT nextval('doobie_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY tag_type ALTER COLUMN id SET DEFAULT nextval('tag_type_id_seq'::regclass);


--
-- Name: tag_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY tags ALTER COLUMN tag_id SET DEFAULT nextval('tag_tag_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY "user" ALTER COLUMN user_id SET DEFAULT nextval('user_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: yash
--

ALTER TABLE ONLY user_follows ALTER COLUMN id SET DEFAULT nextval('user_follows_id_seq'::regclass);


--
-- Name: doobie_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY doobie_answers
    ADD CONSTRAINT doobie_answers_pkey PRIMARY KEY (answer_id);


--
-- Name: doobie_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY doobie
    ADD CONSTRAINT doobie_pkey PRIMARY KEY (doobie_id);


--
-- Name: doobie_questions_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY doobie_questions
    ADD CONSTRAINT doobie_questions_pkey PRIMARY KEY (question_id);


--
-- Name: doobie_tags_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY doobie_tags_mapping
    ADD CONSTRAINT doobie_tags_mapping_pkey PRIMARY KEY (id);


--
-- Name: doobie_type_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY doobie_type
    ADD CONSTRAINT doobie_type_pkey PRIMARY KEY (id);


--
-- Name: tag_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY tags
    ADD CONSTRAINT tag_pkey PRIMARY KEY (tag_id);


--
-- Name: tag_type_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY tag_type
    ADD CONSTRAINT tag_type_pkey PRIMARY KEY (id);


--
-- Name: user_doobie_follows_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY user_doobie_follows
    ADD CONSTRAINT user_doobie_follows_pkey PRIMARY KEY (id);


--
-- Name: user_follows_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY user_follows
    ADD CONSTRAINT user_follows_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: user_tags_follows_pkey; Type: CONSTRAINT; Schema: public; Owner: yash; Tablespace: 
--

ALTER TABLE ONLY user_tags_follows
    ADD CONSTRAINT user_tags_follows_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

