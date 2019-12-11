import random
import copy
import time
import game as g
# import game
import math


def max_value(game, ttime, timeout, number, depth):
    if timeout - 0.5 < ttime or game.t >= 200 or depth > 2:
        return game.get_player_score(number)
    else:
        m_value = -math.inf
        possible_moves = game.get_possible_moves()
        for move in possible_moves:
            new_game = g.Game()
            game.copy(new_game)
            new_game.apply(move)
            new_game.t += 1
            v = min_value(new_game, time.time(), timeout, number, depth + 1)
            if v > m_value:
                m_value = v
        return m_value


def min_value(game, ttime, timeout, number, depth):
    if timeout - 0.5 < ttime or game.t >= 200 or depth > 2:
        return game.get_player_score(number)
    else:
        mi_value = math.inf
        possible_moves = game.get_possible_moves()
        for move in possible_moves:
            new_game = g.Game()
            game.copy(new_game)
            new_game.apply(move)
            new_game.t += 1
            v = max_value(new_game, time.time(), timeout, number, depth)
            if v < mi_value:
                mi_value = v
        return mi_value




class Player:
    """
    Base class for a game-playing agent. 
    You must implement the next_move() method to complete this class.
    
    Parameters
    ----------
    number : int
        The number of the player. If 1 then this player goes first. Otherwise this
        player goes second.
    timeout : float (optional)
        Max time (in seconds) given for the next_move() function to return. If function 
        does not return in this amount of time, it is an automatic forfeit.
    """
    def __init__(self, number, timeout):
        self.number = number
        self.timeout = timeout

    def next_move(self, game):
        raise NotImplementedError("This should be implemented")


class RandomPlayer(Player):
    def next_move(self, game):
        """
        Randomly select a move from the available possible moves.

        Parameters
        ----------
        game : `game.Game`
            An instance of `game.Game` encoding the current state of the
            game.
            
        Returns
        ----------
        (int, int) or None
            A randomly selected possible move.
        """
        possible_moves = game.get_possible_moves()
        if len(possible_moves) > 0:
            move = possible_moves[random.randint(0, len(possible_moves) - 1)]
        else:
            move = None
        return move


class CustomPlayer(Player):
    def next_move(self, game):
        """
        Parameters
            ----------
            game : `game.Game`
                An instance of `game.Game` encoding the current state of the
                game.
            
            Returns
            ----------
            (int, int) or None
                A  possible move. First int is the moving piece's location id. Second int is the target location id.
                
                If None is returned when possible moves are available, it is an automatic forfeit and the player will 
                lose the match.
                
                If function does not return before timeout seconds have passed, it is an automatic forfeit as well.
                
                *** These timeout restrictions will be applied during the grading phase. ***
                
        """
        start = time.time()
        best_move = None
        best_score = 0
        possible_moves = game.get_possible_moves()
        for move in possible_moves:
            new_game = g.Game()
            game.copy(new_game)
            new_game.apply(move)
            new_game.t += 1
            score = min_value(game, time.time(), self.timeout + start, self.number, 0)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move


