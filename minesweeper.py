"""
Minesweeper Game Logic
Handles the game board, mine placement, and game state
"""

import random
from typing import Set, Tuple, List


class Minesweeper:
    def __init__(self, rows: int = 10, cols: int = 10, num_mines: int = 10):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.mines: Set[Tuple[int, int]] = set()
        self.game_over = False
        self.game_won = False
        self.first_click = True
        
    def initialize_board(self, first_row: int, first_col: int):
        """Initialize the board with mines, avoiding the first clicked cell"""
        # Generate mine positions
        available_positions = [
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if (r, c) != (first_row, first_col)
        ]
        
        self.mines = set(random.sample(available_positions, self.num_mines))
        
        # Calculate numbers for each cell
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in self.mines:
                    self.board[row][col] = -1  # -1 represents a mine
                else:
                    # Count adjacent mines
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if (nr, nc) in self.mines:
                                    count += 1
                    self.board[row][col] = count
        
        self.first_click = False
    
    def reveal_cell(self, row: int, col: int) -> bool:
        """Reveal a cell and return True if game continues, False if mine hit"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return True
        
        if self.revealed[row][col] or self.flagged[row][col]:
            return True
        
        # Initialize board on first click
        if self.first_click:
            self.initialize_board(row, col)
        
        self.revealed[row][col] = True
        
        # Check if mine was hit
        if self.board[row][col] == -1:
            self.game_over = True
            self.reveal_all_mines()
            return False
        
        # If empty cell (0), reveal adjacent cells recursively
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self.reveal_cell(row + dr, col + dc)
        
        # Check for win condition
        self.check_win()
        return True
    
    def toggle_flag(self, row: int, col: int):
        """Toggle flag on a cell"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        
        if not self.revealed[row][col]:
            self.flagged[row][col] = not self.flagged[row][col]
    
    def reveal_all_mines(self):
        """Reveal all mines (called when game is lost)"""
        for row, col in self.mines:
            self.revealed[row][col] = True
    
    def check_win(self):
        """Check if the player has won"""
        for row in range(self.rows):
            for col in range(self.cols):
                # If a non-mine cell is not revealed, game is not won
                if self.board[row][col] != -1 and not self.revealed[row][col]:
                    return
        
        self.game_won = True
        self.game_over = True
    
    def get_cell_value(self, row: int, col: int) -> int:
        """Get the value of a cell"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.board[row][col]
        return 0
    
    def is_revealed(self, row: int, col: int) -> bool:
        """Check if a cell is revealed"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.revealed[row][col]
        return False
    
    def is_flagged(self, row: int, col: int) -> bool:
        """Check if a cell is flagged"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.flagged[row][col]
        return False
    
    def get_flags_remaining(self) -> int:
        """Get the number of flags remaining"""
        flags_placed = sum(sum(row) for row in self.flagged)
        return self.num_mines - flags_placed
    
    def reset(self):
        """Reset the game"""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines = set()
        self.game_over = False
        self.game_won = False
        self.first_click = True
