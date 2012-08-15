import unittest

from ..models import Anima
from stark.data import load_world

class AnimaTestCase(unittest.TestCase): 
    def setUp(self):
        load_world.load_demo_rooms()
        self.anima = Anima({
            'key': 'anima', 
            'room': { 'key': 'center' }, 
            'stats': {
                'mp': 200
            }
        })
        
    def test_stats(self):
        self.assertEqual(1, 1)
        self.assertEqual(self.anima.stats.mp, 200)

if __name__ == "__main__":
    unittest.main()
