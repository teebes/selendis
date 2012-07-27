"""
Test the RJSON implementation
"""


from stark.core.rjson import Model
from stark.core.rjson import registry

import unittest

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        registry.reset()

    def test_model(self):
        author = Model({'key': 'author', 'name':'john'})
        book = Model({ 'key': 'book', 'author': { 'key':'author' } })
        self.assertEqual(author, book.author)

    def test_model_reverse(self):
        author = Model({'key': 'author', 'name': 'john'})
        book = Model({ 'key': 'book', 'author': { 'key': 'author' } })
        self.assertEqual(author, book.author)

    def test_dict(self):
        author = Model({'foo': 'bar'})
        self.assertEqual(author.foo, 'bar')

    def test_nested_dict(self):
        author = Model({'key': 'author', 'name': {'first': 'john', 'last': 'doe'}})
        book = Model({'key':'book', 'author': { 'key':'author'}})
        self.assertEqual(book.author.name.first, 'john')

    def test_schema(self):
        class MyModel(Model):
            a = "required"
        with self.assertRaises(KeyError): MyModel({'foo': 'bar'})
        
 

if __name__ == "__main__":
    unittest.main()

