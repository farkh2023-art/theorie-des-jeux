def grim_trigger(history): return 'T' if any(x!=('C','C') for x in history) else 'C'
def tit_for_tat(history): return 'C' if not history else history[-1][1]
