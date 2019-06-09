from flask.cli import FlaskGroup
import os

from src import create_app, db
from src.api.models import User
import unittest
import coverage

COV = coverage.coverage(
    branch=True,
    include='src/*',
    omit=[
        'src/test/*',
        'src/config.py',
    ]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def test():
    tests = unittest.TestLoader().discover('src/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(User(
        username='phu555',
        email="phu555@test.com",
        firstName='phu',
        lastName='sakulwongtana',
        password='password1'
    ))
    db.session.add(User(
        username='phu556',
        email="phu556@test.com",
        firstName='phu2',
        lastName='sakulwongtana2',
        password='password1'
    ))
    db.session.commit()

@cli.command()
def cov():
    tests = unittest.TestLoader().discover('src/test')
    result = unittest.TextTestRunner(verbosity=0).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
