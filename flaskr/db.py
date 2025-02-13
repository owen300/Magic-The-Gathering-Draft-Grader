import sqlite3

import click
from flask import current_app, g
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.Parser import logHandler



logs=logHandler()

def get_db():#creates a db if there is non and returns it
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def close_db(e=None):#closes the db
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():#gets the db setup
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) #setup format

    db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
            ("admin", generate_password_hash("123456")),)#creates a sample user for testing

    db.commit()


@click.command('init-db')
def init_db_command():#init command to run from command line
    """Clear the existing data and create new tables."""
    init_db()
    logs.initialize_json()
    click.echo('Initialized the database.')