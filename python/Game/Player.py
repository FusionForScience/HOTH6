import pygame
import consts

class Player(pygame.sprite.Sprite):
    """ This class represents the rectangle the player controls. """

    # Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        
        self.image = pygame.Surface([consts.width, consts.height])
        self.image.fill(consts.RED)
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .65
 
        # See if we are on the ground.
        if self.rect.y >= consts.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = consts.SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # Move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= consts.SCREEN_HEIGHT:
            self.change_y = -10
        
    
    def duck(self):
        """ Ducks when player holds 'down' button. """
        if self.rect.y <= consts.SCREEN_HEIGHT - self.rect.height:
            self.change_y = 0
            self.rect.y = consts.SCREEN_HEIGHT - self.rect.height
            self.image = pygame.Surface([consts.width, 25])
            self.image.fill(consts.RED)
    
            # Set a reference to the image rect.
            self.rect = self.image.get_rect()

            self.rect.x = 100
            self.rect.y = consts.SCREEN_HEIGHT - self.rect.height
            #screen.fill(BLUE)
        
    def revert(self):
        """ Reverts to normal after ducking. """
        self.image = pygame.Surface([consts.width, consts.height])
        self.image.fill(consts.RED)
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        self.rect.x = 100
        self.rect.y = consts.SCREEN_HEIGHT - self.rect.height