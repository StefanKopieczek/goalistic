# from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DEVELOPMENT_DB = 'sqllite://dev.db'


class DatabaseContext(object):
    def __init__(self, db_uri=None):
        if db_uri is None:
            print '** Using development database **'
            db_uri = DEVELOPMENT_DB
        self._db_uri = db_uri

    def connect(self):
        self.engine = create_engine(self.db_uri, echo=False)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.session.query_property()
        self._bind_models()
        self._ensure_schema()

    def _ensure_schema(self):
        # Create any DB models that don't currently exist.
        self.Base.metadata.create_all(self.engine, checkfirst=True)

    def _bind_models(self):

