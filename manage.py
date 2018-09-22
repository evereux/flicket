#! usr/bin/python3
# -*- coding: utf8 -*-

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from setup import RunSetUP
from application import app, db
from scripts.users_export_to_json import ExportUsersToJson
from scripts.users_import_from_json import ImportUsersFromJson
from scripts.update_user_posts import TotalUserPosts

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('run_set_up', RunSetUP)
manager.add_command('export_users', ExportUsersToJson)
manager.add_command('import_users', ImportUsersFromJson)
manager.add_command('update_user_posts', TotalUserPosts)
manager.add_command('runserver', Server(host="0.0.0.0", port=5000, use_reloader=True, use_debugger=True))

if __name__ == '__main__':
    manager.run()
