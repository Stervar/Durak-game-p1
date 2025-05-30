import random




# масти
SPADES = '♠'
HEARTS = '♥'
DIAMS = '♦'
CLUBS = '♣'



# достоинтсва карт
NOMINALS = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# поиск индекса по достоинству
NAME_TO_VALUE = {n: i for i, n in enumerate(NOMINALS)}

# карт в руке при раздаче
CARDS_IN_HAND_MAX = 6
N_PLAYERS = 2

# эталонная колода (каждая масть по каждому номиналу) - 36 карт
DECK = [(nom, suit) for nom in NOMINALS for suit in [SPADES, HEARTS, DIAMS, CLUBS]]

class Player:
    def __init__(self, index, cards):
        self.index = index
        self.cards = list(map(tuple, cards))  # убедимся, что будет список кортежей

    def take_cards_from_deck(self, deck: list):
        """
        Взять недостающее количество карт из колоды
        Колода уменьшится
        :param deck: список карт колоды 
        """
        lack = max(0, CARDS_IN_HAND_MAX - len(self.cards))
        n = min(len(deck), lack)
        self.add_cards(deck[:n])
        del deck[:n]
        return self

    def sort_hand(self):
        """
        Сортирует карты по достоинству и масти
        """
        self.cards.sort(key=lambda c: (NAME_TO_VALUE[c[0]], c[1]))
        return self

    def add_cards(self, cards):
        self.cards += list(cards)
        self.sort_hand()
        return self

    # всякие вспомогательные функции:
    
    def __repr__(self):
        return f"Player{self.cards!r}"

    def take_card(self, card):
        self.cards.remove(card)

    @property
    def n_cards(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]
    
    
class Durak:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()  # генератор случайных чисел

        self.deck = list(DECK)  # копируем колоду
        self.rng.shuffle(self.deck)  # мешаем карты в копии колоды

        # создаем игроков и раздаем им по 6 карт из перемешанной колоды
        self.players = [Player(i, []).take_cards_from_deck(self.deck)
                        for i in range(N_PLAYERS)]

        # козырь - карта сверху
        self.trump = self.deck[0][1]
        # кладем козырь под низ вращая список по кругу на 1 назад
        self.deck = rotate(self.deck, -1)

        # игровое поле: ключ - атакующая карта, значения - защищающаяся или None
        self.field = {}  

        self.attacker_index = 0  # индекс атакующего игрока
        self.winner = None  # индекс победителя