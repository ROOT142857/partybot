import random
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Hand:
    def __init__(self, cards):
        self.cards = cards
        assert len(cards) == 5
    
    def __str__(self):
        return '(문양(0~3),숫자(1~13)):({},{}),({},{}),({},{}),({},{}),({},{})'.format(self.cards[0].suit,self.cards[0].rank,self.cards[1].suit,self.cards[1].rank,self.cards[2].suit,self.cards[2].rank,self.cards[3].suit,self.cards[3].rank,self.cards[4].suit,self.cards[4].rank)

    def getNumCardsByRank(self):
        numCardsByRank = [0]*13
        for i in range(len(self.cards)):
            j = self.cards[i].rank
            assert 1 <= j <= 13
            numCardsByRank[j-1] += 1
        return numCardsByRank

    def getNumCardsBySuit(self):
        numCardsBySuit = [0]*4
        # ADD ADDITIONAL CODE HERE!!
        for i in range(len(self.cards)):
            j = self.cards[i].suit
            assert 0 <= j <= 3
            numCardsBySuit[j] += 1 
        return numCardsBySuit
        
##############################################################
        
# use this function for atLeastStraight()
def hasConsecutivePositive(L, k):
    n = len(L)
    assert k <= n
    counter = 0
    for i in range(n+1):  # +1: account for wrapping
        if L[i%n] >= 1:
            counter += 1
            if counter == k:
                return True
        else:
            counter = 0  # reset
    return False

    
def atLeastStraight(hand):
    L = hand.getNumCardsByRank()
    # ADD ADDITIONAL CODE HERE!!
    return hasConsecutivePositive(L,5)
    
# for some pattern
def atLeastFlush(hand):
    L = hand.getNumCardsBySuit()
    # ADD ADDITIONAL CODE HERE!!
    for i in range(len(L)):
        if L[i] == 5:
            return True
    return False

    
def straightFlush(hand):
    # ADD ADDITIONAL CODE HERE!!
    if atLeastFlush(hand) and atLeastStraight(hand):
        return True
    return False  # remove it after completing your code


def flush(hand):
    # ADD ADDITIONAL CODE HERE!!
    if atLeastFlush(hand) and not atLeastStraight(hand):
        return True
    return False  # remove it after completing your code


def straight(hand):
    # ADD ADDITIONAL CODE HERE!!
    if atLeastStraight(hand) and not atLeastFlush(hand):
        return True
    return False  # remove it after completing your code


##############################################################
    
# for some pattern
def hasMultipleCardsWithSameRank(hand, num):
    L = hand.getNumCardsByRank()
    cnt = 0
    # ADD ADDITIONAL CODE HERE!!
    for i in range(len(L)):
        if L[i] == num:
            cnt += 1
    return cnt  # remove it after completing your code
    
def quadruple(hand):
    return hasMultipleCardsWithSameRank(hand, 4)

def fullHouse(hand):
    if hasMultipleCardsWithSameRank(hand,2) and hasMultipleCardsWithSameRank(hand,3):
        return True
    return False  # remove it after completing your code
    
def triple(hand):
    # ADD ADDITIONAL CODE HERE!!
    if hasMultipleCardsWithSameRank(hand,3) and not hasMultipleCardsWithSameRank(hand,2):
        return True
    return False  # remove it after completing your code


# counter pattern
def twoPair(hand):
    # ADD ADDITIONAL CODE HERE!!
    if hasMultipleCardsWithSameRank(hand,2) == 2:
        return True
    return False  # remove it after completing your code


def pair(hand):
    # ADD ADDITIONAL CODE HERE!!
    if hasMultipleCardsWithSameRank(hand,2) == 1  and not hasMultipleCardsWithSameRank(hand,3):
        return True
    return False  # remove it after completing your code

def randomHand(numCards):
    cards = []
    for suit in range(4):
        for rank in range(1,13+1):
            cards.append(Card(suit, rank))
    random.shuffle(cards)
    return Hand(cards[:numCards])

def countPokerHands(hands):
    nStraightFlush = 0
    nQuadruple = 0
    nFullHouse = 0
    nFlush = 0
    nStraight = 0
    nTriple = 0
    nTwoPair = 0
    nPair = 0

    for i in range(len(hands)):
        hand = hands[i]
        # ADD ADDITIONAL CODE HERE!!
        if straightFlush(hand):
            nStraightFlush += 1
        if straight(hand):
            nStraight += 1
        if flush(hand):
            nFlush += 1
        if fullHouse(hand):
            nFullHouse += 1
        if quadruple(hand):
            nQuadruple += 1
        if triple(hand):
            nTriple += 1
        if twoPair(hand):
            nTwoPair += 1
        if pair(hand):
            nPair += 1

    return [nPair, nTwoPair, nTriple, nStraight, nFlush, nFullHouse, nQuadruple, nStraightFlush]

##############################################################
# club:0  dia:1  heart:2  spade:3
# Jack:11  Queen:12  King:13
def test():
    hands = [
        Hand([Card(2,12), Card(2,10), Card(2,11), Card(2,1), Card(2,13)]),  # s.f.
        Hand([Card(1,7), Card(1,11), Card(1,6), Card(1,2), Card(1,4)]), # flush
        Hand([Card(0,7), Card(1,6), Card(2,8), Card(0,5), Card(2,9)]),  # straight
        Hand([Card(2,2), Card(3,2), Card(0,5), Card(0,2), Card(1,2)]),  # quadruple
        Hand([Card(1,5), Card(1,2), Card(0,5), Card(2,5), Card(0,2)]),  # full house
        Hand([Card(2,4), Card(1,2), Card(0,5), Card(2,2), Card(0,2)]),  # triple
        Hand([Card(1,2), Card(2,5), Card(0,2), Card(1,5), Card(3,10)]), # two pair
        Hand([Card(1,7), Card(3,2), Card(0,5), Card(0,1), Card(2,2)])  # pair
    ]

    f = [straightFlush, flush, straight, quadruple, fullHouse, triple, twoPair, pair]

    for i in range(len(f)):
        for j in range(len(hands)):
            if (i==j and f[i](hands[j])!=True) or (i!=j and f[i](hands[j])!=False):
            # if (i==j and not f[i](hands[j])) or (i!=j and f[i](hands[j])):
                print("Error:", f[i].__name__+"()", "is not correct for hands["+str(j)+"]")
                break
    print("Your code is correct if no error message appears")

    
if __name__ == '__main__': test()
