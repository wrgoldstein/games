from collections import Counter, defaultdict
from random import randint, sample
from copy import copy

def uniq(list_of_lists):
    out = []
    for L in list_of_lists:
        if L not in out:
            out.append(L)
    return out

def merge(base_score, kept, scores):
    res = []
    for score in scores:
        points, kept_, remaining = score
        res.append((base_score + points, kept + kept_, remaining))
    return res

def list_difference(list1, list2):
    list1c = copy(list1)
    for el in list2:
        list1c.remove(el)
    return list1c

def flatten(l):
    return [item for sublist in l for item in sublist]

class Farkle:
    """
    1: 100
    5: 50
    3 of 1: 300
    3 of 2: 200
    3 of 3: 300
    3 of 4: 400
    3 of 5: 500
    3 of 6: 600
    4 of anything: 1000
    3 pairs: 1000
    5 of anything: 2000
    6 of anything: 3000
    1-6 straight: 1500
    """

    @classmethod
    def six_of_anything(cls,rolled):
        if len(rolled) == 6 and len(set(rolled)) == 1:
            return 3000, rolled, []
    
    @classmethod
    def five_of_anything(cls, rolled):
        counter = Counter(rolled)
        values = counter.values()
        if len(values) and max(values) == 5:
            pip, _ = counter.most_common(1)[0]
            return 2000, [pip]*5, list_difference(rolled, [pip]*5)
    
    @classmethod
    def straight(cls, rolled):
        if len(rolled) == 6 and len(set(rolled)) == 6:
            return 1500, rolled, []

    @classmethod
    def three_pairs(cls, rolled):
        if list(Counter(rolled).values()) == [2,2,2]:
            return 1500, rolled, []
    
    @classmethod
    def four_of_anything(cls, rolled):
        counter = Counter(rolled)
        values = counter.values()
        if len(values) and max(values) == 4:
            pip, _ = counter.most_common(1)[0]
            return 1000, [pip]*4, list_difference(rolled, [pip]*4)
    
    @classmethod
    def three_of_anything(cls, rolled):
        if not len(rolled): return
        counter = Counter(rolled)
        values = counter.values()
        if max(values) < 3:
            return None
        if not len(counter.most_common(1)):
            import pdb; pdb.set_trace()
        pip, value = counter.most_common(1)[0]
        score = 300 if pip == 1 else pip*100
        return score, [pip]*3, list_difference(rolled, [pip]*3)
    
    @classmethod
    def two_ones(cls, rolled):
        if Counter(rolled)[1] >= 2:
            return 200, [1,1], list_difference(rolled, [1,1])

    @classmethod
    def one_ones(cls, rolled):
        if Counter(rolled)[1] >= 1:
            return 100, [1], list_difference(rolled, [1])

    @classmethod
    def two_fives(cls, rolled):
        if Counter(rolled)[5] >= 2:
            return 100, [5,5], list_difference(rolled, [5,5])

    @classmethod
    def one_fives(cls, rolled):
        if Counter(rolled)[5] >= 1:
            return 50, [5], list_difference(rolled, [5])

    @classmethod
    def score(cls, rolled, j=0):
        scores = []
        for i, m in list(enumerate([
            Farkle.six_of_anything,
            Farkle.five_of_anything,
            Farkle.straight,
            Farkle.three_pairs,
            Farkle.four_of_anything,
            Farkle.three_of_anything,
            Farkle.two_ones,
            Farkle.one_ones,
            Farkle.two_fives,
            Farkle.one_fives
        ]))[j:]:
            out = m.__call__(rolled)
            if out is None: continue
            scores.append(out)
            score, kept, remaining = out
            combinations = merge(score, kept, cls.score(remaining, i))
            scores += combinations
        return uniq(scores)
    


class Dice:
    @classmethod
    def roll(cls, n):
        return [randint(1,6) for _ in range(n)]


class Player:
    def strategy1(_, scores):
        # maximize points
        return sorted(scores, key=lambda score: score[0])[-1]

    def strategy2(total, scores):
        # maximize points divided by dice used
        greedy = Player.strategy1(total, scores)
        if sum(total) + greedy[0] >= 500:
            return greedy
        key = lambda score: score[0]/len(score[1])
        return sorted(scores, key=key)[-1]

    def strategy3(total, scores):
        # maximize points times dice remaining
        weight = {0: 1000, 1: -200, 2: -100, 3: 50, 4: 100, 5: 200}
        key = lambda score: score[0] + weight[len(score[2])]
        return sorted(scores, key=key)[-1]

    def reroll_if_4(x):
        return x >= 4

    def reroll_if_5(x):
        return x >= 5

    def __init__(self, strategy=None, reroll_strategy=None):
        self.aside = 0
        self.scores = defaultdict(list)
        self.round = 0
        self.strategy = getattr(Player, strategy) if type(strategy) == str else Player.strategy1
        self.reroll_strategy = getattr(Player, reroll_strategy) if type(reroll_strategy) == str else Player.reroll_if_5

    @classmethod
    def score_round(cls, round):
        if round[-1] == 'farkle':
            return 0
        else:
            return sum(round)

    def roll_verbose(self, total, ndice=6):
        if sum(total) >= 500:
            if not self.reroll_strategy(ndice):
                return total

        rolled = Dice.roll(ndice)
        print(rolled, end='\t')
        scores = Farkle.score(rolled)

        if not len(scores):
            total.append('farkle')
            return total

        score, kept, remaining = self.strategy(total, scores)
        print('>>', kept, ':', score)
        total.append(score)
        dice_left = 6 if not len(remaining) else len(remaining)
        return self.roll_verbose(total, dice_left)

    def roll(self, total, ndice=6):
        if sum(total) >= 500:
            if not self.reroll_strategy(ndice):
                return total

        rolled = Dice.roll(ndice)
        scores = Farkle.score(rolled)

        if not len(scores):
            total.append('farkle')
            return total

        score, kept, remaining = self.strategy(total, scores)
        total.append(score)
        dice_left = 6 if not len(remaining) else len(remaining)

        return self.roll(total, dice_left)

    def fixed_initial_roll(self, total, rolled):
        if sum(total) >= 500:
            if not self.reroll_strategy(ndice):
                return total

        scores = Farkle.score(rolled)

        if not len(scores):
            total.append('farkle')
            return total

        score, kept, remaining = self.strategy(total, scores)
        total.append(score)
        dice_left = 6 if not len(remaining) else len(remaining)

        return self.roll(total, dice_left)