class DevelopmentConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://dev:dev@localhost/dev_cheapflight"
    MEMCACHED_SERVERS = ["localhost:11211"]
