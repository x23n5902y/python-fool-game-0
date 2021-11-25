# Игра в дурака.
# Игра идет до тех пор, пока в колоде не осталось карт и у всех игроков,
# кроме одного, не осталось карт в руке.
# Author: Aleksandr Maslennikov, Senior Durak Developer.
import random

class MyMethods:
    def __str__(self):
        return f'deck[{len(self.cards)}]: {", ".join([str(card) for card in self.cards])}'

    def __iter__(self):
        self.a = 0
        return iter(self.cards)

    def __next__(self):
        if self.a <= len(self.cards) -1:
            x = self.a
            self.a += 1
            return self.cards[x]
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __contains__(self, other_card):
        return other_card in self.cards
class Card:
    DIAMONDS = '\u2666'  # Буби
    CLUBS = '\u2663'  # Крести
    HEARTS = '\u2665'  # Черви
    SPADES = '\u2660'  # Пики

    VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    # VALUES = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, value, suit):
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = suit
        self.index = Card.VALUES.index(str(value))
        self.trump = False

    def __str__(self):
        return f"{self.value}{self.suit}"

    def to_str(self):
        return f"{self.value}{self.suit}"

    # Перегружаем метод таким образом, чтобы функция min
    # могла выбрать наименьшую некозырную карту из руки игрока
    def __lt__(self, other):
        if self.trump and other.trump:
            return self.index < other.index
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True
        if self.index == other.index:
            return False if random.randint(0, 1) in list(range(2)) else True
        else:
            return self.index < other.index

    def less(self, other):
        if self.suit == other.suit:
            return self.index < other.index
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True

    def __gt__(self, other):
        return not self.index < other.index

    def equal_suit(self, other):
        return self.suit == other.suit


class Deck(MyMethods):
    def __init__(self):
        self.cards = []
        for key in [Card.HEARTS, Card.DIAMONDS, Card.CLUBS, Card.SPADES]:
            for value in Card.VALUES:
                self.cards.append(Card(value, key))

    def shuffle(self):
        # Перемешать колоду
        random.shuffle(self.cards)
        # снять произвольное число кард сверху колоды и положить их в конец
        random_half_deck = random.randint(0, 51)
        self.cards = \
            self.cards[random_half_deck:] + \
            self.cards[:random_half_deck]

    def show(self):
        return f'deck[{len(self.cards)}]: ' \
               f'{", ".join([card.to_str() for card in self.cards])}'

    def draw(self, cards):
        taken_cards = self.cards[:cards]
        self.cards = self.cards[cards:]
        return taken_cards

    def pick(self):
        return self.cards.pop(0)

    def __sub__(self):
        pass


class Player:
    NAMES = [{'name': 'Терентий', 'sex': 'M'},
             {'name': 'Феофан', 'sex': 'M'},
             {'name': 'Сидор', 'sex': 'M'},
             {'name': 'Игнатий', 'sex': 'M'},
             {'name': 'Харитон', 'sex': 'M'},
             {'name': 'Аристарх', 'sex': 'M'},
             {'name': 'Пахом', 'sex': 'M'}]
    def __init__(self, name, sex, p_type):
        self.name = name
        self.sex = sex
        self.hand = []
        self.fought_back = False
        self.last_player = False
        self.title = ('Дурак' if self.sex == 'M' else 'женщина-Дурак')
        self.p_type = p_type
        self.round_index = None

    def show_hand(self):
        return f'{self.name}[{len(self.hand)}] : ' \
               f'{", ".join([card.to_str() for card in self.hand])}'

    def pick_card(self, card):
        self.hand.append(card)

    def choose_card(self):
        return self.hand.pop(self.hand.index(min([card for card in self.hand])))

    def defend(self, table):
        current_table = table
        # Долдны отбить последнюю карту на столе
        other_card = current_table[-1]
        # Смотрим, есть лит у нас карта такой же масти с бОльшим значением
        # defense_card = [card for card in self.hand if card.suit == other_card.suit and card.index > other_card.index]
        defense_card = [card for card in self.hand if other_card.less(card)]
        # Если есть, то отбиваемся
        if len(defense_card) > 0:
            return self.hand.pop(self.hand.index(min(defense_card)))
        # Если нет, то забираем стол в руку
        else:
            self.hand += current_table
            return False

    def attack(self, table):
        # Первая атака в начале хода
        current_table = table
        if len(current_table) == 0:
            return self.hand.pop(self.hand.index(min([card for card in self.hand])))
        # Смотрим стол и подкидываем
        if len(current_table) > 0:
            next_card = False
            # Смотрим есть ли карта с таким же значением в руке
            for card_on_table in current_table:
                for my_card in self.hand:
                    if card_on_table.value == my_card.value:
                        next_card = my_card
                        break
            # Если карта найдена, то кладем ее на стол
            if next_card:
                return self.hand.pop(self.hand.index(next_card))
            else:
                return False


class FoolGame:
    DIFFICULTY = [
        'I\'m too young to die',
        'Hey, not too rough',
        'Hurt me plenty',
        'Ultra-Violence',
        'Nightmare']

    def __init__(self, difficulty, n_players):
        # Начинаем игру
        # Перемешиваем список игроков
        random.shuffle(Player.NAMES)
        # Получаем уровень сложности
        self.difficulty = difficulty
        self.difficulty_level = FoolGame.DIFFICULTY[difficulty]
        # Создаем указанное количество игроков
        self.n_players = n_players
        self.players = [
            Player(Player.NAMES[player]['name'],
                   Player.NAMES[player]['sex'], 'AI')
            for player in range(self.n_players)]
        self.deck = None
        self.trump_suit = None
        self.table = []
        self.round_number = 1

    def show_table(self):
        return f'table[{len(self.table)}]: ' \
               f'{", ".join([card.to_str() for card in self.table])}'

    def start(self):
        # Карты раздаем по одной, пока у каждого игрока в руке не будет 6 карт.
        # Зная количество игроков вычисляем индекс карты, которая определит
        # корзырную масть.
        # Перемещаем эту карту в конец колоды и для карт этой масти
        # выставляем значение trump = True
        # Если после раздачи у одного из игроков в руке оказалось 5 и более карт одной масти
        # то он имеет право инициировать пересдачу. Зависит от выбранного уровня сложности

        def preflight():
            # Создаем колоду
            self.deck = Deck()
            self.deck.shuffle()
            # Определяем козырную масть
            self.trump_index = 6 * self.n_players
            self.trump_suit = self.deck.cards[self.trump_index].suit
            cards = len(self.deck.cards[self.trump_index:])
            # Проставляем trump = True для козырных карт
            for card in self.deck.cards:
                if card.suit == self.deck.cards[self.trump_index].suit:
                    card.trump = True
            # Перемещаем карту, определяющую козырную масть в конец колоды.
            self.deck.cards.append(self.deck.cards.pop(self.trump_index))

            # Раздаем карты
            while len(self.deck.cards) > cards:
                for player in self.players:
                    player.hand.append(self.deck.pick())

        def retake_of_cards():
            for player in self.players:
                hand_diamonds = len([diamond for diamond in player.hand if diamond.suit == '\u2666'])
                hand_clubs = len([club for club in player.hand if club.suit == '\u2663'])
                hand_hearts = len([heart for heart in player.hand if heart.suit == '\u2665'])
                hand_spades = len([spade for spade in player.hand if spade.suit == '\u2660'])
                print(
                    f'{player.name}: '
                    f'diamonds={hand_diamonds}, '
                    f'clubs={hand_clubs}, '
                    f'hearts={hand_hearts}, '
                    f'spades={hand_spades}')
                if hand_diamonds >= 5 or \
                        hand_clubs >= 5 or \
                        hand_hearts >= 5 or \
                        hand_spades >= 5:
                    if random.randint(0, 2) in list(range(2)):
                        print(f'{player.name}: Прошу пересдать!')
                        # Все игроки сбрасывают карты
                        for player_ in self.players:
                            player_.hand.clear()
                        # Раздаем снова
                        return True

        def elect_first():
            min_trump = None
            print(f'Козырь: {self.trump_suit}')
            trumps_list = []
            for index, player in enumerate(self.players):
                for card in player.hand:
                    if card.trump:
                        trumps_list.append({'card': card.index, 'player': index})

            if len(trumps_list) > 0:
                min_trump_id, first_player = (min(trumps_list, key=lambda x: x['card'])).values()
                for card in self.players[first_player].hand:
                    if card.index == min_trump_id and card.suit == self.trump_suit:
                        min_trump = card

                print(f'Первым ходит игрок {self.players[first_player].name}, '
                      f'у него {min_trump}')
                return self.players[first_player]
            else:
                random_player_id = random.randint(0, self.n_players - 1)
                print(f'Козырей не пришло\n'
                      f'Первым ходит игрок {self.players[random_player_id].name}')
                return self.players[random_player_id]

        def elect_second(player):
            if self.players.index(player) == (len(self.players) - 1):
                next_player = 0
            else:
                next_player = self.players.index(player) + 1
            return self.players[next_player]

        def elect_next_pair():
            if self.round_number == 1:
                f_player_ = elect_first()
                return f_player_, elect_second(f_player_)
            if self.round_number > 1:
                for player in self.players:
                    if player.fought_back:
                        return player, elect_second(player)
                for player in self.players:
                    if player.last_player:
                        if self.players.index(player) == (len(self.players) - 1):
                            next_player = elect_second(player)
                        else:
                            next_player = elect_second(elect_second(player))
                        return next_player, elect_second(next_player)

        def fight(c_player, n_player):
            print('\n'+c_player.show_hand())
            print(n_player.show_hand(), '\n')
            test_card = c_player.attack(self.table)
            if test_card:
                print(f'{c_player.name} кладет: {test_card}')
                self.table.append(test_card)
            else:
                print(f'{c_player.name}: Бито!')
                n_player.fought_back = True
                return False
            def_card = n_player.defend(self.table)
            if def_card:
                print(f'{n_player.name} бьет: {def_card}')
                self.table.append(def_card)
                print(self.show_table())
                return True
            else:
                print(f'{n_player.name}: Беру!\n')
                print(c_player.show_hand())
                print(n_player.show_hand())
                n_player.fought_back = False
                c_player.last_player = True
                return False

        def tossing(c_player, n_player):
            if n_player.fought_back and len(n_player.hand) > 0:
                for player in self.players:
                    if player != n_player and player != c_player:
                        while True:
                            if self.round_number == 1 and len(self.table) > 9:
                                print(f'SYSTEM: Конец первого раунда, 10 карт на столе.')
                                n_player.fought_back = True
                                break
                            if self.round_number > 1 and len(self.table) > 11:
                                print(f'SYSTEM: Конец {self.round_number}-го раунда, 12 карт на столе.')
                                n_player.fought_back = True
                                break
                            if not fight(player, n_player):
                                break
            self.table.clear()

        def draw_cards():
            for player in self.players:
                while len(player.hand) < 6:
                    if len(self.deck.cards) == 0:
                        break
                    print(f'{player.name}: Беру карту с колоды')
                    player.pick_card(self.deck.pick())
            # print(player.show_hand())

        def remove_player():
            for player in self.players:
                if len(player.hand) == 0:
                    if player.fought_back:
                        elect_second(player).fought_back = True
                        self.players.remove(player)
                        print(f'Игрок {player.name} закончил на {self.round_number -1}-м раунде')
            for player in self.players:
                if len(player.hand) == 0:
                    if player.last_player:
                        if self.players.index(player) == (len(self.players) - 1):
                            elect_second(player).last_player = True
                        else:
                            elect_second(elect_second(player)).last_player = True
                    print(f'Игрок {player.name} закончил на {self.round_number-1}-м раунде')
                    self.players.remove(player)

        # Создаем колоду, перемешиваем и раздаем карты игрокам
        preflight()
        # Если уровень сложности выше I\'m too young to die
        # То игрок имеет право попросить пересдачу, если у него в руке 5 и более карт
        # одной масти
        if self.difficulty > 0:
            print(self.difficulty)
            while retake_of_cards():
                preflight()

        def match(f_player__, s_player__):
            print(f'\nИграем {self.round_number}-й раунд')
            # Определяем, кто ходит первым под игрока со следующим номером
            first_player = f_player__
            next_player = s_player__
            first_player.fought_back = False
            next_player.fought_back = False
            first_player.last_player = False
            next_player.last_player = False

            print(f'Игроки: {first_player.name} VS {next_player.name}')
            # print(f'Игрок: {next_player.name}')
            print(f'Козырь: {self.trump_suit}')
            print(f'Осталось игроков: {len(self.players)}')
            print(f'Осталось карт в колоде: {len(self.deck.cards)}')
            while True:
                if not fight(first_player, next_player):
                    break
            tossing(first_player, next_player)
            self.round_number += 1

        while True:
            f_player, s_player = None, None
            remove_player()
            if len(self.players) == 1:
                print(f'Игрок {self.players[0].name} - дурак')
                break
            else:
                try:
                    f_player, s_player = elect_next_pair()
                except TypeError as error:
                    print(f'Игроки {f_player.name} и {s_player.name} дураки, потому что'
                          f'не смогли нормально сыграть и поймали {error}.'
                          f'У них ничья')
                    break

            match(f_player, s_player)
            draw_cards()


while True:
    try:
        players = int(input('Введите количество игроков от 2-х до 7-ми:'))
        if players in range(2, 8):
            break
        else:
            raise ValueError('Количество игроков должно быть от 2-х до 7-ми')

    except (ValueError, TypeError) as e:
        print(e)

game = FoolGame(1, players)
game.start()
