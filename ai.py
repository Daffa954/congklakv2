import math
import random

# Constants
PLAYER_ONE = 0
PLAYER_TWO = 1
PLAYER_ONE_STORE = 6
PLAYER_TWO_STORE = 13
PITS_PER_PLAYER = 6
TOTAL_PITS = 14

class MancalaAI:
    def __init__(self, depth=6):
        self.depth = depth
        self.nodes_evaluated = 0
        self.transposition_table = {}
    
    def get_valid_moves(self, board, player):
        """Get all valid moves for the given player"""
        # cek lubang yang bisa dipilih jika kosong tidak bisa dipilih
        if player == PLAYER_ONE:
            return [i for i in range(0, 6) if board.pits[i] > 0]
        else:
            return [i for i in range(7, 13) if board.pits[i] > 0]
    
    def evaluate_board(self, board):
        """
        Evaluate the board state from AI's perspective (PLAYER_TWO)
        Higher score means better position for AI
        """
        score = 0
        
        # Cek Score
        score += (board.pits[PLAYER_TWO_STORE] - board.pits[PLAYER_ONE_STORE]) * 100
        
        # Additional strategic factors
        for i in range(7, 13):  # AI pits
            if board.pits[i] > 0:
                # Bonus jika berhasil mengambil lubang yang kosong
                if board.pits[i] <= (13 - i):
                    landing_pit = i + board.pits[i]
                    if landing_pit < 13 and board.pits[landing_pit] == 0:
                        opposite_pit = 12 - landing_pit
                        if board.pits[opposite_pit] > 0:
                            score += 15
                
                # Bonus score
                if (i + board.pits[i]) % 14 == PLAYER_TWO_STORE:
                    score += 20
        
        # Jika AI memberi lawan extra turn
        for i in range(7, 13):
            if board.pits[i] == 0:
                score -= 5
        
        return score
    
    def alpha_beta(self, board, depth, alpha, beta, player, maximizing_player=True):
        """
        Alpha-beta pruning algorithm for minimax
        """
        self.nodes_evaluated += 1
        
        # Base Case
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        # Board untuk menyimpan memori
        board_hash = tuple(board.pits)
        if board_hash in self.transposition_table:
            stored_depth, stored_value = self.transposition_table[board_hash]
            if stored_depth >= depth:
                return stored_value
        
        valid_moves = self.get_valid_moves(board, player)
        
        if not valid_moves:
            return self.evaluate_board(board)
        
        if (maximizing_player and player == PLAYER_TWO) :
            # Maximizing AI
            max_eval = -math.inf
            for move in valid_moves:
                new_board = board.clone()
                extra_turn = new_board.make_move(move, player)
                
                if extra_turn:
                    # Jika AI dapat extra turn 
                    eval_score = self.alpha_beta(new_board, depth - 1, alpha, beta, player, maximizing_player)
                else:
                    # berganti
                    eval_score = self.alpha_beta(new_board, depth - 1, alpha, beta, 1 - player, not maximizing_player)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # pruning
            
            # simpan ke transposition table 
            self.transposition_table[board_hash] = (depth, max_eval)
            return max_eval
        
        else:
            # Minimizing player (Human)
            min_eval = math.inf
            for move in valid_moves:
                new_board = board.clone()
                extra_turn = new_board.make_move(move, player)
                
                if extra_turn:
                    # Jika Player dapat extra turn
                    eval_score = self.alpha_beta(new_board, depth - 1, alpha, beta, player, maximizing_player)
                else:
                    # Berganti
                    eval_score = self.alpha_beta(new_board, depth - 1, alpha, beta, 1 - player, not maximizing_player)
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # 
            
           
            self.transposition_table[board_hash] = (depth, min_eval)
            return min_eval
    
    def get_best_move(self, board, player):
        """
        Get the best move for the AI using alpha-beta pruning
        """
        self.nodes_evaluated = 0
        self.transposition_table.clear()
        
        best_score = -math.inf
        best_moves = []
        alpha = -math.inf
        beta = math.inf
        
        valid_moves = self.get_valid_moves(board, player)
        
        if not valid_moves:
            return None
        
        # Jika hanya terdapat 1
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        for move in valid_moves:
            new_board = board.clone()
            extra_turn = new_board.make_move(move, player)
            
            if extra_turn:
                # AI mendapatkan extraturn menjalankan maximize
                score = self.alpha_beta(new_board, self.depth - 1, alpha, beta, player, True)
            else:
                # Switch to human player
                score = self.alpha_beta(new_board, self.depth - 1, alpha, beta, 1 - player, False)
            
            # Update best move
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)
            
            alpha = max(alpha, best_score)
        
        # If multiple moves have same score, choose randomly for variety
        chosen_move = random.choice(best_moves) if best_moves else None
        
        # Print debugging info (optional)
        print(f"AI evaluated {self.nodes_evaluated} nodes, chose move {chosen_move} with score {best_score}")
        
        return chosen_move
    
    def set_difficulty(self, depth):
        """Change AI difficulty by adjusting search depth"""
        self.depth = depth