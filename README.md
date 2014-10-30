

```
sudo python setup.py install
```

```
CREATE DATABASE pgosquery;
\c pgosquery;

CREATE EXTENSION multicorn;

CREATE SERVER pgosquery_srv foreign data wrapper multicorn options (wrapper 'pgosquery.PgOSQuery');

pgosquery=# CREATE FOREIGN TABLE processes (
    pid integer,
    name character varying
) server pgosquery_srv options (
    tabletype 'processes'
);  

SELECT pid, name FROM processes;
```

```
  pid  | name                                                                                                                
-------+-----------------------------------------------
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
```
