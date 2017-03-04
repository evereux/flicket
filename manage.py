#! usr/bin/python3
# -*- coding: utf8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from setup import RunSetUP
from application import app, db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('run_set_up', RunSetUP)

if __name__ == '__main__':
    manager.run()
