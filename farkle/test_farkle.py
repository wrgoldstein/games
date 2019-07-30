from unittest import TestCase
from farkle import Farkle, Player

class TestFarkle(TestCase):
    def test_five_of_anything(self):
        self.assertEqual(
            Farkle.five_of_anything([1,1,1,1,1,5]),
            (2000, [1,1,1,1,1], [5])
        )

        self.assertIsNone(
            Farkle.five_of_anything([1,1,1,1,2,5])
        )

    def test_score_remaining(self):
        score = Farkle.score([1,1,5,2,3,4])
        score = sorted(score, key=lambda x: x[0])
        self.assertEqual(
            score, 
            [
                (50, [5], [1,1,2,3,4]),
                (100, [1], [1,5,2,3,4]),
                (150, [1,5], [1,2,3,4]),
                (200, [1,1], [5,2,3,4]),
                (250, [1,1,5], [2,3,4]),
                
            ]
        )

    def test_score_remaining2(self):
        score = Farkle.score([6,6,6,5,1,4])
        score = sorted(score, key=lambda x: x[0])
        self.assertEqual(
            score, 
            [
                (50, [5], [6, 6, 6, 1, 4]), 
                (100, [1], [6, 6, 6, 5, 4]), 
                (150, [1, 5], [6, 6, 6, 4]), 
                (600, [6, 6, 6], [5, 1, 4]), 
                (650, [6, 6, 6, 5], [1, 4]), 
                (700, [6, 6, 6, 1], [5, 4]), 
                (750, [6, 6, 6, 1, 5], [4])
            ]
        )
    
    def test_strategy3(self):
        options = [
            (300, [3, 3, 3], [1, 2, 2]),
            (400, [3, 3, 3, 1], [2, 2]),
            (100, [1], [3, 3, 3, 2, 2])
        ]
        self.assertEqual(Player.strategy3([], options)[0], 300)

        options = [
            (100, [1], [3, 5, 3, 2, 2]),
            (150, [1, 5], [3, 3, 2, 2]),
            (50, [5], [3, 3, 1, 2, 2])
        ]
        self.assertEqual(Player.strategy3([], options)[0], 100)

        options = [
            (1000, [6, 6, 6, 6], [1, 2]),
            (1100, [6, 6, 6, 6, 1], [2]),
            (600, [6, 6, 6], [6, 1, 2]),
            (700, [6, 6, 6, 1], [6, 2]),
            (100, [1], [6, 6, 6, 6, 2])
        ]
        self.assertEqual(Player.strategy3([], options)[0], 1100)

    def test_strategy2(self):
        options = [
            (300, [3, 3, 3], [1, 2, 2]),
            (400, [3, 3, 3, 1], [2, 2]),
            (100, [1], [3, 3, 3, 2, 2])
        ]
        self.assertEqual(Player.strategy2([], options)[0], 100)

        options = [
            (100, [1], [3, 5, 3, 2, 2]),
            (150, [1, 5], [3, 3, 2, 2]),
            (50, [5], [3, 3, 1, 2, 2])
        ]
        self.assertEqual(Player.strategy2([], options)[0], 100)

        options = [
            (1000, [6, 6, 6, 6], [1, 2]),
            (1100, [6, 6, 6, 6, 1], [2]),
            (600, [6, 6, 6], [6, 1, 2]),
            (700, [6, 6, 6, 1], [6, 2]),
            (100, [1], [6, 6, 6, 6, 2])
        ]
        self.assertEqual(Player.strategy2([], options)[0], 1100)