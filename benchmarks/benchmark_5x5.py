import json,random,statistics,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nash_solver import find_mixed_nash,_support_pairs

def game(seed):
 r=random.Random(seed);return ([[r.randint(-20,20) for _ in range(5)] for _ in range(5)],[[r.randint(-20,20) for _ in range(5)] for _ in range(5)])
def main(repeats=10):
 _support_pairs(5,5) # prechauffage du cache hors mesure
 times=[]; counts=[]
 for seed in range(repeats):
  A,B=game(5000+seed); t=time.perf_counter(); E=find_mixed_nash(A,B); times.append(time.perf_counter()-t);counts.append(len(E))
 report={'dimensions':[5,5],'repetitions':repeats,'supports_mixtes_examined':226,'min_s':min(times),'mediane_s':statistics.median(times),'moyenne_s':statistics.mean(times),'max_s':max(times),'equilibres_moyens':statistics.mean(counts)}
 Path('benchmark-5x5.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 10)
