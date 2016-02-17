#!/usr/bin/env python
# coding: utf-8
import itertools
import logging
import time

import MySQLdb
import json

from base import BaseEngine


class Connection(object):
    """
    A wrapper around MySQLdb API connections.
    """

    def __init__(self, host, db, user=None, password=None,
                 max_idle_time=7 * 3600, connect_timeout=0,
                 charset="utf8"):
        self.host = host
        self.db = db
        self.max_idle_time = float(max_idle_time)

        args = dict(charset=charset, db=db, connect_timeout=connect_timeout)
        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

        pair = host.split(":")
        if len(pair) == 2:
            args["host"] = pair[0]
            args["port"] = int(pair[1])
        else:
            args["host"] = host
            args["port"] = 3306

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host, exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """
        Closes this database connection.
        """
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """
        Closes the existing database connection and re-opens it.
        """
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)

    def execute(self, query, *args, **kwargs):
        """
        Executes the given query, returning the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, args):
        """
        Executes the given query against all the given param sequences.
        Return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, args)
            return cursor.rowcount
        finally:
            cursor.close()

    def query(self, query, *args, **kwargs):
        """
        Returns a row list for the given query and parameters.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, args, kwargs)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def insert(self, query, *args, **kwargs):
        return self.execute(query, *args, **kwargs)

    def insertmany(self, query, args):
        return self.executemany(query, args)

    def _ensure_connected(self):
        # Mysql by default closes client connections that are idle for
        # 8 hours, but the client library does not report this fact until
        # you try to perform a query and it fails.  Protect against this
        # case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if (self._db is None or
            (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, args, kwargs):
        try:
            return cursor.execute(query, args or kwargs or None)
        except MySQLdb.OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host)
            self.close()
            raise


class Row(dict):
    """
    A dict that allows for object-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class MysqlEngine(BaseEngine):
    def __init__(self, host, db, user=None, password=None,
                 max_idle_time=7 * 3600, connect_timeout=0,
                 charset="utf8"):
        self.connection = Connection(host, db, user, password,
                                     max_idle_time, connect_timeout,
                                     charset)

    def save(self, addup_data):
        sql = """
            insert into polytope_statistics \
            set time_type=%s, time='%s', index_type=%s, index_str='%s', average='%s', distribute='%s', count='%s', addup_count=%s
        """ % (addup_data.time_type, addup_data.time, addup_data.index_type, addup_data.index,
           json.dumps(addup_data.average), json.dumps(addup_data.distribute), json.dumps(addup_data.count),
           addup_data.addup_count)
        self.connection.execute(sql)
