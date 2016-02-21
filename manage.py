#!/usr/bin/python
import os

from werkzeug.utils import import_string
from flask.ext.script import Manager
from flask.ext.script.commands import Clean
from flask.ext.migrate import MigrateCommand, Migrate

from cheapflight import create_app
from cheapflight.ext import db

# import for migrating
import cheapflight.models  # noqa

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command(Clean())


@manager.command
def runscript(script_path):
    '''
    Run Function. e.g.:
    cheapflight.scripts.rader:main or
    cheapflight/scripts/rader.py with main()
    '''
    if ":" not in script_path:
        script_path = os.path.expanduser(os.path.expandvars(script_path))
        script_path = os.path.relpath(script_path)
        script_path = script_path.rstrip(".py")
        script_path = script_path.replace(os.path.sep, ".")
        script_path = script_path.lstrip(".")
        script_path = "%s:main" % script_path

    import_string(script_path)()


@manager.shell
def context():
    return {"app": app, "db": db}


if __name__ == '__main__':
    manager.run()
