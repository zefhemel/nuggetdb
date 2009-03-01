#!/usr/bin/env python

import MySQLdb
import nuggetdb.shard
from nuggetdb.entity import *

shard1 = nuggetdb.shard.Shard('main', MySQLdb, 'root', '', 'nuggetdb')
nuggetdb.shard.register(shard1)

zef = Entity()
zef.firstName = 'Zef'
zef.lastName = 'Hemel'
zef.age = 25
zef.put(shard1)

for e in Entity.all():
    print e.id
