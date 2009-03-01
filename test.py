#!/usr/bin/env python

import MySQLdb
import db

shard1 = db.Shard('main', MySQLdb, 'root', '', 'nuggetdb')
db.register_shard(shard1)

zef = db.Entity()
zef.firstName = 'Zef'
zef.lastName = 'Hemel'
zef.age = 25
zef.put(shard1)

for e in db.Entity.all():
    print e.id
