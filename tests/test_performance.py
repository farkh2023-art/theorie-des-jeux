import random,time,unittest
import pytest
from nash_solver import find_mixed_nash,_support_pairs

def game(n,seed):
 r=random.Random(seed); return ([[r.randint(-20,20) for _ in range(n)] for _ in range(n)],[[r.randint(-20,20) for _ in range(n)] for _ in range(n)])
class TestPerformance5x5(unittest.TestCase):
 def test_support_cache_5x5(self):
  self.assertIs(_support_pairs(5,5),_support_pairs(5,5))
  self.assertEqual(len(_support_pairs(5,5)),226)
 def test_three_5x5_under_budget(self):
  cases=[game(5,s) for s in range(3)]; start=time.perf_counter()
  for A,B in cases: find_mixed_nash(A,B)
  self.assertLess(time.perf_counter()-start,5.0)

@pytest.mark.performance
def test_100_games_2x2_under_wide_budget():
 cases=[game(2,s) for s in range(100)]; start=time.perf_counter()
 for A,B in cases: find_mixed_nash(A,B)
 assert time.perf_counter()-start < 30.0

@pytest.mark.performance
def test_one_game_4x4_under_wide_budget():
 A,B=game(4,404); start=time.perf_counter(); find_mixed_nash(A,B)
 assert time.perf_counter()-start < 30.0
