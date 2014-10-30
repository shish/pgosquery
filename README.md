About
-----

So I saw Facebook's OSQuery, and thought "That looks awesome, but complicated
to build on top of SQLite. Postgres' Foreign Data Wrappers seem like a much
better foundation. How long would it take to write the same app on top of
Postgres?". Turns out it takes about 15 minutes, for someone who's never
written an FDW before :-)

This approach does have the downside that it runs as the postgres user rather
than as root, so it can't see the full details of other people's processes,
but I'm sure that could be worked around if you really want to.


Installation
------------

Let your system python install know about this module:
```
sudo python setup.py develop
```
"setup.py develop" will link the current directory so you can modify it; "setup.py install" will copy a snapshot of current code to the OS folder.

Note that either way, you need to restart the postgres server to pick up python code changes.


Create a database with multicorn loaded (See http://multicorn.org/#installation for multicorn installation)
```
CREATE DATABASE pgosquery;
\c pgosquery;

CREATE EXTENSION multicorn;
```

Create a FDW table for PgOSQuery:
```
CREATE SERVER pgosquery_srv foreign data wrapper multicorn options (wrapper 'pgosquery.PgOSQuery');

pgosquery=# CREATE FOREIGN TABLE processes (
    pid integer,
    name character varying,
	username character varying
) server pgosquery_srv options (
    tabletype 'processes'
);  
```

Select data:
```
SELECT pid, name FROM processes;

  pid  | name                                                                                                                
-------+---------------
     1 | init
     2 | kthreadd
     3 | ksoftirqd/0
     5 | kworker/0:0H
     7 | rcu_sched
     8 | rcuos/0
     9 | rcuos/1
    10 | rcuos/2
    11 | rcuos/3
    12 | rcuos/4
    13 | rcuos/5
    14 | rcuos/6
    15 | rcuos/7
    16 | rcu_bh
    17 | rcuob/0
    18 | rcuob/1
   ... | ...
```


Tables
------

So far, the only table type is "processes". Columns are based on psutil's
attributes, see http://pythonhosted.org/psutil/#psutil.Process
