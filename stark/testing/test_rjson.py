"""
Test the RJSON implementation
"""

from stark.core.rjson import RJSON

import unittest
from stark.core.rjson import Registry

class RJSONTestCase(unittest.TestCase):
    def setUp(self):
        registry = Registry()
        registry.reset()

    def test_model(self):
        author = RJSON({'key': 'author', 'name':'john'})
        book = RJSON({ 'key': 'book', 'author': { 'key':'author' } })
        self.assertEqual(author, book.author)

    def test_model_reverse(self):
        book = RJSON({ 'key': 'book', 'author': { 'key': 'author' } })
        author = RJSON({'key': 'author', 'name': 'john'})
        self.assertEqual(author, book.author)

    def test_dict(self):
        author = RJSON({'foo': 'bar'})
        self.assertEqual(author.foo, 'bar')

    def test_nested_dict(self):
        author = RJSON({'key': 'author', 'name': {'first': 'john', 'last': 'doe'}})
        book = RJSON({'key':'book', 'author': { 'key':'author'}})
        self.assertEqual(book.author.name.first, 'john')
        self.assertEqual(book.author.name.__class__, RJSON)

    def test_typed_inheritence(self):
        class Author(RJSON): pass
        author = Author({'key': 'author', 'name': {'first': 'john', 'last': 'doe'}})
        self.assertTrue(isinstance(author, Author))

    # Disabling schema validation for now
    # def test_schema(self):
    #     class Model(RJSON):
    #        a = "required"
    #    with self.assertRaises(KeyError): Model({'foo': 'bar'})

    def test_collection(self):
        item1 = RJSON({'key': 'item1', 'name': 'Item1'})
        item2 = RJSON({'key': 'item2', 'name': 'Item2'})
        collection = RJSON({
            'key': 'collection',
            'contains': [
                {'key': 'item1'},
                {'key': 'item2'}
            ]})
        self.assertEqual(collection.contains[0].name, 'Item1')

    def test_root_lvl_collection(self):
        items = RJSON([
            {'key': 'item1', 'name': 'Item1'},
            {'key': 'item2', 'name': 'Item2'},
        ])
        self.assertEqual(isinstance(items, list), True)
        self.assertEqual(RJSON({'key': 'item1'}).name, 'Item1')

    def test_root_lvl_non_model_collection(self):
        items = RJSON(["abc", "def"])
        


