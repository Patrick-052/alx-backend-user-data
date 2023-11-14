#!/usr/bin/env python3
"""
BD class
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User


DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Method that saves a new user to the database """
        if not email or not hashed_password:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """find user by some arguments

        Returns:
            User: user found or raise error
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user

        Args:
            user_id (int): id of user
        """
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in DATA:
                raise ValueError
            setattr(user, key, val)
        self._session.commit()
        return None

# """DB module
# """
# from typing import TypeVar
# from user import Base, User
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.session import Session
# from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.ext.declarative import declarative_base


# class DB:
#     """DB class
#     """

#     def __init__(self) -> None:
#         """Initialize a new DB instance
#         """
#         self._engine = create_engine("sqlite:///a.db", echo=True)
#         Base.metadata.drop_all(self._engine)
#         Base.metadata.create_all(self._engine)
#         self.__session = None

#     @property
#     def _session(self) -> Session:
#         """Memoized session object
#         """
#         if self.__session is None:
#             DBSession = sessionmaker(bind=self._engine)
#             self.__session = DBSession()
#         return self.__session

#     def add_user(self, email: str, hashed_password: str) -> User:
#         """ Method that saves a new user to the database """
#         if not email or not hashed_password:
#             return None
#         new_user = User(email=email, hashed_password=hashed_password)
#         session = self._session
#         session.add(new_user)
#         session.commit()
#         return new_user

#     def find_user_by(self, **kwargs) -> User:
#         """ Method that returns the first row found in the users table
#             as  filtered by the method’s input arguments """
#         if kwargs:
#             for k in kwargs.keys():
#                 if not hasattr(User, k):
#                     raise InvalidRequestError

#             user = self._session.query(User).filter_by(**kwargs).first()
#             if not user:
#                 raise NoResultFound
#             return user
#         else:
#             raise InvalidRequestError

#     def update_user(self, user_id: int, **kwargs) -> None:
#         """ Method that takes as argument a required user_id integer
#             and arbitrary keyword arguments, and updates the user specific
#             rows with values of the keyword arguments """
#         if kwargs:
#             user = self.find_user_by(id=user_id)
#             for k, v in kwargs.items():
#                 if not hasattr(user, k):
#                     raise ValueError
#                 setattr(user, k, v)
#             self._session.commit()
#         else:
#             raise ValueError
