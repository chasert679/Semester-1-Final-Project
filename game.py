import pygame
import random
import sys
import fsm
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
LANE_HEIGHT = HEIGHT // 6
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
AI_WIDTH, AI_HEIGHT = 30, 30
LINE_WIDTH = 2
FPS = 30

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)



class RaceGame:
    def __init__(self, track_length, num_ai, time_limit, player_image_path):
        self.track_length = track_length
        self.num_ai = num_ai
        self.player_position = 0  # Start player on the left side of the lanes
        self.player_speed = 10  # Player's movement speed
        self.player_direction = 1  # 1 for right, -1 for left
        self.ai_positions = [-AI_WIDTH] * num_ai  # Start AI slightly more to the left side
        self.ai_speeds = [random.uniform(1, 3) for _ in range(num_ai)]  # AI's initial random movement speeds
        self.ai_directions = [1] * num_ai  # 1 for right, -1 for left
        self.time_limit = time_limit
        self.start_time = pygame.time.get_ticks()

        # Set up Pygame screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Race Game")

        # Load player image
        self.player_image = pygame.image.load(player_image_path)
        self.player_image = pygame.transform.scale(self.player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # Adjust starting position of the player a few pixels above
        self.player_position_y = LANE_HEIGHT - 75

        # Variables for handling key presses
        self.a_pressed = False
        self.d_pressed = False

        # Initialize Finite State Machine
        self.fsm = fsm.FiniteStateMachine()

    def draw_race(self):
        # Draw blue background
        self.screen.fill(BLUE)

        # Draw lanes
        for i in range(1, 6):
            pygame.draw.line(self.screen, WHITE, (0, i * LANE_HEIGHT), (WIDTH, i * LANE_HEIGHT), LINE_WIDTH)

        # Draw player
        player_size_multiplier = self.fsm.get_player_size_multiplier()
        player_width = int(PLAYER_WIDTH * player_size_multiplier)
        player_height = int(PLAYER_HEIGHT * player_size_multiplier)
        player_image_scaled = pygame.transform.scale(self.player_image, (player_width, player_height))
        self.screen.blit(player_image_scaled, (self.player_position, self.player_position_y))

        # Draw AI opponents
        for i, ai_position in enumerate(self.ai_positions):
            pygame.draw.rect(self.screen, WHITE, (self.ai_positions[i], (i + 1) * LANE_HEIGHT + (LANE_HEIGHT - AI_HEIGHT) // 2, AI_WIDTH, AI_HEIGHT))

        # Update the display
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def player_move(self):
        keys = pygame.key.get_pressed()

        if self.fsm.current_state != "stuck":
            if keys[pygame.K_a] and not self.d_pressed:
                self.a_pressed = True
            elif keys[pygame.K_d] and self.a_pressed:
                self.a_pressed = False
                self.d_pressed = True
                self.player_position += int(self.player_speed * self.player_direction * self.fsm.get_player_speed_multiplier())
            else:
                self.d_pressed = False

            # Check if the player has reached the end of the track
            if self.player_position >= self.track_length:
                self.player_direction = -1
                self.player_position = self.track_length - 1  # Adjust position to prevent overshooting

            # Check if the player has reached the beginning of the track
            if self.player_position < 0:
                self.player_direction = 1
                self.player_position = 0  # Adjust position to prevent overshooting

        self.fsm.handle_w_key()  # Check W key press for the stuck state

    def ai_move(self):
        # Implement AI logic for movement
        for i in range(self.num_ai):
            self.ai_positions[i] += int(self.ai_speeds[i]) * self.ai_directions[i]
            self.ai_speeds[i] = random.uniform(1, 3)

            # Check if an AI has reached the end of the track
            if self.ai_positions[i] >= self.track_length:
                self.ai_directions[i] = -1
                self.ai_positions[i] = self.track_length - 1  # Adjust position to prevent overshooting

            # Check if an AI has reached the beginning of the track
            if self.ai_positions[i] < 0:
                self.ai_directions[i] = 1
                self.ai_positions[i] = 0  # Adjust position to prevent overshooting

    def check_winner(self):
        laps_completed = self.player_position // self.track_length

        if laps_completed >= 3 and all(ai >= 3 * self.track_length for ai in self.ai_positions):
            return "It's a tie!"
        elif laps_completed >= 3:
            return "Player wins!"
        elif all(ai >= 3 * self.track_length for ai in self.ai_positions):
            return "AI wins!"
        else:
            return None

    def check_timeout(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        return elapsed_time >= self.time_limit * 1000  # Convert seconds to milliseconds

    def play_game(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()
            self.player_move()
            self.ai_move()
            self.fsm.update_state()  # Update the state of the Finite State Machine
            self.draw_race()

            winner = self.check_winner()
            if winner:
                print(winner)
                pygame.quit()
                sys.exit()

            if self.check_timeout():
                print("Time's up! AI wins.")
                pygame.quit()
                sys.exit()

            clock.tick(FPS)

if __name__ == "__main__":
    # Example usage with 5 AI opponents, a longer time limit of 60 seconds,
    # and specifying the path to the player's image file
    race_game = RaceGame(track_length=WIDTH, num_ai=5, time_limit=60, player_image_path='7129395.png')
    race_game.play_game()