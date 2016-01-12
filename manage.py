#!/usr/bin/python
import os

from flask.ext.script import Manager
from flask.ext.script.commands import Clean
from flask.ext.migrate import MigrateCommand, Migrate

from cheapflight import create_app
from cheapflight.ext import db

# import for migrating
import cheapflight.models.price_history

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command(Clean())


@manager.shell
def context():
    return {"app": app, "db": db}


if __name__ == '__main__':
    manager.run()
