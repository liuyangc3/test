# -*- coding:utf-8 -*-
import sys
import requests

_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


try:
    import simplejson as json
except (ImportError, SyntaxError):
    # simplejson does not support Python 3.2, it throws a SyntaxError
    # because of u'...' Unicode literals.
    import json

if is_py2:
    from urlparse import parse_qs
    from cookielib import CookieJar


if is_py3:
    from urllib.parse import parse_qs
    from http.cookiejar import CookieJar


class RidClient(object):
    """
    url: 'http://rid.t.nxin.com'
    """
    def __init__(self, url):
        self.url = url
        self.cookie = None

    def login(self, user, password):
        jar = CookieJar()
        response = requests.post(
            self.url + '/Login', data={'userName': user, 'password': password}, cookies=jar)

        # {"code": 0, "data": 0}
        # {"code": 1, "error": "用户不存在"}
        # {"code": 2, "error": "密码错误"}
        data = json.loads(response.text)
        print(data)
        if data["code"] != 0:
            raise ValueError(data["error"])
        self.cookie = jar

    class Database(object):
        """
        usage:
            db = Database()
            master = db.new_db('rid', '172.16.0.1', '3306', '5.6')
            examine = db.new_db('rid', '172.16.0.1', '3306', '5.6')
            db.master = master
            db.add_salve('172.16.0.1', '3307')
            db.examine('172.16.0.1', '3308')
            print db.to_dict()
        """
        def __init__(self):
            self.master = None
            self.examine = None
            self.slaves = []

        @staticmethod
        def new_db(name, ip, port, version):
            return {
                "name": name,
                "ip": ip,
                "port": port,
                "dbVersion": version
            }

        def add_slave(self, ip, port):
            self.slaves.append(
                self.new_db(self.master['name'], ip, port, self.master['version']))

        def remove_salve(self, ip, port):
            self.slaves = filter(
                lambda s: s['ip'] != ip and s['port'] != port, self.slaves)

        def examine(self, ip, port):
            self.examine = self.new_db(self.master['name'], ip, port, self.master['version'])

        def to_dict(self):
            data = dict.copy(self.master)
            data["slaves"] = self.slaves
            data["slaves"] = self.examine
            return data

    def add_db_resource(self, name, ip, port, version):
        db = self.Database()
        db.master = db.new_db(name, ip, port, version)
        s = requests.Session()
        prepped = s.prepare_request(requests.Request(
            'POST',
            "{0}/resource/addDbResource".format(self.url),
            data=db.to_dict(),
            cookies=self.cookie))
        req_body = parse_qs(prepped.body)
        prepped.body = "db={0}".format(req_body["db"][0]).replace('\'', '"')
        prepped.headers['Content-Length'] = len(prepped.body)
        res = s.send(prepped)
        print(res.text, res.status_code)

