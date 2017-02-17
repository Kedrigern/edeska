# manage.py


import os
import unittest
import coverage

from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app, db
from project.server.models import User, Post


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    posts = [
        Post('Spuštění nové elektronické desky', 'Pirátská strana má nový nástroj pro vnitřní informování členů a přiznivců!', 'Ondřej Profant'),
        Post('Volba: PKS Praha', 'Řádná volba předsednictva KS Praha proběhne 17. 11. ', 'Tobias Esner'),
        Post('Veřejná soutěž: grafika stranického webu', 'Lorem ipsum', 'Mikuláš Ferjenčík'),
        Post('Výběrové řízení: psavec', 'Požadavky:\n\n* pravopis\n* znalost pirátské filosofie\n- časová flexibilita', 'Mikuláš Ferjenčík'),
        Post('Výběrové řízení: koordinátor dobrovolníků', 'Požadavky:\n* práce s lidmi\n* znalost pirátské filosofie', 'Jakub Nepejchal'),
        Post('Volba: RP', 'Řádná volba republikového předsednictva strany probíhají na CF', 'Tobias Esner')
    ]
    posts[0].priority = 2
    posts[0].category = 1
    posts[1].category = 2
    posts[-1].category = 2
    posts[2].category = 3
    posts[3].category = 3
    posts[4].category = 3
    db.session.add_all(posts)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
