#!/usr/bin/python3
""" Module for testing DB storage """
from os import getenv
import unittest
from models.base_model import BaseModel
from models import storage
import models
import os
from models.state import State
from models.user import User


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "DBStorage")
class TestDBStorage(unittest.TestCase):
    """ Class to test the database storage method """

    def test_all(self):
        """ method to test the all method of dbStorage """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_get(self):
        """Test that get returns specific object, or none"""
        new_state = State(name="New York")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "blah"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count(self):
        """test that new adds an object to the database"""
        initial_count = models.storage.count()
        new_state = State(name="Florida")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertEqual(models.storage.count("State"), initial_count + 1)
        self.assertEqual(models.storage.count(), initial_count + 2)
