"""Solveur de Nash optimise pour jeux bimatriciels finis a deux joueurs."""
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from typing import List, Sequence, Tuple
import numpy as np

Matrix = Sequence[Sequence[float]]

@dataclass(frozen=True)
class PureNashEquilibrium:
    row: int
    column: int
    payoffs: Tuple[float, float]

@dataclass(frozen=True)
class MixedNashEquilibrium:
    row_probabilities: Tuple[float, ...]
    column_probabilities: Tuple[float, ...]
    expected_payoffs: Tuple[float, float]
    row_support: Tuple[int, ...]
    column_support: Tuple[int, ...]

def _arrays(row_payoffs, column_payoffs):
    A=np.asarray(row_payoffs,dtype=float); B=np.asarray(column_payoffs,dtype=float)
    if A.ndim!=2 or A.size==0 or B.shape!=A.shape:
        raise ValueError('Les matrices doivent etre non vides, rectangulaires et de memes dimensions.')
    if not np.isfinite(A).all() or not np.isfinite(B).all():
        raise ValueError('Les gains doivent etre finis.')
    return np.ascontiguousarray(A),np.ascontiguousarray(B)

def _validate_tolerance(tolerance):
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError('tolerance doit etre finie et strictement positive.')

@lru_cache(maxsize=64)
def _support_pairs(m, n):
    """Met en cache les 226 paires de supports non purs d'un jeu 5x5."""
    pairs=[]
    for k in range(2,min(m,n)+1):
        rows=tuple(combinations(range(m),k)); cols=tuple(combinations(range(n),k))
        pairs.extend((I,J) for I in rows for J in cols)
    return tuple(pairs)

def _pure_arrays(A,B,tol):
    # Calcul vectorise des meilleures reponses.
    row_best=A >= A.max(axis=0,keepdims=True)-tol
    col_best=B >= B.max(axis=1,keepdims=True)-tol
    return np.argwhere(row_best & col_best)

def find_pure_nash(row_payoffs, column_payoffs, tolerance=1e-9):
    """Return pure epsilon-Nash equilibria.

    ``tolerance`` is both the probability cutoff at or below which a support
    probability is treated as zero and the maximum tolerated unilateral
    deviation gain. Returned equilibria are therefore epsilon-equilibria
    under this threshold.
    """
    _validate_tolerance(tolerance)
    A,B=_arrays(row_payoffs,column_payoffs)
    return [PureNashEquilibrium(int(i),int(j),(float(A[i,j]),float(B[i,j])))
            for i,j in _pure_arrays(A,B,tolerance)]

def _solve_indifference(C,tol):
    k=C.shape[0]
    # Allocation directe, plus legere que np.block dans la boucle critique.
    M=np.empty((k+1,k+1),dtype=float)
    M[:k,:k]=C; M[:k,k]=-1.0; M[k,:k]=1.0; M[k,k]=0.0
    rhs=np.zeros(k+1,dtype=float); rhs[k]=1.0
    try: sol=np.linalg.solve(M,rhs)
    except np.linalg.LinAlgError: return None
    probs=sol[:k]
    if probs.min() <= tol: return None
    total=probs.sum()
    if total <= tol: return None
    return probs/total,float(sol[k])

def find_mixed_nash(row_payoffs, column_payoffs, tolerance=1e-9):
    """Enumere les equilibres epsilon-isoles par supports de meme cardinalite.

    ``tolerance`` est a la fois le seuil en dessous duquel ou auquel une
    probabilite est traitee comme nulle et le gain maximal de deviation
    unilaterale tolere.
    Les resultats sont donc des epsilon-equilibres pour cette tolerance.

    Optimisations 5x5 : supports mis en cache, cas purs vectorise, allocations
    reduites, sous-matrices extraites par indexation directe et verifications
    numeriques differees jusqu'apres les tests de meilleure reponse.
    """
    _validate_tolerance(tolerance)
    A,B=_arrays(row_payoffs,column_payoffs); m,n=A.shape; found=[]
    # Cas purs sans solveur lineaire.
    for i,j in _pure_arrays(A,B,tolerance):
        x=np.zeros(m); y=np.zeros(n); x[i]=1.0; y[j]=1.0
        found.append(MixedNashEquilibrium(tuple(map(float,x)),tuple(map(float,y)),
            (float(A[i,j]),float(B[i,j])),(int(i),),(int(j),)))
    # Supports mixtes uniquement.
    for I,J in _support_pairs(m,n):
        ii=np.fromiter(I,dtype=np.intp); jj=np.fromiter(J,dtype=np.intp)
        rq=_solve_indifference(A[ii[:,None],jj],tolerance)
        if rq is None: continue
        rp=_solve_indifference(B[ii[:,None],jj].T,tolerance)
        if rp is None: continue
        q,u=rq; p,v=rp
        # Produits restreints avant la construction des vecteurs complets.
        row_returns=A[:,jj]@q
        if row_returns.max()>u+tolerance: continue
        col_returns=p@B[ii,:]
        if col_returns.max()>v+tolerance: continue
        if not np.allclose(row_returns[ii],u,atol=tolerance,rtol=0): continue
        if not np.allclose(col_returns[jj],v,atol=tolerance,rtol=0): continue
        x=np.zeros(m); y=np.zeros(n); x[ii]=p; y[jj]=q
        eq=MixedNashEquilibrium(tuple(map(float,x)),tuple(map(float,y)),
            (float(p@A[ii[:,None],jj]@q),float(p@B[ii[:,None],jj]@q)),I,J)
        if not any(np.allclose(x,e.row_probabilities,atol=tolerance,rtol=0) and
                   np.allclose(y,e.column_probabilities,atol=tolerance,rtol=0) for e in found):
            found.append(eq)
    return found
