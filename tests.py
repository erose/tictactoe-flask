# -*- coding: utf-8 -*-
import unittest
import app
from app import score

class TestingBadRequests(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_400_on_ill_formatted_board(self):
        r = self.app.get('/', query_string="board=AAA")
        self.assertEqual(r.status_code, 400)

        r = self.app.get('/', query_string="board=       oxx") # 10 characters
        self.assertEqual(r.status_code, 400)

        r = self.app.get('/', query_string="board=é      ox")
        self.assertEqual(r.status_code, 400)

    def test_400_on_no_board_provided(self):
        r = self.app.get('/', query_string="bored=xx oo xox")
        self.assertEqual(r.status_code, 400)
        
    def test_400_on_full_board(self):
        r = self.app.get('/', query_string="board=xxxoooxox")
        self.assertEqual(r.status_code, 400)

    def test_400_on_winning_board(self):
        r = self.app.get('/', query_string="board=xxx   ooo")
        self.assertEqual(r.status_code, 400)

    def test_400_on_not_plausibly_os_turn(self):
        r = self.app.get('/', query_string="board=xxx      ")
        self.assertEqual(r.status_code, 400)

class TestingGoodRequests(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_easy_board(self):
        # Lincoln's example given in the google doc.
        r = self.app.get('/', query_string="board= xxo  o  ")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_data(), 'oxxo  o  ')

class TestingIsWinner(unittest.TestCase):
    def test_winning_boards(self):
        self.assertTrue(app.is_winner('xxxoo    ', player='x'))

    def test_non_winning_boards(self):
        self.assertFalse(app.is_winner('xx xooooo', player='x'))

class TestingOptimality(unittest.TestCase):
    def test_score_winning_and_losing_base_cases(self):
        self.assertEqual(score('xxx      ', player='x'), 1)
        self.assertEqual(score('xxx      ', player='o'), -1)

        self.assertEqual(score('o  o  o  ', player='o'), 1)
        self.assertEqual(score('o  o  o  ', player='x'), -1)
        self.assertEqual(score('x  x  x  ', player='x'), 1)
        self.assertEqual(score('x  x  x  ', player='o'), -1)

    def test_score_tie_base_cases(self):
        self.assertEqual(score('xoooxxoxo', player='x'), 0)
        self.assertEqual(score('xoooxxoxo', player='o'), 0)

    def test_score_easy_board_can_win(self):
        self.assertEqual(score('oo xx    ', player='o'), 1)
        self.assertEqual(score('oo xx    ', player='x'), 1)

    @unittest.skip("takes a long time")
    def test_score_blank_board_is_tie(self):
        self.assertEqual(score('         ', player='o'), 0)
        self.assertEqual(score('         ', player='x'), 0)

if __name__ == "__main__":
    unittest.main()
