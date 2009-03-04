#!/usr/bin/env python

import MySQLdb
import nuggetdb.shard
from nuggetdb.entity import *
from nuggetdb.index import Index

shard1 = nuggetdb.shard.Shard('shard1', MySQLdb, 'root', '', 'nuggetdb', table_prefix='shard1_')
shard1.create()
nuggetdb.shard.register(shard1)
shard2 = nuggetdb.shard.Shard('shard2', MySQLdb, 'root', '', 'nuggetdb', table_prefix='shard2_')
shard2.create()
#nuggetdb.shard.register(shard2)

idx1 = Index(ns="User", columns=['firstName', 'lastName'], column_types=[str, str], shard=shard2)
idx1.create()

idx2 = Index(ns="User", columns=['lastName'], column_types=[str], shard=shard2)
idx2.create()

zef = Entity(ns='User')
zef.firstName = 'Zef'
zef.lastName = 'Hemel'
zef.age = 25
zef.put(nuggetdb.shard.random_pick())

p = Entity(ns='Page')
p.url = 'http://zef.me'
p.put(nuggetdb.shard.random_pick())

idx1.update()
idx2.update()

for e in Entity.all_in_ns(None):
    print e.id#, e.firstName, e.lastName
