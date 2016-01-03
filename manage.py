#!./venv/bin/python
import os

from flask.ext.script import Manager
from flask.ext.script.commands import Clean
from flask.ext.migrate import MigrateCommand, Migrate

from cheapflight import create_app
from cheapflight.ext import db


app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command(Clean())


@manager.shell
def context():
    return {'app': app}


@manager.command
def syncdb(destroy=False, verbose=False):
    if os.environ.get('PRODUCTION_CONFIG'):
        return

    import cheapflight.models.price_history

    db.engine.echo = bool(verbose)
    if destroy:
        db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
