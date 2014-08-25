# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from htmapp.web.application_factory import create_app, init_app
from GunicornServer import GunicornServer

app = create_app()
init_app(app)
manager = Manager(app)

manager.add_command("gunicorn", GunicornServer())

@manager.command
def hello():
    """
    Print hello
    """
    from htmapp.logger import get_logger
    get_logger().debug("Hello debug")
    get_logger().info("Hello info")
    get_logger().warning("Hello warning")
    get_logger().error("Hello error")
    get_logger().critical("Hello critical")
    print "hello"

@manager.command
def init_db():
    """
    Drop and create database
    """
    from htmapp.db.create import init_database
    init_database()

@manager.command
def update_tags():
    """
    Update tags in database
    """
    from htmapp.datagrabber.tags_updater import update_tags
    update_tags(app.config['REQUEST_THREADS_COUNT'], app.config['SUMMARIZE_THREADS_COUNT'], app.config['TAGS_MEMORY'])

if __name__ == "__main__":
    manager.run()