TL;DR Example
-------------

```sql
--------------------------------------------------------
-- get the name, pid and attached port of all processes
-- which are listening on localhost interfaces
--------------------------------------------------------
SELECT DISTINCT
    process.name,
    listening.port,
    process.pid
FROM processes AS process
JOIN listening_ports AS listening
ON process.pid = listening.pid
WHERE listening.address = '127.0.0.1';
```

```psql
   name   | port | pid
----------+------+------
 postgres | 5432 | 6932

(1 row)
```


About
-----

So I saw Facebook's OSQuery[1], and thought "That looks awesome, but
complicated to build on top of SQLite. Postgres' Foreign Data Wrappers seem
like a much better foundation. How long would it take to write the same app
on top of Postgres?". Turns out it takes about 15 minutes, for someone who's
never written an FDW before :-)

This approach does have the downside that it runs as the postgres user rather
than as root, so it can't see the full details of other people's processes,
but I'm sure that could be worked around if you really want to.

Currently this is just a proof-of-concept to see how useful Postgres' foreign
data wrappers are, and how easy they are to create with the Multicorn python
library. Seems the answers are "very useful" and "very easy". If people want
to make this more useful by adding more virtual tables, pull requests are
welcome~

[1] https://github.com/facebook/osquery


Installation
------------

Let your system python install know about this module:
```
sudo python setup.py develop
```
"setup.py develop" will link the current directory so you can modify it; "setup.py install" will copy a snapshot of current code to the OS folder.

Note that either way, you need to restart the postgres server to pick up python code changes.


Create a database with multicorn loaded (See http://multicorn.org/#installation for multicorn installation)
```sql
CREATE DATABASE pgosquery;
\c pgosquery;

CREATE EXTENSION multicorn;
```

Create a FDW table for PgOSQuery:
```sql
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
```

Select data:
```sql
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
```

```psql
   name   | port | pid
----------+------+------
 postgres | 5432 | 6932

(1 row)
```


Table Types
-----------

processes:

Columns are based on psutil's Process attributes, see http://pythonhosted.org/psutil/#psutil.Process


listening_ports:

columns: pid, address, port
