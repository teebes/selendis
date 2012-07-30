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
        book = Model({ 'key': 'book', 'author': { 'key': 'author' } })
        author = Model({'key': 'author', 'name': 'john'})
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

    def test_collection(self):
        item1 = Model({'key': 'item1', 'name': 'Item1'})
        item2 = Model({'key': 'item2', 'name': 'Item2'})
        collection = Model({
            'key': 'collection',
            'contains': [
                {'key': 'item1'},
                {'key': 'item2'}
            ]})
        self.assertEqual(collection.contains[0].name, 'Item1')

    def test_root_lvl_collection(self):
        items = Model([
            {'key': 'item1', 'name': 'Item1'},
            {'key': 'item2', 'name': 'Item2'},
        ])
        self.assertEqual(isinstance(items, list), True)
        self.assertEqual(Model({'key': 'item1'}).name, 'Item1')

    def test_root_lvl_non_model_collection(self):
        items = Model(["abc", "def"])
        

if __name__ == "__main__":
    unittest.main()

