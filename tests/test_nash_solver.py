import unittest
import pytest
from nash_solver import find_mixed_nash, find_pure_nash
class TestNash(unittest.TestCase):
 def test_pd(self): self.assertEqual([(e.row,e.column) for e in find_pure_nash([[3,0],[5,1]],[[3,5],[0,1]])],[(1,1)])
 def test_matching(self):
  E=find_mixed_nash([[1,-1],[-1,1]],[[-1,1],[1,-1]])
  e=[x for x in E if len(x.row_support)==2][0]
  self.assertAlmostEqual(e.row_probabilities[0],.5)
 def test_rps(self):
  A=[[0,-1,1],[1,0,-1],[-1,1,0]]; B=[[-x for x in r] for r in A]
  e=[x for x in find_mixed_nash(A,B) if len(x.row_support)==3][0]
  for p in e.row_probabilities+e.column_probabilities:self.assertAlmostEqual(p,1/3)
 def test_5x5_uniform(self):
  # Cycle zero-sum generalise : unique equilibre completement mixte uniforme.
  A=[[0,1,-1,-1,1],[-1,0,1,-1,1],[1,-1,0,1,-1],[1,1,-1,0,-1],[-1,-1,1,1,0]]
  B=[[-x for x in r] for r in A]
  full=[e for e in find_mixed_nash(A,B) if len(e.row_support)==5]
  self.assertEqual(len(full),1)
  for p in full[0].row_probabilities+full[0].column_probabilities:self.assertAlmostEqual(p,.2)

 def test_battle_of_sexes_has_three_equilibria(self):
  A=[[2,0],[0,1]]; B=[[1,0],[0,2]]
  self.assertEqual(len(find_mixed_nash(A,B)),3)

 def test_rectangular_pure_nash(self):
  A=[[2,0,1],[0,2,1]]; B=[[2,0,1],[0,2,1]]
  self.assertGreaterEqual(len(find_pure_nash(A,B)),2)

 def test_no_interior_mixed_equilibrium(self):
  # Strictly dominant first actions imply that no fully mixed equilibrium exists.
  A=[[2,2],[0,0]]; B=[[2,0],[2,0]]
  self.assertFalse(any(len(e.row_support)>1 and len(e.column_support)>1
                       for e in find_mixed_nash(A,B)))

@pytest.mark.parametrize("A,B", [([[1,2]], [[1,2],[3,4]]), ([[1,2],[3]], [[1,2],[3,4]])])
def test_invalid_dimensions_raise(A,B):
 with pytest.raises(ValueError): find_mixed_nash(A,B)

@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_non_finite_payoffs_raise(bad):
 with pytest.raises(ValueError): find_mixed_nash([[bad]],[[0]])

@pytest.mark.parametrize("tol", [float("nan"), float("inf"), -float("inf"), -1.0, 0.0])
def test_invalid_tolerances_raise(tol):
 with pytest.raises(ValueError): find_mixed_nash([[1]],[[1]],tolerance=tol)

def test_empty_matrices_raise():
 with pytest.raises(ValueError): find_mixed_nash([],[])
 with pytest.raises(ValueError): find_mixed_nash([[]],[[]])
