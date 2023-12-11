import pygame
class FiniteStateMachine:
    def __init__(self):
        self.states = {"normal": 1.0, "double_speed": 2.0, "stuck": 0.5}
        self.current_state = "stuck"  # Start in the "stuck" state
        self.transition_time = 15
        self.state_start_time = pygame.time.get_ticks()
        self.double_speed_duration = 5
        self.double_speed_start_time = 0
        self.stuck_duration = 40
        self.stuck_start_time = pygame.time.get_ticks()  # Set the start time for the stuck state
        self.w_pressed_count = 0

    def update_state(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.state_start_time) / 1000

        if elapsed_time >= self.transition_time:
            self.state_start_time = current_time
            self.w_pressed_count = 0

            if self.current_state == "stuck":
                self.current_state = "normal"
            else:
                self.current_state = "double_speed" if self.current_state == "normal" else "normal"
            self.double_speed_start_time = current_time

        if self.current_state == "stuck":
            elapsed_time_stuck = (current_time - self.stuck_start_time) / 1000
            if elapsed_time_stuck >= self.stuck_duration:
                self.current_state = "normal"
                self.state_start_time = current_time

    def get_player_speed_multiplier(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.double_speed_start_time) / 1000

        if self.current_state == "double_speed" and elapsed_time < self.double_speed_duration:
            return self.states["double_speed"]
        elif self.current_state == "stuck":
            return self.states["stuck"]
        else:
            return self.states["normal"]

    def get_player_size_multiplier(self):
        if self.current_state == "stuck":
            return self.states["stuck"]
        else:
            return 1.0

    def handle_w_key(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.current_state == "stuck" and keys[pygame.K_w]:
            self.w_pressed_count += 1

            if self.w_pressed_count >= 30:
                self.current_state = "normal"
                self.state_start_time = current_time
                self.w_pressed_count = 0