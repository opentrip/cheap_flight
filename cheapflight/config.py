import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = False
    MEMCACHED_SERVERS = ["localhost:11211"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % os.path.join(
        PROJECT_DIR,
        ".tmp_permdirs",
        "dev_database.sqlite"
    )


class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///%s" % os.path.join(
        PROJECT_DIR,
        ".tmp_permdirs",
        "testing_database.sqlite"
    )
