#!/usr/bin/env python

import MySQLdb
import nuggetdb.shard
from nuggetdb.entity import *

shard1 = nuggetdb.shard.Shard('shard1', MySQLdb, 'root', '', 'nuggetdb', table_prefix='shard1_')
shard1.create()
nuggetdb.shard.register(shard1)
shard2 = nuggetdb.shard.Shard('shard2', MySQLdb, 'root', '', 'nuggetdb', table_prefix='shard2_')
shard2.create()
#nuggetdb.shard.register(shard2)

zef = Entity(ns='User')
zef.firstName = 'Zef'
zef.lastName = 'Hemel'
zef.age = 25
zef.put(nuggetdb.shard.random_pick())

p = Entity(ns='Page')
p.url = 'http://zef.me'
p.put(nuggetdb.shard.random_pick())

for e in Entity.all_in_ns('User'):
    print e.id, e.firstName, e.lastName
