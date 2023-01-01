import pygame
import constants


class Inventory:
    def __init__(self):
        # Create an empty inventory
        self.items = []

        # Load the inventory GUI image
        self.image = pygame.Surface((200,200))
        self.image.fill(constants.BLUE)

        # Set the inventory GUI position
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)

    def add_item(self, item):
        # Add an item to the inventory
        self.items.append(item)

    def remove_item(self, item):
        # Remove an item from the inventory
        self.items.remove(item)

    def draw(self, surface):
        # Draw the inventory GUI on the given surface
        surface.blit(self.image, self.rect)

        # Draw the inventory items on top of the GUI
        font = pygame.font.Font(None, 36)
        y = 10
        for item in self.items:
            text = font.render(item, 1, (255, 255, 255))
            surface.blit(text, (self.rect.left + 10, self.rect.top + y))
            y += 40


# Set up Pygame
pygame.init()

# Create a window for the game
screen = pygame.display.set_mode((640, 480))

# Create an inventory
inventory = Inventory()

# Add some items to the inventory
inventory.add_item("Stone")
inventory.add_item("Dirt")
inventory.add_item("Grass")

# Run the game loop
running = True
while running:
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the inventory
    inventory.draw(screen)

    # Update the display
    pygame.display.flip()

    # Check for events and quit the game if necessary
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
