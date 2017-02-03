from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from types import MethodType

DEVELOPMENT_DB = 'sqlite:///dev.db'


class DatabaseContext(object):
    def __init__(self, db_uri=None):
        if db_uri is None:
            print '** Using development database **'
            db_uri = DEVELOPMENT_DB
        self._db_uri = db_uri

    def connect(self):
        self.engine = create_engine(self._db_uri, echo=False)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.session.query_property()
        self._bind_models()
        self._ensure_schema()
        self._define_todict()

    def _define_todict(self):
        def _inner_todict(other):
            d = {}
            for prop in other.__class__._visible_attributes:
                if hasattr(other, prop):
                    d[prop] = getattr(other, prop)
            return d
        self.Base.to_dict = MethodType(_inner_todict, None, self.Base)

    def _ensure_schema(self):
        # Create any DB models that don't currently exist.
        self.Base.metadata.create_all(self.engine, checkfirst=True)

    def _bind_models(self):
        class User(self.Base):
            __tablename__ = 'user'
            _visible_attributes = ['id', 'name', 'email']
            id = Column(Integer, primary_key=True)
            email = Column(String)
            name = Column(String)
            goals = relationship('Goal', back_populates='user')
            measurements = relationship('Measurement', back_populates='user')
            meals = relationship('Meal', back_populates='user')
        self.User = User

        class Goal(self.Base):
            __tablename__ = 'goal'
            _visible_attributes = ['id', 'user_id', 'start_ts', 'end_ts', 'warmup_period']
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('user.id'))
            user = relationship('User', back_populates='goals')
            start_ts = Column(DateTime)
            end_ts = Column(DateTime)
            warmup_period = Column(Integer)
            loss_period = Column(Integer)
            loss_rate = Column(Integer)
        self.Goal = Goal

        class Measurement(self.Base):
            __tablename__ = 'measurement'
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('user.id'))
            user = relationship('User', back_populates='measurements')
            weight = Column(Integer)
            timestamp = Column(DateTime)
            is_estimate = Column(Boolean)
        self.Measurement = Measurement

        class Meal(self.Base):
            __tablename__ = 'meal'
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('user.id'))
            user = relationship('User', back_populates='meals')
            amount = Column(Integer)
            timestamp = Column(DateTime)
            is_estimate = Column(Boolean)
        self.Meal = Meal
