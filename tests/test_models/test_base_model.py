#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_model_instance_1 = BaseModel()
        base_model_instance_2 = BaseModel()
        self.assertNotEqual(base_model_instance_1.id, base_model_instance_2.id)

    def test_two_models_different_created_at(self):
        base_model_instance_1 = BaseModel()
        sleep(0.05)
        base_model_instance_2 = BaseModel()
        self.assertLess(base_model_instance_1.created_at,
                        base_model_instance_2.created_at)

    def test_two_models_different_updated_at(self):
        base_model_instance_1 = BaseModel()
        sleep(0.05)
        base_model_instance_2 = BaseModel()
        self.assertLess(base_model_instance_1.updated_at,
                        base_model_instance_2.updated_at)

    def test_str_representation(self):
        current_datetime = datetime.today()
        current_datetime_repr = repr(current_datetime)
        base_model_instance = BaseModel()
        base_model_instance.id = "123456"
        base_model_instance.created_at = base_model_instance.updated_at \
            = current_datetime
        base_model_str = base_model_instance.__str__()
        self.assertIn("[BaseModel] (123456)", base_model_str)
        self.assertIn("'id': '123456'", base_model_str)
        self.assertIn("'created_at': " + current_datetime_repr, base_model_str)
        self.assertIn("'updated_at': " + current_datetime_repr, base_model_str)

    def test_args_unused(self):
        base_model_instance = BaseModel(None)
        self.assertNotIn(None, base_model_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        current_datetime = datetime.today()
        current_datetime_iso = current_datetime.isoformat()
        base_model_instance = BaseModel(id="345",
                                        created_at=current_datetime_iso,
                                        updated_at=current_datetime_iso)
        self.assertEqual(base_model_instance.id, "345")
        self.assertEqual(base_model_instance.created_at, current_datetime)
        self.assertEqual(base_model_instance.updated_at, current_datetime)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        current_datetime = datetime.today()
        current_datetime_iso = current_datetime.isoformat()
        base_model_instance = BaseModel("12", id="345",
                                        created_at=current_datetime_iso,
                                        updated_at=current_datetime_iso)
        self.assertEqual(base_model_instance.id, "345")
        self.assertEqual(base_model_instance.created_at, current_datetime)
        self.assertEqual(base_model_instance.updated_at, current_datetime)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model_instance = BaseModel()
        sleep(0.05)
        first_updated_at = base_model_instance.updated_at
        base_model_instance.save()
        self.assertLess(first_updated_at, base_model_instance.updated_at)

    def test_two_saves(self):
        base_model_instance = BaseModel()
        sleep(0.05)
        first_updated_at = base_model_instance.updated_at
        base_model_instance.save()
        second_updated_at = base_model_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model_instance.save()
        self.assertLess(second_updated_at, base_model_instance.updated_at)

    def test_save_with_arg(self):
        base_model_instance = BaseModel()
        with self.assertRaises(TypeError):
            base_model_instance.save(None)

    def test_save_updates_file(self):
        base_model_instance = BaseModel()
        base_model_instance.save()
        base_model_id = "BaseModel." + base_model_instance.id
        with open("file.json", "r") as file:
            self.assertIn(base_model_id, file.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_model_instance = BaseModel()
        self.assertTrue(dict, type(base_model_instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        base_model_instance = BaseModel()
        self.assertIn("id", base_model_instance.to_dict())
        self.assertIn("created_at", base_model_instance.to_dict())
        self.assertIn("updated_at", base_model_instance.to_dict())
        self.assertIn("__class__", base_model_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_model_instance = BaseModel()
        base_model_instance.name = "Holberton"
        base_model_instance.my_number = 98
        self.assertIn("name", base_model_instance.to_dict())
        self.assertIn("my_number", base_model_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_model_instance = BaseModel()
        base_model_dict = base_model_instance.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        current_datetime = datetime.today()
        base_model_instance = BaseModel()
        base_model_instance.id = "123456"
        base_model_instance.created_at = base_model_instance.updated_at \
            = current_datetime
        expected_dict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': current_datetime.isoformat(),
            'updated_at': current_datetime.isoformat()
        }
        self.assertDictEqual(base_model_instance.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        base_model_instance = BaseModel()
        self.assertNotEqual(base_model_instance
                            .to_dict(), base_model_instance.__dict__)

    def test_to_dict_with_arg(self):
        base_model_instance = BaseModel()
        with self.assertRaises(TypeError):
            base_model_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
