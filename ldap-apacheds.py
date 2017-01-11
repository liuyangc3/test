# -*- coding:utf-8 -*-
import ldap

# bind
dn = "uid=liuyangc3,ou=system"
pw = "xxxxxxxxx"
conn = ldap.initialize("ldap://a.b.c:10389")
conn.simple_bind_s(dn, pw)

conn.set_option(ldap.OPT_REFERRALS, 0)
conn.protocol_version = ldap.VERSION3

try:
    for entry in conn.search_s('uid=liuyangc3,ou=developer,dc=nxin,dc=com', scope=ldap.SCOPE_SUBTREE):
        print(entry)
except Exception, e:
    print e
