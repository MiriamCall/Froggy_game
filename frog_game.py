import arcade
import random

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Froggy Game"

# Sprite filenames
FROG_SPRITE = "frog_300_sprite.png"
VEHICLE_SPRITE = "bus_sprite.png"

# Scaling constants
SPRITE_SCALING = 0.2
VEHICLE_SCALING = 0.3

# Movement speed
PLAYER_MOVEMENT_SPEED = 3
VEHICLE_MOVEMENT_SPEED = 5

class FroggyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite lists
        self.player_list = None
        self.vehicle_list = None
        
        # Player sprite
        self.player_sprite = None
        
        # Level and score
        self.level = 1
        self.score = 0
        
        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize variables """
        # Create sprite lists
        self.player_list = arcade.SpriteList()
        self.vehicle_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(
            FROG_SPRITE,
            SPRITE_SCALING
        )
        
        # Starting position of the player
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 20
        
        self.player_list.append(self.player_sprite)
        
        # Create vehicles
        for i in range(5):
            vehicle = arcade.Sprite(
                VEHICLE_SPRITE,
                VEHICLE_SCALING
            )
            
            # Position the vehicle
            vehicle.center_y = random.randrange(100, SCREEN_HEIGHT - 100)
            vehicle.center_x = random.randrange(SCREEN_WIDTH)
            
            # Add vehicle speed attribute
            vehicle.change_x = VEHICLE_MOVEMENT_SPEED * (1 + (self.level - 1) * 0.2)
            
            self.vehicle_list.append(vehicle)

    def on_draw(self):
        """ Render the screen """
        self.clear()
        
        # Draw sprites
        self.player_list.draw()
        self.vehicle_list.draw()
        
        # Draw score and level
        arcade.draw_text(
            f"Level: {self.level}  Score: {self.score}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            20
        )

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed """
        if key == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.level = 1
            self.score = 0
            self.setup()  # Restart the game


    def on_key_release(self, key, modifiers):
        """ Called whenever a key is released """
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.player_sprite.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Update player position
        self.player_list.update()
        
        # Keep player on screen
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT:
            # Player reached the top - next level!
            self.level += 1
            self.score += 100
            self.reset_player()
            self.increase_difficulty()
        
        # Update vehicles
        self.vehicle_list.update()
        
        # Loop vehicles around screen
        for vehicle in self.vehicle_list:
            if vehicle.right < 0:
                vehicle.left = SCREEN_WIDTH
            elif vehicle.left > SCREEN_WIDTH:
                vehicle.right = 0
        
        # Check for collisions
        if self.player_sprite.collides_with_list(self.vehicle_list):
            self.reset_player()

    def reset_player(self):
        """ Reset player position """
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 20
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def increase_difficulty(self):
        """ Increase game difficulty by adjusting vehicle speed and repositioning them """
        for vehicle in self.vehicle_list:
            # Increase speed based on level
            vehicle.change_x = VEHICLE_MOVEMENT_SPEED * (1 + (self.level - 1) * 0.2)

            # Reposition vehicles randomly
            vehicle.center_x = random.randrange(SCREEN_WIDTH)
        vehicle.center_y = random.randrange(100, SCREEN_HEIGHT - 100)


def main():
    """ Main function """
    window = FroggyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()