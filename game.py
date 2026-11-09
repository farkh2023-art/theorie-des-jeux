class StageGame:
    def __init__(self,payoffs): self.payoffs=payoffs
    def payoff(self,a,b): return self.payoffs[(a,b)]
