import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevelopmentConfig(object):
    DEBUG = True
    MEMCACHED_SERVERS = ["localhost:11211"]
    PERMDIRS = os.path.join(PROJECT_DIR, "permdirs")
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % os.path.join(PERMDIRS, "database.sqlite")
