# -*- coding:utf-8 -*-

import MySQLdb
import lxml.html
from lxml.html import builder as E


class AutoConnection(object):
    def __init__(self, *args, **kwargs):
        self.conn = None
        self.cursor = None
        self.conn_args = args
        self.conn_kwargs = kwargs

    def connect(self):
        self.conn = MySQLdb.connect(*self.conn_args, **self.conn_kwargs)
        return self.conn

    def cursor(self):
        if not self.cursor:
            self.cursor = self.conn.cursor()
        return self.cursor

    def close(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()

    def execute(self, *args):
        """
        fix MySQL server has gone away

        :param args:  MySQLdb.execute args
        """
        try:
            self.cursor.execute(*args)
            self.conn.commit()
        except (AttributeError, MySQLdb.OperationalError):
            conn = MySQLdb.connect(*self.conn_args, **self.conn_kwargs)
            self.cursor = conn.cursor()
            self.cursor.execute(*args)
            self.conn.commit()

# global conn
host = '10.211.253.26'
user = 'dbn_admin'
password = 'oM0bmpKc-O'
db = 'rid'
conn = AutoConnection(host, user, password, db)


class Table(object):
    def __init__(self, length):
        self.length = length
        self.head = None
        self.body = []

    def tr(self, label, data):
        """
        :param label: "th" or "td"
        :type data: list
        """
        if len(data) != self.length:
            raise IndexError('table out of length')
        label = getattr(E, label)
        return E.TR(*tuple(label(td) for td in data))

    def add_head(self, data):
        self.head = E.THEAD(self.tr('TH', data))

    def add_body_tr(self, data):
        self.body.append(self.tr('TD', data))

    def table(self):
        return E.TABLE(
            self.head,
            E.TBODY(*self.body),
            border="1"
        )


t = Table(3)
t.add_head(["name", "age", "sex"])
t.add_body_tr(["web", "30", "male"])
table1 = t.table()

t = Table(4)
t.add_head(["id", "max", "min", "conn"])
t.add_body_tr(["1", "9", "4", "14"])
t.add_body_tr(["2", "14", "2", "8"])
table2 = t.table()

port = 3306
dead_lock_information = "dead lock"
img_base_64 = "IMGBASE64"
html = E.HTML(E.BODY(
    E.H1("MySQL Port:{0}".format(port)),
    table1,
    table2,
    E.IMG(src="data:image/png;base64,{0}".format(img_base_64)),
    E.H1("DEAD LOCK"),
    E.PRE(dead_lock_information)
))

print lxml.html.tostring(html)
