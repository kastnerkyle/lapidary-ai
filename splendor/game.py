import random
from itertools import permutations
import numpy as np

from data import colours

# Splendor colour order:
# - White
# - Blue
# - Green
# - Red
# - Black

class Card(object):
    def __init__(
            self, tier, colour, points, white=0, blue=0,
            green=0, red=0, black=0):
        self.colour = colour
        self.points = points
        self.tier = tier

        
        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    @property
    def requirements(self):
        return (self.white, self.blue, self.green, self.red, self.black)

    def num_required(self, colour):
        return getattr(self, colour)

    def __str__(self):
        return '<Card T={} P={} {}>'.format(
            self.tier, self.points, ','.join(
                ['{}:{}'.format(colour, self.num_required(colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if self.num_required(colour)]))

    def __repr__(self):
        return str(self)
                 
class Noble(object):
    def __init__(self, points=3, white=0, blue=0, green=0, red=0, black=0):
        self.points = points

        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    def num_required(self, colour):
        return getattr(self, colour)

    def __str__(self):
        return '<Noble P={} {}>'.format(
            self.points, ','.join(
                ['{}:{}'.format(colour, self.num_gems(colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if self.num_gems(colour)]))

    def __repr__(self):
        return str(self)

tier_1 = [
    Card(1, 'blue', 0, black=3),
    Card(1, 'blue', 0, white=1, black=2),
    Card(1, 'blue', 0, green=2, black=2),
    Card(1, 'blue', 0, white=1, green=2, red=2),
    Card(1, 'blue', 0, blue=1, green=3, red=1),
    Card(1, 'blue', 0, white=1, green=1, red=1, black=1),
    Card(1, 'blue', 0, white=1, green=1, red=2, black=1),
    Card(1, 'blue', 1, red=4),

    Card(1, 'red', 0, white=3),
    Card(1, 'red', 0, blue=2, green=1),
    Card(1, 'red', 0, white=2, red=2),
    Card(1, 'red', 0, white=2, green=1, black=2),
    Card(1, 'red', 0, white=1, red=1, black=3),
    Card(1, 'red', 0, white=1, blue=1, green=1, black=1),
    Card(1, 'red', 0, white=2, blue=1, green=1, black=1),
    Card(1, 'red', 1, white=4),

    Card(1, 'black', 0, green=3),
    Card(1, 'black', 0, green=2, red=1),
    Card(1, 'black', 0, white=2, green=2),
    Card(1, 'black', 0, white=2, blue=2, red=1),
    Card(1, 'black', 0, green=1, red=3, black=1),
    Card(1, 'black', 0, white=1, blue=1, green=1, red=1),
    Card(1, 'black', 0, white=1, blue=2, green=1, red=1),
    Card(1, 'black', 1, blue=4),

    Card(1, 'white', 0, blue=3),
    Card(1, 'white', 0, red=2, black=1),
    Card(1, 'white', 0, blue=2, black=2),
    Card(1, 'white', 0, blue=2, green=2, black=1),
    Card(1, 'white', 0, white=3, blue=1, black=1),
    Card(1, 'white', 0, blue=1, green=1, red=1, black=1),
    Card(1, 'white', 0, blue=1, green=2, red=1, black=1),
    Card(1, 'white', 1, green=4),

    Card(1, 'green', 0, red=3),
    Card(1, 'green', 0, white=2, blue=1),
    Card(1, 'green', 0, blue=2, red=2),
    Card(1, 'green', 0, blue=1, red=2, black=2),
    Card(1, 'green', 0, white=1, blue=3, green=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=2),
    Card(1, 'green', 1, black=4)
    ]

tier_2 = [
    Card(2, 'blue', 1, blue=2, green=2, red=3),
    Card(2, 'blue', 1, blue=2, green=3, black=3),
    Card(2, 'blue', 2, blue=5),
    Card(2, 'blue', 2, white=5, blue=3),
    Card(2, 'blue', 2, white=2, red=1, black=4),
    Card(2, 'blue', 3, blue=6),

    Card(2, 'red', 1, white=2, red=2, black=3),
    Card(2, 'red', 1, blue=3, red=2, black=3),
    Card(2, 'red', 2, black=5),
    Card(2, 'red', 2, white=3, black=5),
    Card(2, 'red', 2, white=1, blue=4, green=2),
    Card(2, 'red', 3, red=6),

    Card(2, 'black', 1, white=3, blue=2, green=2),
    Card(2, 'black', 1, white=3, green=3, black=2),
    Card(2, 'black', 2, white=5),
    Card(2, 'black', 2, green=5, red=3),
    Card(2, 'black', 2, blue=1, green=4, red=2),
    Card(2, 'black', 3, black=6),

    Card(2, 'white', 1, green=3, red=2, black=2),
    Card(2, 'white', 1, white=2, blue=3, red=3),
    Card(2, 'white', 2, red=5),
    Card(2, 'white', 2, red=5, black=3),
    Card(2, 'white', 2, green=1, red=4, black=2),
    Card(2, 'white', 3, white=6),

    Card(2, 'green', 1, white=2, blue=3, black=2),
    Card(2, 'green', 1, white=3, green=2, red=3),
    Card(2, 'green', 2, green=5),
    Card(2, 'green', 2, blue=5, green=3),
    Card(2, 'green', 2, white=4, blue=2, black=1),
    Card(2, 'green', 3, green=6)
    ]

tier_3 = [
    Card(3, 'blue', 3, white=3, green=3, red=3, black=5),
    Card(3, 'blue', 4, white=7),
    Card(3, 'blue', 4, white=6, blue=3, black=3),
    Card(3, 'blue', 5, white=7, blue=3),

    Card(3, 'red', 3, white=3, blue=5, green=3, black=5),
    Card(3, 'red', 4, green=7),
    Card(3, 'red', 4, blue=3, green=6, red=3),
    Card(3, 'red', 5, green=7, red=3),

    Card(3, 'black', 3, white=3, blue=3, green=5, red=3),
    Card(3, 'black', 4, red=7),
    Card(3, 'black', 4, green=3, red=6, black=3),
    Card(3, 'black', 5, red=7, black=3),

    Card(3, 'white', 3, blue=3, green=3, red=5, black=3),
    Card(3, 'white', 4, black=7),
    Card(3, 'white', 4, white=3, red=3, black=6),
    Card(3, 'white', 5, white=3, black=7),

    Card(3, 'green', 3, white=5, blue=3, red=3, black=3),
    Card(3, 'green', 4, blue=7),
    Card(3, 'green', 4, white=3, blue=6, green=3),
    Card(3, 'green', 5, blue=7, green=3)
    ]

triples = {('black', 'blue', 'white'),
           ('black', 'green', 'blue'),
           ('black', 'green', 'white'),
           ('black', 'red', 'blue'),
           ('black', 'red', 'green'),
           ('black', 'red', 'white'),
           ('green', 'blue', 'white'),
           ('red', 'blue', 'white'),
           ('red', 'green', 'blue'),
           ('red', 'green', 'white')}
pairs = [('black', 'red'),
         ('black', 'blue'),
         ('black', 'white'),
         ('black', 'green'),
         ('red', 'blue'),
         ('red', 'white'),
         ('red', 'green'),
         ('blue', 'white'),
         ('blue', 'green'),
         ('green', 'white')]
# tier_1 = [Card(1, 'blue', 0, **{c: 1 for c in triple}) for triple in triples]
# tier_1 = [Card(1, 'blue', 0, **{c1: 2, c2: 1}) for c1, c2 in pairs]
# tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(5)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(5)]
tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(5)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(5)]
tier_2 = []
tier_3 = []
all_cards = tier_1 + tier_2 + tier_3
# tier_1 = set(tier_1)
# tier_2 = set(tier_2)
# tier_3 = set(tier_3)


nobles = [
    Noble(red=4, green=4),
    Noble(black=4, red=4),
    Noble(blue=4, green=4),
    Noble(black=4, white=4),
    Noble(blue=4, white=4),
    Noble(black=3, red=3, white=3),
    Noble(green=3, blue=3, white=3),
    Noble(black=3, red=3, green=3),
    Noble(green=3, blue=3, red=3),
    Noble(black=3, blue=3, white=3)
    ]

class Player(object):
    def __init__(self):
        self.cards_in_hand = []
        self.cards_played = []
        self.nobles = []

        self._gold = 0
        self._white = 0
        self._blue = 0
        self._green = 0
        self._red = 0
        self._black = 0

    def copy(self):
        copy = Player()
        for colour in colours + ['gold']:
            copy.set_gems(colour, self.num_gems(colour))
        copy.nobles = self.nobles[:]
        copy.cards_in_hand = self.cards_in_hand[:]
        copy.cards_played = self.cards_played[:]
        return copy

    def num_gems(self, colour):
        return getattr(self, '_' + colour)

    def set_gems(self, colour, number):
        setattr(self, '_' + colour, number)

    @property
    def total_num_gems(self):
        return (self._gold + self._white + self._blue + self._green +
                self._red + self._black)

    @property
    def gems(self):
        return {'white': self._white,
                'blue': self._blue,
                'green': self._green,
                'red': self._red,
                'black': self._black,
                'gold': self._gold}

    # def gems_list(self):
    #     return (['white' for _ in range(self.white)] + 
    #             ['blue' for _ in range(self.blue)] +
    #             ['green' for _ in range(self.green)] +
    #             ['red' for _ in range(self.red)] +
    #             ['black' for _ in range(self.black)] +
    #             ['gold' for _ in range(self.gold)])

    def add_gems(self, **kwargs):
        for colour, change in kwargs.items():
            assert colour in colours or colour == 'gold'
            self.set_gems(colour, self.num_gems(colour) + change)


    @property
    def num_reserved(self):
        return len(self.cards_in_hand)

    @property
    def score(self):
        score = 0
        for card in self.cards_played:
            score += card.points

        for noble in self.nobles:
            score += noble.points
        return score

    def num_cards_of_colour(self, colour):
        number = 0
        for card in self.cards_played:
            if card.colour == colour:
                number += 1
        return number

    def can_afford(self, card):
        missing_colours = [max(card.num_required(colour) -
                               self.num_gems(colour) -
                               self.num_cards_of_colour(colour), 0)
                           for colour in colours]

        if sum(missing_colours) > self.num_gems('gold'):
            return False, None

        cost = {colour: max(min(self.num_gems(colour),
                                card.num_required(colour) -
                                self.num_cards_of_colour(colour)), 0) for colour in colours}
        cost['gold'] = sum(missing_colours)

        # TODO: Allow gold to be used instead of coloured gems, if available

        return True, cost

    def verify_state(self):
        assert 0 <= self.total_num_gems <= 10
        assert len(self.cards_in_hand) <= 3
        assert len(set(self.nobles)) == len(self.nobles)

        for colour in colours + ['gold']:
            assert self.num_gems(colour) >= 0


class StateVector(object):
    def __init__(self, num_players, vector=None):
        super(StateVector, self).__init__()

        self.num_players = num_players

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[num_players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[num_players]

        if vector is None:
            self.init_vector()
        else:
            self.vector = vector

    def copy(self):
        vector = StateVector(num_players=self.num_players,
                             vector=self.vector.copy())
        vector.card_indices = self.card_indices
        vector.supply_gem_indices = self.supply_gem_indices
        vector.player_gem_indices = self.player_gem_indices
        vector.player_played_colours_indices = self.player_played_colours_indices
        vector.player_score_indices = self.player_score_indices
        vector.noble_indices = self.noble_indices

        return vector

    def init_vector(self):
        
        num_players = self.num_players
        num_cards = len(all_cards)

        # store card locations
        cur_index = 0
        card_locations = [0 for _ in range(num_cards * (2 + num_players))]
        self.card_indices = {card: i * (2 + num_players) for i, card in enumerate(all_cards)}

        cur_index += len(card_locations)

        # store numbers of gems in the supply
        num_colour_gems_in_play = self.num_gems_in_play
        gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
        self.supply_gem_indices = {colour: cur_index + i * (num_colour_gems_in_play + 1)
                                   for i, colour in enumerate(colours)}

        cur_index += len(gem_nums_in_supply)

        # ...plus gold
        gold_nums_in_supply = [0 for _ in range(6)]
        self.supply_gem_indices['gold'] = cur_index

        cur_index += len(gold_nums_in_supply)

        # store numbers of gems held by each player
        all_player_gems = []
        player_gem_indices = {}
        for player_index in range(num_players):
            player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
            all_player_gems.extend(player_gems)
            player_gem_indices.update({(player_index, colour): cur_index + i * (num_colour_gems_in_play + 1)
                                       for i, colour in enumerate(colours)})
            cur_index += len(player_gems)

            all_player_gems.extend([0 for _ in range(6)])
            player_gem_indices[(player_index, 'gold')] = cur_index
            cur_index += 6
        self.player_gem_indices = player_gem_indices

        # store numbers of coloured cards played by each player
        # only count up to 7 - more than this makes no difference
        all_player_cards = []
        player_played_colours_indices = {}
        for player_index in range(num_players):
            player_cards = [0 for _ in range(5 * 8)]
            all_player_cards.extend(player_cards)

            player_played_colours_indices.update({(player_index, colour): cur_index + i * 8
                                                  for i, colour in enumerate(colours)})
            cur_index += len(player_cards)
        self.player_played_colours_indices = player_played_colours_indices
            
        # cur_index += len(all_player_cards)

        # store number of points of each player
        # only count up to 20, higher scores are very unlikely
        player_scores = [0 for _ in range(21 * num_players)]
        self.player_score_indices = {player_index: cur_index + player_index * 21
                                     for player_index in range(num_players)}

        cur_index  += len(player_scores)

        # store number of nobles in the game, and available
        nobles_available = [0 for _ in range(len(nobles))]  # locations 
        self.noble_indices = {noble: cur_index + i for i, noble in enumerate(nobles)}

        self.vector = np.array(card_locations + gem_nums_in_supply + gold_nums_in_supply +
                               all_player_gems + all_player_cards + player_scores +
                               nobles_available)

    def verify_state(self):
        for colour in colours:
            index = self.supply_gem_indices[colour]
            assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
        gold_index = self.supply_gem_indices['gold']
        assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

        for player_index in range(self.num_players):
            for colour in colours:
                index = self.player_gem_indices[(player_index, colour)]
                assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
            gold_index = self.player_gem_indices[(player_index, 'gold')]
            assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

            score_index = self.player_score_indices[player_index]
            assert np.sum(self.vector[score_index:score_index + 21]) == 1
            
    def num_supply_gems(self, colour):
        index = self.supply_gem_indices[colour]
        arr = self.vector[index:index + self.num_gems_in_play + 1]
        return np.argmax(arr)

    def set_card_location(self, card, location):
        card_index = self.card_indices[card]
        for i in range(2 + self.num_players):
            self.vector[card_index + i] = 0
        if location is not None:
            self.vector[card_index + location] = 1

    def set_supply_gems(self, colour, number):
        index = self.supply_gem_indices[colour]
        num_gems_in_play = self.num_gems_in_play if colour != 'gold' else 5
        self.vector[index:index + num_gems_in_play + 1] = 0
        self.vector[index + number] = 1

    def set_player_gems(self, player_index, colour, number):
        index = self.player_gem_indices[(player_index, colour)]
        num_gems_in_play = self.num_gems_in_play if colour != 'gold' else 5
        for i in range(num_gems_in_play + 1):
            self.vector[index + i] = 0
        self.vector[index + number] = 1

    def set_player_played_colour(self, player_index, colour, number):
        index = self.player_played_colours_indices[(player_index, colour)]
        for i in range(8):
            self.vector[index + i] = 0
        self.vector[index + number] = 1

    def set_player_score(self, player_index, score):
        index = self.player_score_indices[player_index]
        for i in range(21):
            self.vector[index + i] = 0
        self.vector[index + score] = 1

    def set_noble_available(self, noble, available):
        noble_index = self.noble_indices[noble]
        if available:
            self.vector[noble_index] = 1
        else:
            self.vector[noble_index] = 0
    

class GameState(object):

    def __init__(self, players=3, init_game=False, validate=True, generator=None,
                 state_vector=None):
        self.num_players = players
        self.players = []
        self.validate = validate

        if state_vector is None:
            state_vector = StateVector(self.num_players)
        self.state_vector = state_vector

        self.current_player_index = 0

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[players]

        self._tier_1 = tier_1
        self._tier_1_copied = False
        self._tier_2 = tier_2
        self._tier_2_copied = False
        self._tier_3 = tier_3
        self._tier_3_copied = False

        self._tier_1_visible = []
        self._tier_1_visible_copied = False
        self._tier_2_visible = []
        self._tier_2_visible_copied = False
        self._tier_3_visible = []
        self._tier_3_visible_copied = False

        self._num_gold_available = 5
        self._num_white_available = self.num_gems_in_play
        self._num_blue_available = self.num_gems_in_play
        self._num_green_available = self.num_gems_in_play
        self._num_red_available = self.num_gems_in_play
        self._num_black_available = self.num_gems_in_play

        self.initial_nobles = []
        self.nobles = []

        if generator is None:
            generator = np.random.RandomState()
        self.generator = generator

        if init_game:
            self.init_game()

    @property
    def tier_1(self):
        raise ValueError('tier_1')
    @property
    def tier_2(self):
        raise ValueError('tier_2')
    @property
    def tier_3(self):
        raise ValueError('tier_3')

    @property
    def tier_1_available(self):
        raise ValueError('tier_1_available')
    @property
    def tier_2_available(self):
        raise ValueError('tier_2_available')
    @property
    def tier_3_available(self):
        raise ValueError('tier_3_available')

    @property
    def num_gold_available(self):
        raise ValueError('gold')
    @property
    def num_white_available(self):
        raise ValueError('white')
    @property
    def num_blue_available(self):
        raise ValueError('blue')
    @property
    def num_green_available(self):
        raise ValueError('green')
    @property
    def num_red_available(self):
        raise ValueError('red')
    @property
    def num_black_available(self):
        raise ValueError('black')

    def copy(self):
        copy = GameState(self.num_players, validate=self.validate, generator=self.generator,
                         state_vector=self.state_vector.copy())
        for colour in colours + ['gold']:
            setattr(copy, '_num_{}_available'.format(colour), self.num_gems_available(colour))

        copy.initial_nobles = self.initial_nobles
        copy.nobles = self.nobles[:]

        copy._tier_1 = self.cards_in_deck(1, ensure_copied=False)
        copy._tier_2 = self.cards_in_deck(2, ensure_copied=False)
        copy._tier_3 = self.cards_in_deck(3, ensure_copied=False)

        copy._tier_1_visible = self.cards_in_market(1, ensure_copied=False)
        copy._tier_2_visible = self.cards_in_market(2, ensure_copied=False)
        copy._tier_3_visible = self.cards_in_market(3, ensure_copied=False)

        copy.players = [p.copy() for p in self.players]
        copy.current_player_index = self.current_player_index

        copy.generator = self.generator

        return copy

    def get_scores(self):
        scores = [player.score for player in self.players]
        return scores

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def num_gems_available(self, colour):
        return getattr(self, '_num_{}_available'.format(colour))

    def total_num_gems_available(self):
        return sum([self.num_gems_available(colour) for colour in colours])

    def cards_in_deck(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, tier_attr)

    def cards_in_market(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}_visible'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_visible_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, '_tier_{}_visible'.format(tier))

    def add_supply_gems(self, colour, change):
        attr_name = '_num_{}_available'.format(colour)
        setattr(self, attr_name, getattr(self, attr_name) + change)
        self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))

    def seed(self):
        self.generator.seed(seed)

    def init_game(self):
        # Shuffle the cards
        self.generator.shuffle(self.cards_in_deck(1))
        self.generator.shuffle(self.cards_in_deck(2))
        self.generator.shuffle(self.cards_in_deck(3))

        # Select nobles
        orig_nobles = nobles[:]
        self.generator.shuffle(orig_nobles)
        self.nobles = orig_nobles[:self.num_nobles]
        self.initial_nobles = tuple(self.nobles[:])

        # Update visible dev cards
        self.update_dev_cards()

        # Make player objects
        self.players = [Player() for _ in range(self.num_players)]

        # Sync with state vector
        for card in self.cards_in_deck(1) + self.cards_in_deck(2) + self.cards_in_deck(3):
            self.state_vector.set_card_location(card, 0)
        for card in self.cards_in_market(1) + self.cards_in_market(2) + self.cards_in_market(3):
            self.state_vector.set_card_location(card, 1)
        
        for colour in colours:
            self.state_vector.set_supply_gems(colour, self.num_gems_in_play)
        self.state_vector.set_supply_gems('gold', 5)

        for noble in self.initial_nobles:
            self.state_vector.set_noble_available(noble, 1)

        for player_index in range(self.num_players):
            self.state_vector.set_player_score(player_index, 0)
            for colour in colours:
                self.state_vector.set_player_gems(player_index, colour, 0)
                self.state_vector.set_player_played_colour(player_index, colour, 0)
                # self.state_vector.set_player_cards(player_index, colour, 0)
            self.state_vector.set_player_gems(player_index, 'gold', 0)
        

    def make_move(self, move):

        # import ipdb
        # ipdb.set_trace()
        player = self.players[self.current_player_index]
        if move[0] == 'gems':
            player.add_gems(**move[1])
            for colour, change in move[1].items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))

        elif move[0] == 'buy_available':
            action, tier, index, gems = move
            card = self.cards_in_market(tier).pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, None)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                       cur_num_card_colour)

        elif move[0] == 'buy_reserved':
            action, index, gems = move
            card = player.cards_in_hand.pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, None)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                 cur_num_card_colour)

        elif move[0] == 'reserve':
            action, tier, index, gems = move
            if index == -1:
                card = self.cards_in_deck(tier).pop()
            else:
                card = self.cards_in_market(tier).pop(index)
            player.cards_in_hand.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            self.state_vector.set_card_location(card, 2 + self.current_player_index)

        else:
            raise ValueError('Received invalid move {}'.format(move))

        # Assign nobles if necessary
        assignable = []
        for i, noble in enumerate(self.nobles):
            for colour in colours:
                if player.num_cards_of_colour(colour) < noble.num_required(colour):
                    break
            else:
                assignable.append(i)
        if assignable:
            noble = self.nobles.pop(assignable[0])
            self.state_vector.set_noble_available(noble, 0)
            player.nobles.append(noble)

        # Clean up the state
        self.update_dev_cards()

        # Check that everything is within expected parameters
        if self.validate:
            try:
                player.verify_state()
                self.verify_state()
            except AssertionError:
                # TODO: Fix known bug with invalid moves being generated and triggering this
                print('Failure verifying state after making move')
                print('move was', move)
                import traceback
                traceback.print_exc()
                import ipdb; ipdb.set_trace()

        self.current_player_index += 1
        self.current_player_index %= len(self.players)

        return self

    def verify_state(self):
        sv = self.state_vector

        for colour in colours:
            assert 0 <= self.num_gems_available(colour) <= self.num_gems_in_play
        assert 0 <= self.num_gems_available('gold') <= 5

        for colour in colours:
            assert self.num_gems_available(colour) + sum([player.num_gems(colour) for player in self.players]) == self.num_gems_in_play
            assert self.num_gems_available(colour) == self.state_vector.num_supply_gems(colour)

            index = sv.supply_gem_indices[colour]
            assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1
            assert np.sum(sv.vector[index + self.num_gems_available(colour)]) == 1

        for card in self.cards_in_deck(1):
            index = sv.card_indices[card]
            assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 1
            assert sv.vector[index] == 1

        for card in self.cards_in_market(1):
            index = sv.card_indices[card]
            assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 1
            assert sv.vector[index + 1] == 1

        for player_index, player in enumerate(self.players):
            for card in player.cards_in_hand:
                index = sv.card_indices[card]
                assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 1
                assert sv.vector[index + 2 + player_index] == 1

            for card in player.cards_played:
                index = sv.card_indices[card]
                assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 0

            for colour in colours:
                index = sv.player_gem_indices[(player_index, colour)]
                assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1
                assert sv.vector[index + player.num_gems(colour)] == 1

                num_played = len([c for c in player.cards_played if c.colour == colour])
                index = sv.player_played_colours_indices[(player_index, colour)]
                assert np.sum(sv.vector[index:index + 8]) == 1
                assert sv.vector[index + num_played] == 1


        self.state_vector.verify_state()

    def update_dev_cards(self):

        while len(self.cards_in_market(1)) < 4 and self.cards_in_deck(1):
            card = self.cards_in_deck(1).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(1).append(card)

        while len(self.cards_in_market(2)) < 4 and self.cards_in_deck(2):
            card = self.cards_in_deck(2).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(2).append(card)

        while len(self.cards_in_market(3)) < 4 and self.cards_in_deck(3):
            card = self.cards_in_deck(3).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(3).append(card)

    def print_state(self):
        print('{} players'.format(self.num_players))
        print()

        print('Nobles:')
        for noble in self.nobles:
            print(noble)
        print()

        print('Tier 1 visible:')
        for card in self.tier_1_visible:
            print(card)
        print('{} tier 1 remain'.format(len(self.tier_1)))
        print()

        print('Tier 2 visible:')
        for card in self.tier_2_visible:
            print(card)
        print('{} tier 2 remain'.format(len(self.tier_2)))
        print()

        print('Tier 3 visible:')
        for card in self.tier_3_visible:
            print(card)
        print('{} tier 3 remain'.format(len(self.tier_3)))
        print()

        print('Available colours:')
        for colour in colours:
            print('  {}: {}'.format(colour, self.num_gemsavailable(colour)))
        print()

        for i, player in enumerate(self.players):
            i += 1
            print('Player {}:'.format(i))
            for colour in colours + ['gold']:
                print('  {}: {}'.format(colour, player.num_gems(colour)))
            if player.cards_in_hand:
                print(' reserves:'.format(i))
                for card in player.cards_in_hand:
                    print('  ', card)
            if player.cards_played:
                print(' played:'.format(i))
                for card in player.cards_played:
                    print('  ', card)

        # moves = self.get_current_player_valid_moves()
        # for move in moves:
        #     print(move)
        # print('{} moves available'.format(len(moves)))

    def get_valid_moves(self, player_index):

        moves = []
        provisional_moves = []  # moves that take gems, will need checking later
        player = self.players[player_index]

        # Moves that take gems
        # 1) taking two of the same colour
        for colour in colours:
            if self.num_gems_available(colour) >= 4:
                provisional_moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [colour for colour in colours if self.num_gems_available(colour) > 0]
        # for ps in list(set(permutations(available_colours, min(3, len(available_colours))))):
        #     provisional_moves.append(('gems', {p: 1 for p in ps}))
        for selection in choose_3(available_colours, num_to_choose=min(3, len(available_colours))):
            provisional_moves.append(('gems', {c: 1 for c in selection}))

        num_gem_moves = len(provisional_moves)

        # Moves that reserve cards
        if player.num_reserved < 3:
            gold_gained = 1 if self.num_gems_available('gold') > 0 else 0
            for tier in range(1, 4):
                for i in range(len(self.cards_in_market(tier))):
                    provisional_moves.append(('reserve', tier, i, {'gold': gold_gained}))
                if self.cards_in_deck(tier, ensure_copied=False):
                    provisional_moves.append(('reserve', tier, -1, {'gold': gold_gained}))

        num_reserve_moves = len([m for m in provisional_moves if m[0] == 'reserve'])

        # Moves that buy available cards
        buy_moves = []
        for tier in range(1, 4):
            for index, card in enumerate(self.cards_in_market(tier)):
                can_afford, cost = player.can_afford(card)
                if not can_afford:
                    continue
                buy_moves.append(('buy_available', tier, index, {c: -1 * v for c, v in cost.items()}))

        # Moves that buy reserved cards
        for index, card in enumerate(player.cards_in_hand):
            can_afford, cost = player.can_afford(card)
            if not can_afford:
                continue
            buy_moves.append(('buy_reserved', index, {c: -1 * v for c, v in cost.items()}))

        if buy_moves:
            buy_multiplier = max(1, (num_gem_moves + num_reserve_moves) / len(buy_moves))
            buy_multiplier = int(np.round(buy_multiplier))
            for move in buy_moves:
                for _ in range(buy_multiplier):
                    moves.append(move)
        

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        player_gems = player.gems
        for move in provisional_moves:
            if move[0] == 'gems':
                num_gems_gained = sum(move[1].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                num_gems_to_lose = player.total_num_gems + num_gems_gained - 10

                gems_gained = move[1]
                new_gems = {c: (player_gems[c] + gems_gained.get(c, 0)) for c in (colours + ['gold'])}
                possible_discards = discard_to_n_gems(new_gems, 10)
                for discard in possible_discards:
                    new_gems_gained = {key: value for key, value in gems_gained.items()}
                    for key, value in discard.items():
                        if key not in new_gems_gained:
                            new_gems_gained[key] = 0
                        new_gems_gained[key] += value
                    moves.append(('gems', new_gems_gained))

                    # print(num_gems_to_lose, -1 * sum(discard.values()))
                    if num_gems_to_lose != -1 * sum(discard.values()):
                        import ipdb
                        ipdb.set_trace()
                    assert -1 * sum(discard.values()) == num_gems_to_lose

            elif move[0] == 'reserve':
                num_gems_gained = sum(move[3].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                for colour in colours + ['gold']:
                    new_gems_dict = {key: value for key, value in move[3].items()}
                    if player.num_gems(colour) > 0:
                        if colour not in new_gems_dict:
                            new_gems_dict[colour] = 0
                        new_gems_dict[colour] -= 1
                        moves.append(('reserve', move[1], move[2], new_gems_dict))
                        
                # gems_list = set(player.gems_list() + gems_dict_to_list(move[3]))
                # for gem in gems_list:
                #     new_gems_dict = {key: value for key, value in move[3].items()}
                #     if gem not in new_gems_dict:
                #         new_gems_dict[gem] = 0
                #     new_gems_dict[gem] -= 1
                #     moves.append(('reserve', move[1], move[2], new_gems_dict))
 
        # If there are no valid moves, pass with a no-gems-change move
        # print('passing')
        # if len(moves) == 0:
        #     moves.append(('gems', {}))

        return moves

    def get_current_player_valid_moves(self):
        return self.get_valid_moves(self.current_player_index)

    def new_get_state_vector(self, player_perspective_index=None):
        if player_perspective_index is None:
            raise ValueError('player_perspective_index is None')
            player_perspective_index = self.current_player_index

        num_cards = len(all_cards)

        ordered_players = self.players  # the state vector no longer depends on the current player

        vector = np.zeros(613)
        cur_index = 0

        # store card locations
        # card_locations = [0 for _ in range(num_cards * (2 + len(self.players)))]
        card_locations = np.zeros(num_cards * (2 + len(ordered_players)))
        for i, card in enumerate(all_cards):
            if card in self.tier_1 or card in self.tier_2 or card in self.tier_3:
                card_locations[i] = 1
            elif card in self.tier_1_visible or card in self.tier_2_visible or card in self.tier_3_visible:
                card_locations[i + num_cards] = 1
            else:
                for pi, player in enumerate(ordered_players):
                    if card in player.cards_in_hand:
                        card_locations[i + (2 + pi) * num_cards] = 1

        # store numbers of gems in the supply
        num_colour_gems_in_play = self.num_gems_in_play
        # gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
        gem_nums_in_supply = np.zeros(5 * (num_colour_gems_in_play + 1))
        for i, colour in enumerate(colours):
            available = self.num_gems_available(colour)
            gem_nums_in_supply[(num_colour_gems_in_play + 1)*i + available] = 1

        # gold_nums_in_supply = [0 for _ in range(6)]
        gold_nums_in_supply = np.zeros(6)
        gold_nums_in_supply[self.num_gems_available('gold')] = 1

        # store numbers of gems held by each player
        all_player_gems = []
        for player in ordered_players:
            # player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
            player_gems = np.zeros(5 * (num_colour_gems_in_play + 1))
            for i, colour in enumerate(colours):
                num_gems = player.num_gems(colour)
                player_gems[(num_colour_gems_in_play + 1)*i + num_gems] = 1
            all_player_gems.extend(player_gems)
            player_gold_gems = [0 for _ in range(5)]
            player_gold_gems[player.num_gems('gold')] = 1
            all_player_gems.append(player_gold_gems)
        all_player_gems = np.hstack(all_player_gems)
                

        # store numbers of coloured cards played by each player
        # only count up to 7 - more than this makes no difference
        all_player_cards = []
        for player in ordered_players:
            # player_cards = [0 for _ in range(5 * 8)]
            player_cards = np.zeros(5 * 8)
            for i, colour in enumerate(colours):
                num_cards = player.num_cards_of_colour(colour)
                player_cards[8 * i + min(num_cards, 7)] = 1
            all_player_cards.append(player_cards)
        all_player_cards = np.hstack(all_player_cards)

        # store number of points of each player
        # only count up to 20, higher scores are very unlikely
        # player_scores = [0 for _ in range(21 * len(ordered_players))]
        player_scores = np.zeros(21 * len(ordered_players))
        for i, player in enumerate(ordered_players):
            player_scores[i * 21 + min(player.score, 20)] = 1

        # store number of nobles in the game, and available
        # nobles_in_game = [0 for _ in nobles]
        # nobles_available = [0 for _ in nobles]
        # nobles_claimed = [0 for _ in nobles for player in ordered_players]
        nobles_in_game = np.zeros(len(nobles))
        nobles_available = np.zeros(len(nobles))
        nobles_claimed = np.zeros(len(nobles) * len(ordered_players))
        for i, noble in enumerate(nobles):
            if noble in self.initial_nobles:
                nobles_in_game[i] = 1
                if noble in self.nobles:
                    nobles_available[i] = 1
                    continue
                for pi, player in enumerate(ordered_players):
                    if noble in player.nobles:
                        nobles_claimed[len(self.initial_nobles)*pi + i] = 1

        # return np.array(card_locations + gem_nums_in_supply + gold_nums_in_supply +
        #                 all_player_gems + all_player_cards + player_scores +
        #                 nobles_in_game + nobles_available + nobles_claimed)

        return np.hstack([card_locations, gem_nums_in_supply, gold_nums_in_supply,
                          all_player_gems, all_player_cards, player_scores,
                          nobles_in_game, nobles_available, nobles_claimed])

    def get_state_vector(self, player_perspective_index=None):
        
        if player_perspective_index is None:
            raise ValueError('player_perspective_index is None')
            player_perspective_index = self.current_player_index

        return self.state_vector.vector

    # def get_state_vector(self, player_perspective_index=None):
    #     '''Get the current game state as a vector of 1s and 0s, for the neural net.
    #     '''

    #     if player_perspective_index is None:
    #         raise ValueError('player_perspective_index is None')
    #         player_perspective_index = self.current_player_index
    #     # num_gems_available = 0
    #     # orig_gems_available = 5 * self.num_gems_in_play
    #     # for colour in colours:
    #     #     num_gems_available += self.num_gems_available(colour)
    #     # frac_gems_available = num_gems_available / orig_gems_available

    #     # current_player = self.players[player_perspective_index]
    #     # frac_cards_held = len(current_player.cards_in_hand) / 3.

    #     # frac_cards_played = len(current_player.cards_played) / 60.

    #     # frac_gems_held = (current_player.num_gems - current_player.gold) / 10

    #     # return np.array([frac_gems_held, frac_cards_held])


    #     # TODO: Add option to return the vector as a dataframe with row labels

    #     # all_cards = tier_1 + tier_2 + tier_3
    #     num_cards = len(all_cards)

    #     # ordered_players = self.players[player_perspective_index:] + self.players[:player_perspective_index]
    #     ordered_players = self.players  # the state vector no longer depends on the current player

    #     # store card locations
    #     card_locations = [0 for _ in range(num_cards * (2 + len(self.players)))]
    #     for i, card in enumerate(all_cards):
    #         if card in self.tier_1 or card in self.tier_2 or card in self.tier_3:
    #             card_locations[i] = 1
    #         elif card in self.tier_1_visible or card in self.tier_2_visible or card in self.tier_3_visible:
    #             card_locations[i + num_cards] = 1
    #         else:
    #             for pi, player in enumerate(ordered_players):
    #                 if card in player.cards_in_hand:
    #                     card_locations[i + (2 + pi) * num_cards] = 1

    #     # # store how many of the gems we have ready for each card
    #     # card_gems_ready = [0 for _ in all_cards]
    #     # current_player = ordered_players[0]
    #     # for i, card in enumerate(all_cards):
    #     #     num_gems_needed = np.sum(card.requirements)
    #     #     num_gems_ready = 0
    #     #     for colour in colours:
    #     #         num_gems_ready += min(getattr(current_player, colour), getattr(card, colour))
    #     #     num_gems_ready += min(num_gems_needed - num_gems_ready, current_player.gold)
    #     #     card_gems_ready[i] = num_gems_ready / num_gems_needed
                
    #     # store numbers of gems in the supply
    #     num_colour_gems_in_play = self.num_gems_in_play
    #     gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
    #     for i, colour in enumerate(colours):
    #         available = self.num_gems_available(colour)
    #         gem_nums_in_supply[(num_colour_gems_in_play + 1)*i + available] = 1

    #     gold_nums_in_supply = [0 for _ in range(6)]
    #     gold_nums_in_supply[self.num_gems_available('gold')] = 1

    #     # store numbers of gems held by each player
    #     all_player_gems = []
    #     for player in ordered_players:
    #         player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
    #         for i, colour in enumerate(colours):
    #             num_gems = getattr(player, colour)
    #             player_gems[(num_colour_gems_in_play + 1)*i + num_gems] = 1
    #         all_player_gems.extend(player_gems)
    #         player_gold_gems = [0 for _ in range(5)]
    #         player_gold_gems[getattr(player, 'gold')] = 1
    #         all_player_gems.extend(player_gold_gems)
                

    #     # store numbers of coloured cards played by each player
    #     # only count up to 7 - more than this makes no difference
    #     all_player_cards = []
    #     for player in ordered_players:
    #         player_cards = [0 for _ in range(5 * 8)]
    #         for i, colour in enumerate(colours):
    #             num_cards = player.num_cards_of_colour(colour)
    #             player_cards[8 * i + min(num_cards, 7)] = 1
    #         all_player_cards.extend(player_cards)

    #     # store number of points of each player
    #     # only count up to 20, higher scores are very unlikely
    #     player_scores = [0 for _ in range(21 * len(ordered_players))]
    #     for i, player in enumerate(ordered_players):
    #         player_scores[i * 21 + min(player.score, 20)] = 1

    #     # store number of nobles in the game, and available
    #     nobles_in_game = [0 for _ in nobles]
    #     nobles_available = [0 for _ in nobles]
    #     nobles_claimed = [0 for _ in nobles for player in ordered_players]
    #     for i, noble in enumerate(nobles):
    #         if noble in self.initial_nobles:
    #             nobles_in_game[i] = 1
    #             if noble in self.nobles:
    #                 nobles_available[i] = 1
    #                 continue
    #             for pi, player in enumerate(ordered_players):
    #                 if noble in player.nobles:
    #                     nobles_claimed[len(self.initial_nobles)*pi + i] = 1

    #     # num cards played
    #     # cards_played = [0 for _ in range(4)]
    #     # num_cards_played = len(ordered_players[0].cards_played)
    #     # # print('num cards played', num_cards_played, ordered_players[0].cards_played, ordered_players[1].cards_played)
    #     # cards_played[num_cards_played] = 1
                
    #     # arr = np.array(card_locations[(2*len(all_cards)):] + gem_nums_in_supply)
    #     # return arr

    #     # cur_player = ordered_players[0]
    #     # can_win = [1 if (cur_player.red >= 1 and cur_player.black >= 1 and cur_player.white >= 1) else 0]

    #     return np.array(card_locations + gem_nums_in_supply + gold_nums_in_supply +
    #                     # card_gems_ready + 
    #                     all_player_gems + all_player_cards + player_scores +
    #                     nobles_in_game + nobles_available + nobles_claimed)
    #                     # +
    #                     # cards_played)
        


def discard_to_n_gems(gems, target, current_possibility={}, possibilities=None, colours=['white', 'blue', 'green', 'red', 'black']):
    if possibilities is None:
        return discard_to_n_gems(gems, target, current_possibility, colours=colours, possibilities=[])
    num_gems = sum(gems.values())

    if num_gems == target:
        possibilities.append(current_possibility)
        return possibilities
    if not colours:
        return possibilities
    assert num_gems >= target

    orig_current_possibility = {c: n for c, n in current_possibility.items()}

    colours = colours[:]
    colour = colours.pop()

    num_gems_of_colour = gems.get(colour, 0)
    for i in range(0, min(num_gems_of_colour, num_gems - target) + 1):
        current_gems = {c: n for c, n in gems.items()}
        current_gems[colour] -= i
        current_possibility = {c: n for c, n in orig_current_possibility.items()}
        current_possibility[colour] = -1 * i
        discard_to_n_gems(current_gems, target,
                          current_possibility=current_possibility,
                          possibilities=possibilities,
                          colours=colours)
        
    return possibilities

def choose_3(colours, input_selection=[], outputs=None, num_to_choose=3):
    if outputs is None:
        outputs = set()
    colours = colours[:]

    while colours:
        colour = colours.pop()

        # 1) add this colour to the selection
        cur_selection = input_selection[:]
        cur_selection.append(colour)
        if len(cur_selection) == num_to_choose:
            cur_selection = tuple(cur_selection)
            outputs.add(cur_selection) 
            # outputs.append(tuple(cur_selection))
        else:
            choose_3(colours, input_selection=cur_selection, outputs=outputs, num_to_choose=num_to_choose)

        # 2) don't add this colour to the selection
        cur_selection = input_selection[:]
        choose_3(colours, input_selection=cur_selection, outputs=outputs, num_to_choose=num_to_choose)

    return outputs
            
            

def gems_dict_to_list(d):
    return (['white' for _ in range(d.get('white', 0))] +
            ['blue' for _ in range(d.get('blue', 0))] +
            ['green' for _ in range(d.get('green', 0))] +
            ['red' for _ in range(d.get('red', 0))] +
            ['black' for _ in range(d.get('black', 0))] +
            ['gold' for _ in range(d.get('gold', 0))])

def main():
    manager = GameState()
    manager.print_state()

if __name__ == "__main__":
    main()
