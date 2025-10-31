import pygame
import sys
import math
import time
import random
from ai import MancalaAI

BACKGROUND_COLOR = (25, 25, 35)
PIT_COLOR = (70, 130, 180)
PIT_COLOR_2 = (220, 120, 70)
STONE_COLOR = (240, 240, 240)
STONE_COLOR_2 = (200, 200, 220)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
HIGHLIGHT_COLOR = (255, 255, 255, 80)
GLOW_COLOR = (100, 200, 255, 100)

# New colors for visual feedback
SELECTED_PIT_COLOR = (255, 215, 0)  # Gold for selected pit
RECEIVING_PIT_COLOR = (144, 238, 144)  # Light green for receiving stones
CAPTURE_COLOR = (255, 100, 255)  # Magenta for captured pits

PLAYER_ONE = 0
PLAYER_TWO = 1
PLAYER_ONE_STORE = 6
PLAYER_TWO_STORE = 13
PITS_PER_PLAYER = 6
TOTAL_PITS = 14

# Difficulty levels dan Nilai Depth
DIFFICULTY_EASY = 3
DIFFICULTY_MEDIUM = 6
DIFFICULTY_HARD = 10

# Inisialisasi jumlah batu
STONES_3 = 3
STONES_4 = 4
STONES_5 = 5

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Master Congklak - AI Challenge")
clock = pygame.time.Clock()


# Kelas Untuk Aturan main papan
class Board:
    def __init__(self, initial_stones=4):
        self.initial_stones = initial_stones
        self.pits = (
            [initial_stones] * PITS_PER_PLAYER
            + [0]
            + [initial_stones] * PITS_PER_PLAYER
            + [0]
        )

    # agar tidak merubah data board asli
    def clone(self):
        new_board = Board(self.initial_stones)
        new_board.pits = self.pits.copy()
        return new_board

    def make_move(self, pit, player):
        stones = self.pits[pit]
        self.pits[pit] = 0
        current_pit = pit

        while stones > 0:
            current_pit = (current_pit + 1) % TOTAL_PITS

            if player == PLAYER_ONE and current_pit == PLAYER_TWO_STORE:
                continue
            if player == PLAYER_TWO and current_pit == PLAYER_ONE_STORE:
                continue

            self.pits[current_pit] += 1
            stones -= 1

        # extra turn menyimpan True or false
        extra_turn = (player == PLAYER_ONE and current_pit == PLAYER_ONE_STORE) or (
            player == PLAYER_TWO and current_pit == PLAYER_TWO_STORE
        )

        # Hanya panggil capture jika BUKAN giliran ekstra
        if not extra_turn:
            self.handle_capture(current_pit, player)

        return extra_turn

    def handle_capture(self, last_pit, player):
        if (
            player == PLAYER_ONE
            and 0 <= last_pit < PLAYER_ONE_STORE
            and self.pits[last_pit]
            == 1  # Lubang terakhir adalah milik pemain & berisi 1
        ):
            opposite = 12 - last_pit
            if self.pits[opposite] > 0:  # Lubang seberang ada isinya
                self.pits[PLAYER_ONE_STORE] += self.pits[opposite] + 1
                self.pits[last_pit] = 0
                self.pits[opposite] = 0

        elif (
            player == PLAYER_TWO
            and PLAYER_ONE_STORE < last_pit < PLAYER_TWO_STORE
            and self.pits[last_pit] == 1
        ):
            opposite = 12 - last_pit
            if self.pits[opposite] > 0:
                self.pits[PLAYER_TWO_STORE] += self.pits[opposite] + 1
                self.pits[last_pit] = 0
                self.pits[opposite] = 0

    def is_game_over(self):
        return all(self.pits[i] == 0 for i in range(0, 6)) or all(
            self.pits[i] == 0 for i in range(7, 13)
        )

    def end_game(self):
        for i in range(0, 6):
            self.pits[PLAYER_ONE_STORE] += self.pits[i]
            self.pits[i] = 0
        for i in range(7, 13):
            self.pits[PLAYER_TWO_STORE] += self.pits[i]
            self.pits[i] = 0

    def evaluate(self):
        return self.pits[PLAYER_TWO_STORE] - self.pits[PLAYER_ONE_STORE]


# Controller game view dan board
class MancalaGame:
    def __init__(self, difficulty=DIFFICULTY_MEDIUM, initial_stones=4):
        self.initial_stones = initial_stones
        self.board = Board(initial_stones)
        self.current_player = PLAYER_ONE
        self.difficulty = difficulty
        self.ai = MancalaAI(depth=difficulty)

    def reset(self, difficulty=None, initial_stones=None):
        if difficulty is not None:
            self.difficulty = difficulty
        if initial_stones is not None:
            self.initial_stones = initial_stones
        self.board = Board(self.initial_stones)
        self.current_player = PLAYER_ONE
        self.ai = MancalaAI(depth=self.difficulty)

    def is_valid_move(self, pit):
        return (
            self.current_player == PLAYER_ONE
            and 0 <= pit < 6
            and self.board.pits[pit] > 0
        ) or (
            self.current_player == PLAYER_TWO
            and 7 <= pit < 13
            and self.board.pits[pit] > 0
        )

    def make_move(self, pit, view=None, animate=False):
        stones = self.board.pits[pit]
        self.board.pits[pit] = 0
        current_pit = pit
        
        # Visual feedback: highlight selected pit
        if view:
            view.selected_pit = pit
            view.last_pit = None
            view.captured_pits = []
            view.draw_board()
            pygame.display.update()
            pygame.time.wait(800)  # Show selected pit longer

        while stones > 0:
            current_pit = (current_pit + 1) % TOTAL_PITS
            if self.current_player == PLAYER_ONE and current_pit == PLAYER_TWO_STORE:
                continue
            if self.current_player == PLAYER_TWO and current_pit == PLAYER_ONE_STORE:
                continue

            self.board.pits[current_pit] += 1
            stones -= 1

            if animate and view:
                view.receiving_pit = current_pit
                view.sync_positions_after_move()
                view.draw_board()
                pygame.display.update()
                pygame.time.wait(650)  # Slower animation for each stone drop

        if view:
            view.selected_pit = None
            view.receiving_pit = None
            view.last_pit = current_pit
            view.sync_positions_after_move()

        extra_turn = (
            self.current_player == PLAYER_ONE and current_pit == PLAYER_ONE_STORE
        ) or (self.current_player == PLAYER_TWO and current_pit == PLAYER_TWO_STORE)

        # Panggil capture HANYA jika tidak ada giliran tambahan
        if not extra_turn:
            # Check if capture will happen and store the pits for visual feedback
            if view:
                captured = self.check_capture(current_pit, self.current_player)
                if captured:
                    view.captured_pits = captured
                    view.draw_board()
                    pygame.display.update()
                    pygame.time.wait(1500)  # Show capture longer
                    
            self.board.handle_capture(current_pit, self.current_player)
            # Pindah pemain
            self.current_player = 1 - self.current_player

        if view:
            view.captured_pits = []
            view.last_pit = None
            view.sync_positions_after_move()

    def check_capture(self, last_pit, player):
        """Check if a capture will happen and return the pits involved"""
        if (
            player == PLAYER_ONE
            and 0 <= last_pit < PLAYER_ONE_STORE
            and self.board.pits[last_pit] == 1
        ):
            opposite = 12 - last_pit
            if self.board.pits[opposite] > 0:
                return [last_pit, opposite]
                
        elif (
            player == PLAYER_TWO
            and PLAYER_ONE_STORE < last_pit < PLAYER_TWO_STORE
            and self.board.pits[last_pit] == 1
        ):
            opposite = 12 - last_pit
            if self.board.pits[opposite] > 0:
                return [last_pit, opposite]
        
        return []

    def ai_move(self, view):
        move = self.ai.get_best_move(self.board, PLAYER_TWO)
        if move is not None:
            self.make_move(move, view, animate=True)


# Tampilan view
class MancalaView:
    def __init__(self, game):
        self.game = game
        
        # Visual feedback attributes
        self.selected_pit = None
        self.receiving_pit = None
        self.last_pit = None
        self.captured_pits = []

        # Posisi tombol
        self.quit_rect = pygame.Rect(WIDTH - 170, 30, 140, 50)

        # Tombol di bawah papan
        bottom_button_y = HEIGHT - 80  # MOVED DOWN: Was HEIGHT - 90
        button_width = 260
        button_height = 60
        button_spacing = 30
        total_bottom_width = (button_width * 3) + (button_spacing * 2)
        bottom_start_x = (WIDTH - total_bottom_width) // 2

        self.difficulty_rect = pygame.Rect(
            bottom_start_x, bottom_button_y, button_width, button_height
        )
        self.stones_rect = pygame.Rect(
            bottom_start_x + button_width + button_spacing,
            bottom_button_y,
            button_width,
            button_height,
        )
        self.restart_rect = pygame.Rect(
            bottom_start_x + 2 * (button_width + button_spacing),
            bottom_button_y,
            button_width,
            button_height,
        )

        self.stone_positions = {i: [] for i in range(TOTAL_PITS)}

        # State & Animasi
        self.pulse_value = 0
        self.pulse_direction = 1
        self.show_difficulty_menu = False
        self.show_stones_menu = False

        try:
            self.title_font = pygame.font.Font(None, 80)
            self.big_font = pygame.font.Font(None, 60)
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 30)
            self.tiny_font = pygame.font.Font(None, 24)
        except:
            self.title_font = pygame.font.Font(None, 70)
            self.big_font = pygame.font.Font(None, 50)
            self.font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 26)
            self.tiny_font = pygame.font.Font(None, 22)

        # Tombol Menu
        menu_button_width = 280
        menu_button_height = 70
        menu_start_x = (WIDTH - menu_button_width) // 2
        menu_start_y = HEIGHT // 2 - 100

        self.difficulty_buttons = {
            "easy": pygame.Rect(
                menu_start_x, menu_start_y, menu_button_width, menu_button_height
            ),
            "medium": pygame.Rect(
                menu_start_x, menu_start_y + 80, menu_button_width, menu_button_height
            ),
            "hard": pygame.Rect(
                menu_start_x, menu_start_y + 160, menu_button_width, menu_button_height
            ),
        }

        self.stones_buttons = {
            "3": pygame.Rect(
                menu_start_x, menu_start_y, menu_button_width, menu_button_height
            ),
            "4": pygame.Rect(
                menu_start_x, menu_start_y + 80, menu_button_width, menu_button_height
            ),
            "5": pygame.Rect(
                menu_start_x, menu_start_y + 160, menu_button_width, menu_button_height
            ),
        }

        # PERBAIKAN BUG KLIK: Hitung tata letak di sini
        self.board_width = min(1100, WIDTH - 200)
        self.board_height = 450
        self.board_x = (WIDTH - self.board_width) // 2
        self.board_y = (HEIGHT - self.board_height) // 2
        self.board_rect = pygame.Rect(
            self.board_x, self.board_y, self.board_width, self.board_height
        )

        self.store_width = 90
        self.store_height = 300
        self.stores_center_y = self.board_y + self.board_height // 2
        self.left_store_x = self.board_x + 40
        self.right_store_x = self.board_x + self.board_width - 40 - self.store_width
        self.ai_store_rect = pygame.Rect(
            self.left_store_x,
            self.stores_center_y - self.store_height // 2,
            self.store_width,
            self.store_height,
        )
        self.player_store_rect = pygame.Rect(
            self.right_store_x,
            self.stores_center_y - self.store_height // 2,
            self.store_width,
            self.store_height,
        )

        self.pits_start_x = self.left_store_x + self.store_width + 50
        self.pits_area_width = self.right_store_x - self.pits_start_x - 50
        self.pit_spacing = self.pits_area_width // 6
        self.pit_radius = 45

        # Simpan koordinat lubang untuk deteksi klik
        self.pit_coords = {}
        # Lubang AI (Atas)
        for idx, pit in enumerate(range(12, 6, -1)):
            x = self.pits_start_x + idx * self.pit_spacing + self.pit_spacing // 2
            y = self.stores_center_y - 80
            self.pit_coords[pit] = (x, y)
        # Lubang Player (Bawah)
        for idx, pit in enumerate(range(0, 6)):
            x = self.pits_start_x + idx * self.pit_spacing + self.pit_spacing // 2
            y = self.stores_center_y + 80
            self.pit_coords[pit] = (x, y)

        self.generate_initial_positions()

    def draw_text(self, text, x, y, font_obj, color=TEXT_COLOR, center=True):
        text_surface = font_obj.render(text, True, color)
        rect = (
            text_surface.get_rect(center=(x, y))
            if center
            else text_surface.get_rect(topleft=(x, y))
        )
        screen.blit(text_surface, rect)

    def random_stone_positions(self, count, store=False):
        positions = []
        min_distance = 10
        max_attempts = 100
        radius_variance = 30 if not store else 60

        for _ in range(count):
            placed = False
            for _ in range(max_attempts):
                angle = random.uniform(0, 2 * math.pi)
                dist = random.randint(15, radius_variance)
                sx = dist * math.cos(angle)
                sy = dist * math.sin(angle)
                if all(
                    math.hypot(sx - ox, sy - oy) >= min_distance for ox, oy in positions
                ):
                    positions.append((sx, sy))
                    placed = True
                    break
            if not placed:
                positions.append((random.uniform(-15, 15), random.uniform(-15, 15)))
        return positions

    def generate_initial_positions(self):
        for pit in range(TOTAL_PITS):
            self.stone_positions[pit] = self.random_stone_positions(
                self.game.board.pits[pit],
                store=(pit in [PLAYER_ONE_STORE, PLAYER_TWO_STORE]),
            )

    def sync_positions_after_move(self):
        for pit in range(TOTAL_PITS):
            current = len(self.stone_positions[pit])
            target = self.game.board.pits[pit]
            store = pit in [PLAYER_ONE_STORE, PLAYER_TWO_STORE]
            if target > current:
                new_pos = self.random_stone_positions(target - current, store=store)
                self.stone_positions[pit].extend(new_pos)
            elif target < current:
                self.stone_positions[pit] = self.stone_positions[pit][:target]

    def draw_stones(self, count, x, y, pit, is_player_one=False):
        store = pit in [PLAYER_ONE_STORE, PLAYER_TWO_STORE]
        radius = 8 if not store else 10

        # Sinkronkan ulang jika jumlahnya tidak cocok
        if len(self.stone_positions[pit]) != count:
            self.stone_positions[pit] = self.random_stone_positions(count, store=store)

        for i, (sx, sy) in enumerate(self.stone_positions[pit]):
            stone_color = STONE_COLOR_2 if i % 2 == 0 else STONE_COLOR
            pygame.draw.circle(
                screen, (30, 30, 30, 100), (int(x + sx + 2), int(y + sy + 2)), radius
            )
            pygame.draw.circle(screen, stone_color, (int(x + sx), int(y + sy)), radius)
            pygame.draw.circle(
                screen, (255, 255, 255, 150), (int(x + sx - 2), int(y + sy - 2)), 2
            )

    def draw_modern_button(self, rect, text, hover=False, color=None):
        if color is None:
            color = BUTTON_COLOR if not hover else BUTTON_HOVER

        shadow_offset = 4 if not hover else 2

        shadow_rect = rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(screen, (30, 30, 40), shadow_rect, border_radius=12)

        pygame.draw.rect(screen, color, rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255, 50), rect, 2, border_radius=12)

        self.draw_text(
            text, rect.centerx, rect.centery, self.small_font, (255, 255, 255)
        )

    def draw_difficulty_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        self.draw_text(
            "SELECT DIFFICULTY",
            WIDTH // 2,
            HEIGHT // 2 - 200,
            self.big_font,
            (255, 255, 255),
        )

        mouse_pos = pygame.mouse.get_pos()

        easy_color = (100, 200, 100)
        medium_color = (255, 200, 100)
        hard_color = (255, 100, 100)

        desc_x = self.difficulty_buttons["easy"].right + 150

        easy_hover = self.difficulty_buttons["easy"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.difficulty_buttons["easy"], "EASY", easy_hover, easy_color
        )
        self.draw_text(
            "Depth: 3 - Fast moves",
            desc_x,
            self.difficulty_buttons["easy"].centery,
            self.small_font,
            (200, 200, 200),
        )

        medium_hover = self.difficulty_buttons["medium"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.difficulty_buttons["medium"], "MEDIUM", medium_hover, medium_color
        )
        self.draw_text(
            "Depth: 6 - Balanced",
            desc_x,
            self.difficulty_buttons["medium"].centery,
            self.small_font,
            (200, 200, 200),
        )

        hard_hover = self.difficulty_buttons["hard"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.difficulty_buttons["hard"], "HARD", hard_hover, hard_color
        )
        self.draw_text(
            "Depth: 10 - Challenging",
            desc_x,
            self.difficulty_buttons["hard"].centery,
            self.small_font,
            (200, 200, 200),
        )

        current_diff = f"Current: {self.get_difficulty_name()}"
        self.draw_text(
            current_diff, WIDTH // 2, HEIGHT // 2 + 250, self.font, (255, 255, 255)
        )

    def draw_stones_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        self.draw_text(
            "SELECT STONES PER PIT",
            WIDTH // 2,
            HEIGHT // 2 - 200,
            self.big_font,
            (255, 255, 255),
        )

        mouse_pos = pygame.mouse.get_pos()

        stones_3_color = (100, 200, 200)
        stones_4_color = (200, 200, 100)
        stones_5_color = (200, 100, 200)

        desc_x = self.stones_buttons["3"].right + 150

        stones_3_hover = self.stones_buttons["3"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.stones_buttons["3"], "3 STONES", stones_3_hover, stones_3_color
        )
        self.draw_text(
            "Faster game, more strategic",
            desc_x,
            self.stones_buttons["3"].centery,
            self.small_font,
            (200, 200, 200),
        )

        stones_4_hover = self.stones_buttons["4"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.stones_buttons["4"], "4 STONES", stones_4_hover, stones_4_color
        )
        self.draw_text(
            "Classic Mancala",
            desc_x,
            self.stones_buttons["4"].centery,
            self.small_font,
            (200, 200, 200),
        )

        stones_5_hover = self.stones_buttons["5"].collidepoint(mouse_pos)
        self.draw_modern_button(
            self.stones_buttons["5"], "5 STONES", stones_5_hover, stones_5_color
        )
        self.draw_text(
            "Longer game, more stones",
            desc_x,
            self.stones_buttons["5"].centery,
            self.small_font,
            (200, 200, 200),
        )

        current_stones = f"Current: {self.game.initial_stones} stones per pit"
        self.draw_text(
            current_stones, WIDTH // 2, HEIGHT // 2 + 250, self.font, (255, 255, 255)
        )

    def get_difficulty_name(self):
        if self.game.difficulty == DIFFICULTY_EASY:
            return "EASY"
        elif self.game.difficulty == DIFFICULTY_MEDIUM:
            return "MEDIUM"
        else:
            return "HARD"

    def get_stones_name(self):
        return f"{self.game.initial_stones} STONES"

    def draw_game_over_screen(self, result, color, player_score, ai_score):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        self.draw_text(result, WIDTH // 2, HEIGHT // 2 - 60, self.big_font, color)

        score_text = f"FINAL SCORE: {player_score} - {ai_score}"
        self.draw_text(
            score_text, WIDTH // 2, HEIGHT // 2 + 40, self.font, (255, 255, 255)
        )

        self.draw_text(
            "Starting new game in 3 seconds...",
            WIDTH // 2,
            HEIGHT // 2 + 120,
            self.small_font,
            (200, 200, 220),
        )

        pygame.display.flip()

    def draw_board(self, ai_thinking=False):
        # Cek menu
        if self.show_difficulty_menu:
            self.draw_difficulty_menu()
            pygame.display.flip()
            return

        if self.show_stones_menu:
            self.draw_stones_menu()
            pygame.display.flip()
            return

        self.sync_positions_after_move()

        # Background color
        screen.fill(BACKGROUND_COLOR)

        # Efek gradien
        for y in range(0, HEIGHT, 4):
            oscillation = (math.sin(y / 100 + time.time()) + 1) / 2
            brightness_mod = int(oscillation * 15)

            r = 30 + brightness_mod
            g = 35 + brightness_mod
            b = 45 + brightness_mod

            color = (r, g, b)

            pygame.draw.rect(screen, color, (0, y, WIDTH, 4))

        self.pulse_value += 0.05 * self.pulse_direction
        if self.pulse_value > 1 or self.pulse_value < 0:
            self.pulse_direction *= -1

        # Title
        title_text = "MASTER CONGKLAK"
        title_main = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_main.get_rect(center=(WIDTH // 2, 60))
        screen.blit(title_main, title_rect)

        # Shadow Papan
        shadow_rect = self.board_rect.copy()
        shadow_rect.x += 8
        shadow_rect.y += 8
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=25)
        # Papan
        pygame.draw.rect(screen, (40, 45, 60), self.board_rect, border_radius=25)
        pygame.draw.rect(screen, (60, 65, 80), self.board_rect, 5, border_radius=25)

        # Indikator Giliran
        turn_text = (
            "YOUR TURN"
            if self.game.current_player == PLAYER_ONE
            else "AI IS THINKING..."
        )
        turn_color = (
            (100, 255, 150)
            if self.game.current_player == PLAYER_ONE
            else (255, 150, 100)
        )

        # Animasi denyut untuk warna
        r = int(turn_color[0] * (0.8 + 0.2 * self.pulse_value))
        g = int(turn_color[1] * (0.8 + 0.2 * self.pulse_value))
        b = int(turn_color[2] * (0.8 + 0.2 * self.pulse_value))
        animated_turn_color = (r, g, b)

        self.draw_text(
            turn_text, WIDTH // 2, self.board_y - 30, self.font, animated_turn_color
        )

        # Lumbung (Gunakan atribut self)
        # Lumbung AI (Kiri)
        pygame.draw.rect(
            screen, (50, 55, 75), self.ai_store_rect.inflate(10, 10), border_radius=20
        )
        pygame.draw.rect(screen, PIT_COLOR, self.ai_store_rect, border_radius=15)
        pygame.draw.rect(
            screen, (255, 255, 255, 30), self.ai_store_rect, 3, border_radius=20
        )
        self.draw_stones(
            self.game.board.pits[PLAYER_TWO_STORE],
            self.ai_store_rect.centerx,
            self.ai_store_rect.centery,
            PLAYER_TWO_STORE,
        )
        self.draw_text(
            "AI",
            self.ai_store_rect.centerx,
            self.ai_store_rect.top - 25,
            self.font,
            (200, 200, 220),
        )
        self.draw_text(
            str(self.game.board.pits[PLAYER_TWO_STORE]),
            self.ai_store_rect.centerx,
            self.ai_store_rect.bottom + 30,
            self.big_font,
            (255, 255, 255),
        )

        # Lumbung Player (Kanan)
        pygame.draw.rect(
            screen,
            (50, 55, 75),
            self.player_store_rect.inflate(10, 10),
            border_radius=20,
        )
        pygame.draw.rect(screen, PIT_COLOR_2, self.player_store_rect, border_radius=15)
        pygame.draw.rect(
            screen, (255, 255, 255, 30), self.player_store_rect, 3, border_radius=20
        )
        self.draw_stones(
            self.game.board.pits[PLAYER_ONE_STORE],
            self.player_store_rect.centerx,
            self.player_store_rect.centery,
            PLAYER_ONE_STORE,
        )
        self.draw_text(
            "PLAYER",
            self.player_store_rect.centerx,
            self.player_store_rect.top - 25,
            self.font,
            (220, 220, 200),
        )
        self.draw_text(
            str(self.game.board.pits[PLAYER_ONE_STORE]),
            self.player_store_rect.centerx,
            self.player_store_rect.bottom + 30,
            self.big_font,
            (255, 255, 255),
        )

        # Lubang AI (Atas)
        for idx, pit in enumerate(range(12, 6, -1)):
            x, y = self.pit_coords[pit]
            
            # Determine pit color based on state
            current_pit_color = PIT_COLOR
            if pit == self.selected_pit:
                current_pit_color = SELECTED_PIT_COLOR
            elif pit == self.receiving_pit:
                current_pit_color = RECEIVING_PIT_COLOR
            elif pit in self.captured_pits:
                current_pit_color = CAPTURE_COLOR
            
            # Glow effect for valid moves
            if self.game.current_player == PLAYER_TWO and self.game.is_valid_move(pit) and not self.selected_pit:
                alpha = int(100 + 80 * self.pulse_value)
                highlight_surf = pygame.Surface(
                    (self.pit_radius * 2 + 20, self.pit_radius * 2 + 20),
                    pygame.SRCALPHA,
                )
                pygame.draw.circle(
                    highlight_surf,
                    (*GLOW_COLOR[:3], alpha),
                    (self.pit_radius + 10, self.pit_radius + 10),
                    self.pit_radius + 10,
                )
                screen.blit(
                    highlight_surf, (x - self.pit_radius - 10, y - self.pit_radius - 10)
                )

            pygame.draw.circle(screen, (50, 55, 75), (x, y), self.pit_radius + 4)
            pygame.draw.circle(screen, current_pit_color, (x, y), self.pit_radius)
            pygame.draw.circle(screen, (255, 255, 255, 30), (x, y), self.pit_radius, 2)
            
            # Extra highlight for selected/receiving/captured pits
            if pit == self.selected_pit:
                pygame.draw.circle(screen, (255, 255, 255, 200), (x, y), self.pit_radius, 5)
                self.draw_text("SELECTED!", x, y - 80, self.small_font, SELECTED_PIT_COLOR)
            elif pit == self.receiving_pit:
                pygame.draw.circle(screen, (255, 255, 255, 150), (x, y), self.pit_radius, 4)
                self.draw_text("RECEIVING", x, y - 80, self.small_font, RECEIVING_PIT_COLOR)
            elif pit in self.captured_pits:
                pygame.draw.circle(screen, (255, 255, 255, 200), (x, y), self.pit_radius, 5)
                self.draw_text("CAPTURED!", x, y - 80, self.small_font, CAPTURE_COLOR)
            
            self.draw_stones(self.game.board.pits[pit], x, y, pit)
            self.draw_text(str(6 - idx), x, y - 60, self.small_font, (200, 200, 220))
            stone_count = self.game.board.pits[pit]
            if stone_count > 0:
                self.draw_text(
                    str(stone_count), x, y + 55, self.small_font, (255, 255, 0)
                )

        # Lubang Player (Bawah)
        for idx, pit in enumerate(range(0, 6)):
            x, y = self.pit_coords[pit]
            
            # Determine pit color based on state
            current_pit_color = PIT_COLOR_2
            if pit == self.selected_pit:
                current_pit_color = SELECTED_PIT_COLOR
            elif pit == self.receiving_pit:
                current_pit_color = RECEIVING_PIT_COLOR
            elif pit in self.captured_pits:
                current_pit_color = CAPTURE_COLOR
            
            # Glow effect for valid moves
            if self.game.current_player == PLAYER_ONE and self.game.is_valid_move(pit) and not self.selected_pit:
                alpha = int(100 + 80 * self.pulse_value)
                highlight_surf = pygame.Surface(
                    (self.pit_radius * 2 + 20, self.pit_radius * 2 + 20),
                    pygame.SRCALPHA,
                )
                pygame.draw.circle(
                    highlight_surf,
                    (255, 200, 100, alpha),
                    (self.pit_radius + 10, self.pit_radius + 10),
                    self.pit_radius + 10,
                )
                screen.blit(
                    highlight_surf, (x - self.pit_radius - 10, y - self.pit_radius - 10)
                )

            pygame.draw.circle(screen, (50, 55, 75), (x, y), self.pit_radius + 4)
            pygame.draw.circle(screen, current_pit_color, (x, y), self.pit_radius)
            pygame.draw.circle(screen, (255, 255, 255, 30), (x, y), self.pit_radius, 2)
            
            # Extra highlight for selected/receiving/captured pits
            if pit == self.selected_pit:
                pygame.draw.circle(screen, (255, 255, 255, 200), (x, y), self.pit_radius, 5)
                self.draw_text("SELECTED!", x, y + 80, self.small_font, SELECTED_PIT_COLOR)
            elif pit == self.receiving_pit:
                pygame.draw.circle(screen, (255, 255, 255, 150), (x, y), self.pit_radius, 4)
                self.draw_text("RECEIVING", x, y + 80, self.small_font, RECEIVING_PIT_COLOR)
            elif pit in self.captured_pits:
                pygame.draw.circle(screen, (255, 255, 255, 200), (x, y), self.pit_radius, 5)
                self.draw_text("CAPTURED!", x, y + 80, self.small_font, CAPTURE_COLOR)
            
            self.draw_stones(self.game.board.pits[pit], x, y, pit, True)
            self.draw_text(str(idx + 1), x, y + 60, self.small_font, (220, 220, 200))
            stone_count = self.game.board.pits[pit]
            if stone_count > 0:
                self.draw_text(
                    str(stone_count), x, y - 55, self.small_font, (255, 255, 0)
                )

        # Label Pemain
        self.draw_text(
            "ARTIFICIAL INTELLIGENCE",
            WIDTH // 2,
            self.board_y + 30,
            self.font,
            (170, 210, 255),
        )
        self.draw_text(
            "HUMAN PLAYER",
            WIDTH // 2,
            self.board_y + self.board_height - 30,
            self.font,
            (255, 210, 170),
        )

        # Tampilan Pengaturan
        settings_y = self.board_rect.bottom + 20  # MOVED UP: Was +35
        diff_text = f"DIFFICULTY: {self.get_difficulty_name()}"
        stones_text = f"STONES: {self.get_stones_name()}"
        self.draw_text(
            diff_text, WIDTH // 2 - 200, settings_y, self.small_font, (200, 200, 255)
        )
        self.draw_text(
            stones_text, WIDTH // 2 + 200, settings_y, self.small_font, (200, 255, 200)
        )

        # Tombol-Tombol
        mouse_pos = pygame.mouse.get_pos()
        self.draw_modern_button(
            self.restart_rect, "RESTART", self.restart_rect.collidepoint(mouse_pos)
        )
        self.draw_modern_button(
            self.quit_rect, "QUIT", self.quit_rect.collidepoint(mouse_pos)
        )
        self.draw_modern_button(
            self.difficulty_rect,
            "CHANGE DIFFICULTY",
            self.difficulty_rect.collidepoint(mouse_pos),
        )
        self.draw_modern_button(
            self.stones_rect, "CHANGE STONES", self.stones_rect.collidepoint(mouse_pos)
        )

        # Instruksi dengan visual feedback legend
        instruction_y = self.board_rect.bottom + 42  # MOVED: Was HEIGHT - 45
        self.draw_text(
            "Click on your pits (1-6) to make a move",
            WIDTH // 2,
            instruction_y,
            self.small_font,  # Kept small_font
            (150, 150, 170),
        )
        
        # Legend for colors (MOVED TO TOP LEFT)
        legend_x_start = 30
        legend_y_start = 30
        legend_y_spacing = 25

        # Selected pit legend
        pygame.draw.circle(screen, SELECTED_PIT_COLOR, (legend_x_start, legend_y_start), 8)
        self.draw_text("Selected", legend_x_start + 15, legend_y_start, self.tiny_font, (200, 200, 200), center=False)
        
        # Receiving pit legend
        pygame.draw.circle(screen, RECEIVING_PIT_COLOR, (legend_x_start, legend_y_start + legend_y_spacing), 8)
        self.draw_text("Receiving", legend_x_start + 15, legend_y_start + legend_y_spacing, self.tiny_font, (200, 200, 200), center=False)
        
        # Captured pit legend
        pygame.draw.circle(screen, CAPTURE_COLOR, (legend_x_start, legend_y_start + 2 * legend_y_spacing), 8)
        self.draw_text("Captured", legend_x_start + 15, legend_y_start + 2 * legend_y_spacing, self.tiny_font, (200, 200, 200), center=False)


        # Overlay AI Thinking
        if ai_thinking:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            thinking_text = "AI IS ANALYZING MOVES..."
            self.draw_text(
                thinking_text, WIDTH // 2, HEIGHT // 2, self.big_font, (255, 255, 255)
            )
            dots = "." * (int(time.time() * 2) % 4)
            self.draw_text(
                "Thinking" + dots,
                WIDTH // 2,
                HEIGHT // 2 + 60,
                self.font,
                (200, 200, 255),
            )

        pygame.display.flip()


# === MAIN LOOP ===
def main():
    game = MancalaGame(difficulty=DIFFICULTY_MEDIUM, initial_stones=4)
    view = MancalaView(game)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if view.show_difficulty_menu:
                        view.show_difficulty_menu = False
                    elif view.show_stones_menu:
                        view.show_stones_menu = False
                    else:
                        running = False
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if view.show_difficulty_menu:
                    # Handle difficulty selection
                    if view.difficulty_buttons["easy"].collidepoint(mouse_pos):
                        game.reset(difficulty=DIFFICULTY_EASY)
                        view.show_difficulty_menu = False
                    elif view.difficulty_buttons["medium"].collidepoint(mouse_pos):
                        game.reset(difficulty=DIFFICULTY_MEDIUM)
                        view.show_difficulty_menu = False
                    elif view.difficulty_buttons["hard"].collidepoint(mouse_pos):
                        game.reset(difficulty=DIFFICULTY_HARD)
                        view.show_difficulty_menu = False
                elif view.show_stones_menu:
                    # Handle stones selection
                    if view.stones_buttons["3"].collidepoint(mouse_pos):
                        game.reset(initial_stones=STONES_3)
                        view.show_stones_menu = False
                    elif view.stones_buttons["4"].collidepoint(mouse_pos):
                        game.reset(initial_stones=STONES_4)
                        view.show_stones_menu = False
                    elif view.stones_buttons["5"].collidepoint(mouse_pos):
                        game.reset(initial_stones=STONES_5)
                        view.show_stones_menu = False
                else:
                    # Handle main menu buttons
                    if view.restart_rect.collidepoint(mouse_pos):
                        game.reset()
                        view = MancalaView(
                            game
                        )  # Buat ulang view untuk reset posisi biji
                    elif view.quit_rect.collidepoint(mouse_pos):
                        running = False
                    elif view.difficulty_rect.collidepoint(mouse_pos):
                        view.show_difficulty_menu = True
                    elif view.stones_rect.collidepoint(mouse_pos):
                        view.show_stones_menu = True

                    elif game.current_player == PLAYER_ONE:
                        # Gunakan koordinat dari 'view' untuk deteksi
                        for pit, (pit_x, pit_y) in view.pit_coords.items():
                            if 0 <= pit < 6:  # Hanya periksa lubang pemain (0-5)
                                # Cek jarak mouse ke pusat lubang
                                if (
                                    math.hypot(
                                        pit_x - mouse_pos[0], pit_y - mouse_pos[1]
                                    )
                                    < view.pit_radius
                                ):
                                    if game.is_valid_move(pit):
                                        game.make_move(pit, view, animate=True)
                                        break  # Keluar dari loop setelah menemukan lubang yg diklik

        if not running:
            break

        view.draw_board()

        if (
            game.board.is_game_over()
            and not view.show_difficulty_menu
            and not view.show_stones_menu
        ):
            game.board.end_game()

            player_score = game.board.pits[PLAYER_ONE_STORE]
            ai_score = game.board.pits[PLAYER_TWO_STORE]

            if player_score > ai_score:
                result = "VICTORY! YOU WIN! 🎉"
                color = (100, 255, 150)
            elif ai_score > player_score:
                result = "AI WINS! 🤖"
                color = (255, 150, 100)
            else:
                result = "IT'S A TIE! ⚖️"
                color = (255, 255, 150)

            view.draw_game_over_screen(result, color, player_score, ai_score)

            time.sleep(3)
            game.reset()
            view = MancalaView(game)  # Buat ulang view untuk reset posisi biji
            continue

        if (
            game.current_player == PLAYER_TWO
            and not game.board.is_game_over()
            and not view.show_difficulty_menu
            and not view.show_stones_menu
        ):
            view.draw_board(ai_thinking=True)
            pygame.display.update()

            # Tentukan jeda berdasarkan kesulitan - slower thinking time
            if game.difficulty == DIFFICULTY_EASY:
                think_time = 1000  # 1 second
            elif game.difficulty == DIFFICULTY_MEDIUM:
                think_time = 1500  # 1.5 seconds
            else:
                think_time = 2000  # 2 seconds

            pygame.time.wait(think_time)
            game.ai_move(view)

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

