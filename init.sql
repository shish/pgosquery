create user pgosquery with password 'pgosquery';
create database pgosquery with owner pgosquery;
\c pgosquery;
CREATE EXTENSION multicorn;

CREATE SERVER pgosquery_srv foreign data wrapper multicorn options (
	wrapper 'pgosquery.PgOSQuery'
);

CREATE FOREIGN TABLE processes (
	pid integer,
	name character varying
) server pgosquery_srv options (
	tabletype 'processes'
);

select pid, name from processes;
