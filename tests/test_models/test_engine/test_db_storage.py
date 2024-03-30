#!/usr/bin/python3
""" Module for testing database storage"""
import unittest
from models.base_model import BaseModel
from models import storage, type_of_storage


@unittest.skipIf(type_of_storage != "db", "Testing DB storage only")
class TestDBStorage(unittest.TestCase):
    """ Class for testing database storage"""

    def test_all(self):
        """ Test the all method"""
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)
