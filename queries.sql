SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE IF EXISTS pgosquery;
CREATE DATABASE pgosquery WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
ALTER DATABASE pgosquery OWNER TO postgres;

\connect pgosquery

BEGIN;

CREATE SCHEMA IF NOT EXISTS public;
ALTER SCHEMA public OWNER TO postgres;
CREATE EXTENSION IF NOT EXISTS multicorn WITH SCHEMA public;

DROP SERVER IF EXISTS pgosquery_srv CASCADE;

CREATE SERVER pgosquery_srv foreign data wrapper multicorn options (
    wrapper 'pgosquery.PgOSQuery'
);

CREATE FOREIGN TABLE processes (
    pid integer,
    name character varying,
    username character varying
) server pgosquery_srv options (
    tabletype 'processes'
);

CREATE FOREIGN TABLE listening_ports (
    pid integer,
    address character varying,
    port integer
) server pgosquery_srv options (
    tabletype 'listening_ports'
);

COMMIT;

--------------------------------------------------------
-- get the name, pid and attached port of all processes
-- which are listening on all interfaces
--------------------------------------------------------
SELECT DISTINCT
    process.name,
    listening.port,
    process.pid
FROM processes AS process
JOIN listening_ports AS listening
ON process.pid = listening.pid
WHERE listening.address = '127.0.0.1';

SELECT DISTINCT
    process.name,
    listening.port,
    process.pid
FROM processes AS process
JOIN listening_ports AS listening
ON process.pid = listening.pid