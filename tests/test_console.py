#!/usr/bin/python3
"""Module for testing console"""

import unittest
import os
import sys
from unittest.mock import patch
from console import HBNBCommand
from io import StringIO
from models import storage


class test_command(unittest.TestCase):
    """Class to test the console"""

    def setUp(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

        storage.__objects = {}

    def test_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            self.assertTrue(len(f.getvalue()) > 0)

    def test_create_error(self):
        """test if create works right"""
        temp_out = StringIO()
        sys.stdout = temp_out

        self.hbtn.onecmd("create")
        self.assertEqual(temp_out.getvalue(), '** class name missing **\n')
        temp_out.close()

        temp_out = StringIO()
        sys.stdout = temp_out
        HBNBCommand().do_create("base")
        self.assertEqual(temp_out.getvalue(), '** class doesn\'t exist **\n')
        temp_out.close()

        temp_out = StringIO()
        sys.stdout = temp_out
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            HBNBCommand().do_create("BaseModel")
            self.assertTrue(temp_out.getvalue() != "")
        temp_out.close()
        sys.stdout = sys.__stdout__

    def test_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(f.getvalue(), "** instance id missing **\n")

    def test_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue(), "** instance id missing **\n")

    def test_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            self.assertEqual(f.getvalue(), "[]\n")


if __name__ == "__main__":
    unittest.main()
