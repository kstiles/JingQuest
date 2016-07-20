import pygame
from button import Button

class Toolbar(pygame.sprite.Sprite):

    def __init__(self, width):

        # Don't add to any sprite groups, toolbar drawn differently from
        super(Toolbar, self).__init__()

        # Create the image
        self.image = pygame.Surface((width, 96))
        self.image.fill((60, 60, 60))

        # Create the bounding rectangle
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0

        # Create the tab that shows/hides the toolbar
        self.tabDown = pygame.image.load("./rsc/toolbar_tab_down.png")
        self.tabUp = pygame.image.load("./rsc/toolbar_tab_up.png")
        self.tabRect = self.tabDown.get_rect()
        self.tabRect.centerx = width / 2
        self.tabRect.top = self.rect.bottom

        # Create side buttons
        self.buttons = pygame.sprite.Group()
        Button.containers = self.buttons
        Button("quit", 0, 0, default = pygame.image.load("./rsc/quit_icon.png"))
        Button("save", 32, 0, default = pygame.image.load("./rsc/save_icon_32px.png"))

        # Create toolbox buttons
        self.toolboxList = []
        
        box1 = pygame.image.load("./rsc/toolbar_tool_unselected.png")
        box2 = pygame.image.load("./rsc/toolbar_tool_selected.png")

        # Player spawn tool
        img1, img2 = box1.copy(), box2.copy()
        icon = pygame.image.load("./rsc/jing_32px.png")
        img1.blit(icon, (8, 8))
        img2.blit(icon, (8, 8))
        self.toolboxList.append(Button("player", 96, 24, default = img1, selected = img2))

        # Platform tool
        img1, img2 = box1.copy(), box2.copy()
        icon = pygame.Surface((32, 32))
        icon.fill((247, 145, 25))
        pygame.draw.line(icon, (0, 0, 0), (0, 0), (32, 0), 1)
        pygame.draw.line(icon, (0, 0, 0), (0, 0), (0, 32), 1)
        pygame.draw.line(icon, (0, 0, 0), (0, 30), (32, 30), 2)
        pygame.draw.line(icon, (0, 0, 0), (30, 0), (30, 32), 2)
        img1.blit(icon, (8, 8))
        img2.blit(icon, (8, 8))
        self.toolboxList.append(Button("platform", 168, 24, default = img1, selected = img2))

        # Shrek tool
        img1, img2 = box1.copy(), box2.copy()
        icon = pygame.image.load("./rsc/shrek_32px.png")
        img1.blit(icon, (8, 8))
        img2.blit(icon, (8, 8))
        self.toolboxList.append(Button("enemy", 240, 24, default = img1, selected = img2))

        # Dat Boi tool
        img1, img2 = box1.copy(), box2.copy()
        icon = pygame.image.load("./rsc/datboi_icon.png")
        img1.blit(icon, (8, 8))
        img2.blit(icon, (8, 8))
        self.toolboxList.append(Button("datboi", 312, 24, default = img1, selected = img2))
        
        self.buttons.draw(self.image)

        # Create attributes
        self.currentTool = None
        self.setTool("platform")
        self.collapsed = False
        

    def draw(self, surface):

        if not self.collapsed:
            surface.blit(self.image, (0, 0))
            surface.blit(self.tabUp, (self.tabRect.left, self.rect.height))
        else:
            surface.blit(self.tabDown, (self.tabRect.left, 0))

    def handleMouse(self, mouse, mousebutton):

        # Mouse is within the toolbar
        if not self.collapsed and mouse[1] <= self.rect.bottom:

            for button in self.buttons:
                if button.checkClickOnButton(mouse):
                    if button in self.toolboxList:
                        self.setTool(button.getName())
                    return button.getName()
            return "no button"

        # Mouse is within the tab
        elif self.tabRect.top <= mouse[1] <= self.tabRect.bottom and self.tabRect.left <= mouse[0] <= self.tabRect.right:
            self.toggle()
            return "tab"

        # Mouse is not within the toolbar
        else:
            return "none"

    def toggle(self):

        self.collapsed = not self.collapsed
        if self.collapsed:
            self.tabRect.top = 0
        else:
            self.tabRect.top = self.rect.bottom

    def setTool(self, tool):

        # Deselect the old tool
        for button in self.toolboxList:
            if self.currentTool == button.getName():
                button.setState("default")
                self.image.blit(button.image, (button.rect.left, button.rect.top))
                break

        # Select the new tool
        self.currentTool = tool
        for button in self.toolboxList:
            if self.currentTool == button.getName():
                button.setState("selected")
                self.image.blit(button.image, (button.rect.left, button.rect.top))
                break

    def getTool(self):
        return self.currentTool

