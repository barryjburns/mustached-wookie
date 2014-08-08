#!/usr/bin/python

import os, sys, subprocess, shlex, string, random, time, datetime, psycopg2, tempfile


pool = string.letters + string.digits
length = 32
root, project = os.path.split(os.path.split(os.path.abspath(__file__))[0])

random.seed()
passwd = ''.join(random.choice(pool) for idx in range(length))
tmpsql = tempfile.NamedTemporaryFile('w', 0)



try:
    tmpsql.write("drop database if exists %s;drop database if exists %s;create user %s password '%s';create database %s owner %s;" % (project, project, project, passwd, project, project))
    tmpsql.close()
    if subprocess.call("su postgres -c psql -1 -f '%s'" % tmpsql.name):
        raise RuntimeError('Error readying database.')
finally:
    del tmpsql

connection = psycopg2.connect('dbname=%s user=%s password=%s' % (project, project, passwd)


