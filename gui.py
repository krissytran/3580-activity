"""
Minesweeper GUI using Pygame
Main game interface and rendering
"""

import pygame
import sys
from minesweeper import Minesweeper


class MinesweeperGUI:
    # Colors
    BG_COLOR = (189, 189, 189)
    CELL_COLOR = (192, 192, 192)
    REVEALED_COLOR = (211, 211, 211)
    MINE_COLOR = (255, 0, 0)
    FLAG_COLOR = (255, 100, 100)
    TEXT_COLORS = {
        1: (0, 0, 255),
        2: (0, 128, 0),
        3: (255, 0, 0),
        4: (0, 0, 128),
        5: (128, 0, 0),
        6: (0, 128, 128),
        7: (0, 0, 0),
        8: (128, 128, 128)
    }
    
    BUTTON_COLOR = (100, 100, 100)
    BUTTON_HOVER = (120, 120, 120)
    BUTTON_TEXT = (255, 255, 255)
    
    def __init__(self, rows: int = 10, cols: int = 10, num_mines: int = 10, cell_size: int = 40):
        pygame.init()
        
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.cell_size = cell_size
        self.margin = 10
        self.header_height = 80
        
        # Calculate window size
        self.width = cols * cell_size + 2 * self.margin
        self.height = rows * cell_size + 2 * self.margin + self.header_height
        
        # Create window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.cell_font = pygame.font.Font(None, 28)
        
        # Game instance
        self.game = Minesweeper(rows, cols, num_mines)
        
        # Buttons
        self.new_game_button = pygame.Rect(self.margin, 10, 120, 30)
        self.easy_button = pygame.Rect(self.margin + 140, 10, 80, 30)
        self.medium_button = pygame.Rect(self.margin + 230, 10, 80, 30)
        self.hard_button = pygame.Rect(self.margin + 320, 10, 80, 30)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
    def draw_button(self, rect: pygame.Rect, text: str, mouse_pos: tuple):
        """Draw a button with hover effect"""
        color = self.BUTTON_HOVER if rect.collidepoint(mouse_pos) else self.BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, (50, 50, 50), rect, 2, border_radius=5)
        
        text_surface = self.small_font.render(text, True, self.BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_header(self, mouse_pos: tuple):
        """Draw the header with buttons and info"""
        # Draw buttons
        self.draw_button(self.new_game_button, "New Game", mouse_pos)
        self.draw_button(self.easy_button, "Easy", mouse_pos)
        self.draw_button(self.medium_button, "Medium", mouse_pos)
        self.draw_button(self.hard_button, "Hard", mouse_pos)
        
        # Draw flags remaining
        flags_text = f"Flags: {self.game.get_flags_remaining()}"
        flags_surface = self.small_font.render(flags_text, True, (0, 0, 0))
        self.screen.blit(flags_surface, (self.margin, 50))
        
        # Draw game status
        if self.game.game_won:
            status_text = "YOU WIN! 🎉"
            color = (0, 150, 0)
        elif self.game.game_over:
            status_text = "GAME OVER!"
            color = (200, 0, 0)
        else:
            status_text = "Playing..."
            color = (0, 0, 0)
        
        status_surface = self.small_font.render(status_text, True, color)
        status_rect = status_surface.get_rect(right=self.width - self.margin, top=50)
        self.screen.blit(status_surface, status_rect)
    
    def draw_board(self):
        """Draw the game board"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.margin
                y = row * self.cell_size + self.margin + self.header_height
                
                # Draw cell background
                if self.game.is_revealed(row, col):
                    color = self.REVEALED_COLOR
                    if self.game.get_cell_value(row, col) == -1:
                        color = self.MINE_COLOR
                else:
                    color = self.CELL_COLOR
                
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (100, 100, 100), (x, y, self.cell_size, self.cell_size), 1)
                
                # Draw cell content
                if self.game.is_flagged(row, col):
                    # Draw flag
                    pygame.draw.polygon(self.screen, self.FLAG_COLOR, [
                        (x + self.cell_size // 4, y + self.cell_size // 4),
                        (x + 3 * self.cell_size // 4, y + self.cell_size // 2),
                        (x + self.cell_size // 4, y + 3 * self.cell_size // 4)
                    ])
                elif self.game.is_revealed(row, col):
                    value = self.game.get_cell_value(row, col)
                    if value == -1:
                        # Draw mine
                        center = (x + self.cell_size // 2, y + self.cell_size // 2)
                        pygame.draw.circle(self.screen, (0, 0, 0), center, self.cell_size // 4)
                    elif value > 0:
                        # Draw number
                        text = self.cell_font.render(str(value), True, self.TEXT_COLORS.get(value, (0, 0, 0)))
                        text_rect = text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.screen.blit(text, text_rect)
    
    def get_cell_from_pos(self, pos: tuple) -> tuple:
        """Convert mouse position to cell coordinates"""
        x, y = pos
        if y < self.header_height:
            return None, None
        
        col = (x - self.margin) // self.cell_size
        row = (y - self.margin - self.header_height) // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None, None
    
    def handle_click(self, pos: tuple, button: int):
        """Handle mouse click"""
        # Check button clicks
        if self.new_game_button.collidepoint(pos):
            self.game.reset()
            return
        
        if self.easy_button.collidepoint(pos):
            self.rows, self.cols, self.num_mines = 8, 8, 10
            self.resize_window()
            self.game = Minesweeper(self.rows, self.cols, self.num_mines)
            return
        
        if self.medium_button.collidepoint(pos):
            self.rows, self.cols, self.num_mines = 16, 16, 40
            self.resize_window()
            self.game = Minesweeper(self.rows, self.cols, self.num_mines)
            return
        
        if self.hard_button.collidepoint(pos):
            self.rows, self.cols, self.num_mines = 16, 30, 99
            self.resize_window()
            self.game = Minesweeper(self.rows, self.cols, self.num_mines)
            return
        
        # Handle board clicks
        row, col = self.get_cell_from_pos(pos)
        if row is not None and not self.game.game_over:
            if button == 1:  # Left click
                self.game.reveal_cell(row, col)
            elif button == 3:  # Right click
                self.game.toggle_flag(row, col)
    
    def resize_window(self):
        """Resize window for different difficulty levels"""
        self.width = self.cols * self.cell_size + 2 * self.margin
        self.height = self.rows * self.cell_size + 2 * self.margin + self.header_height
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    def run(self):
        """Main game loop"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
            
            # Draw everything
            self.screen.fill(self.BG_COLOR)
            self.draw_header(mouse_pos)
            self.draw_board()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game_gui = MinesweeperGUI(rows=10, cols=10, num_mines=10)
    game_gui.run()
