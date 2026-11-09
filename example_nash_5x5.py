from nash_solver import find_mixed_nash
A=[[0,1,-1,-1,1],[-1,0,1,-1,1],[1,-1,0,1,-1],[1,1,-1,0,-1],[-1,-1,1,1,0]]
B=[[-x for x in r] for r in A]
for e in find_mixed_nash(A,B): print(e)
