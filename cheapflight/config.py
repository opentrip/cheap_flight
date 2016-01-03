class DevelopmentConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://dev:dev@localhost/dev_cheapflight"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEMCACHED_SERVERS = ["localhost:11211"]
