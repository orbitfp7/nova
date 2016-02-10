# Copyright (c) 2015 Umea University
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table

from nova.db.sqlalchemy import api as db
from nova.db.sqlalchemy import utils


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    table = Table('fault_tolerance_relations', meta,
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('created_at', DateTime),
                  Column('updated_at', DateTime),
                  Column('deleted_at', DateTime),
                  Column('deleted', Integer),
                  Column('primary_instance_uuid', String(length=36),
                         nullable=False),
                  Column('secondary_instance_uuid', String(length=36),
                         nullable=False),
                  mysql_engine='InnoDB',
                  mysql_charset='utf8')

    table.create()
    utils.create_shadow_table(migrate_engine, table=table)

    if migrate_engine.name == 'mysql' or migrate_engine.name == 'postgresql':
        Index('fault_tolerance_relations_primary_instance_uuid_idx',
              table.c.primary_instance_uuid).create(migrate_engine)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    name = 'fault_tolerance_relations'
    table = Table(name, meta, autoload=True)
    table.drop()
    table = Table(db._SHADOW_TABLE_PREFIX + name, meta, autoload=True)
    table.drop()
