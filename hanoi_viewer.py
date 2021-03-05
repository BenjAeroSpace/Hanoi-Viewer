"""
Script By Benj


This script allow you to see how to solve the famous Hanoï towers problem or by an autmoatic display of each steps, 
by manual control via two buttons. The script also allow to see the number of moves, reset the process etc

If you don't know what's the Hanoï towers, here is a small explanation.

The goal is to move all the rings from the left to the right, but you can only move rings one by one
and you can't place a ring onto a smaller one !

Note that the script might be updtated in the futur, don't hesitate to often check the github page !
"""
# coding: utf-8
#importing libs
import datetime
import sys

try:
    import pygame
    # try to import pygame, this allow to prevent any crash if pygame is missing
except:
    print("Uh Oh, it seems that pygame is not detected on you computer, install pygame and try again")
    input("press any key to exit...")
    sys.exit()
    # If pygame is missing, inform the user then quit the program


def rings_number_request():
    """
    Function to request the number of rings
    """
    rings_number = -1
    while rings_number <= 0 or rings_number >= 12:
        # while the number of rings is not correct, request
        try:
            pass
            rings_number = int(input("Enter number of rings (0 < x < 12): "))
            # try to int the number
        except:
            print("Please enter a whole number.")
            # if not a number, say to the user that the input is not correct
    print("Depending of the number of rings selected, the calculation of the moves may take some times")
    return rings_number


class Hanoi():
    def __init__(self, rings):
        """
        Class containing all the informations to solve the Hanoï towers
        """
        self.left_rod = {"id": 1, "coord": 197, "content": [i for i in range(1, rings+1)]}
        self.center_rod = {"id": 2, "coord": 397, "content": []}
        self.right_rod = {"id": 3, "coord": 597, "content": []}
        # Here are the rods, in the first position
        self.moves = []
        # We store all the move done into a list to diplay them after, the calculation of the solution is made before
        # the display of it
        self.step_index = 0
        # use this index to show the moves


    def hanoi(self, n, init, final, tmp):
        """
        Hanoï function solve the hanoï towers by moving elements from a list to another, each list representing a rod
        """
        if n > 1:
            self.hanoi(n-1, init, tmp, final)
            ring_to_move = init["content"][-1]
            # get the last ring from the rod (last element of the list)
            final["content"].append(ring_to_move)
            init["content"].remove(ring_to_move)
            # move from init["id"] to final["id"], or in other words, ring from the initial to the final rod
            self.moves.append([init["id"], final["id"]])
            # append the move to the moves list
            self.hanoi(n-1, tmp, final, init)
        else:
            ring_to_move = init["content"][-1]
            # get the last ring from the rod (last element of the list)
            final["content"].append(ring_to_move)
            init["content"].remove(ring_to_move)
            # move from init["id"] to final["id"], or in other words, ring from the initial to the final rod
            self.moves.append([init["id"], final["id"]])
            # append the move to the moves list


class PygameSetup():
    def __init__(self, rings):
        """
        Class containing all stuff used to make the pygame window working
        """
        self.blue = pygame.Color("blue")
        self.red = pygame.Color("red")
        self.green = pygame.Color("green")
        self.purple = pygame.Color("purple")
        self.white = pygame.Color("white")
        self.grey = pygame.Color(50, 50, 50)
        self.pink = pygame.Color(210, 0, 255)
        # pygame colors
        self.arial40 = pygame.font.SysFont("arial",40)
        self.arial30 = pygame.font.SysFont("arial",30)
        self.arial20 = pygame.font.SysFont("arial",20)
        # Pygame fonts
        self.screen_size = (800,400)
        # it's in the variable name
        self.first_run = True
        # to draw the initial interface or not
        self.rings = rings
        # init class viriable with the ring provided
        self.widh_dif = 190//self.rings
        # init the size difference between each ring
        self.play = False
        self.left = {"id": 1, "coord": 197, "content": [i for i in range(1, rings+1)]}
        self.center = {"id": 2, "coord": 397, "content": []}
        self.right = {"id": 3, "coord": 597, "content": []}
        self.rods = [self.left, self.center, self.right]
        # create another set of rings to display the moves,
        # this avoid number of issues by using the rods contained in the Hanoï class


    def buttons_drawing(self):
        """
        Function to draw the buttons
        """
        if self.play:
            # if the auto-player is ON
            pygame.draw.rect(screen, self.purple, pygame.Rect(420, 320, 100, 50))
            screen.blit(self.arial30.render("PAUSE", True, self.white), (430,327))
            pygame.draw.rect(screen, self.green, pygame.Rect(280, 320, 107, 50))
            screen.blit(self.arial30.render("PLAYING", True, self.white), (281,327))
        else:
            # if it is paused
            pygame.draw.rect(screen, self.red, pygame.Rect(420, 320, 100, 50))
            screen.blit(self.arial30.render("PAUSED", True, self.white), (421,327))
            pygame.draw.rect(screen, self.purple, pygame.Rect(280, 320, 107, 50))
            screen.blit(self.arial30.render("PLAY", True, self.white), (302,327))
        # constant buttons that does not change depending of the playing status
        pygame.draw.rect(screen, self.purple, pygame.Rect(550, 320, 150, 50))
        screen.blit(self.arial30.render("NEXT MOVE", True, self.white), (552,327))
        pygame.draw.rect(screen, self.purple, pygame.Rect(100, 320, 152, 50))
        screen.blit(self.arial30.render("PREV. MOVE", True, self.white), (101,327))
        pygame.draw.rect(screen, self.purple, pygame.Rect(10, 60, 40, 144))
        pos = 62
        for letter in "RESET":
            screen.blit(self.arial30.render(letter, True, self.white), (20,pos))
            pos+=26


    def base_window(self):
        """
        draw the base of the interface
        """
        screen.fill(self.grey)
        # fill the screen with grey to erase ANYTHING
        pygame.draw.rect(screen, self.red, pygame.Rect(103, 300, 600, 10))
        pygame.draw.rect(screen, self.red, pygame.Rect(197, 50, 6, 250))
        pygame.draw.rect(screen, self.red, pygame.Rect(397, 50, 6, 250))
        pygame.draw.rect(screen, self.red, pygame.Rect(597, 50, 6, 250))
        # draw the base and the rods
        screen.blit(self.arial40.render("1", True, self.red), (190,5))
        screen.blit(self.arial40.render("2", True, self.red), (390,5))
        screen.blit(self.arial40.render("3", True, self.red), (590,5))
        screen.blit(self.arial40.render("3", True, self.red), (590,5))
        # name the beautiful rods
        self.buttons_drawing()
        # call the function to show the buttons


    def rings_drawing(self):
        """
        Function that display the rings and manage the rings in the lists,
        the function also manage the step_index value to avoid optimisations issues.
        """
        try:
            # all the function is contained in a try/except to avoid any index errors
            move = hn.moves[hn.step_index]
            # get the move in the moves list, this is a tuple 
            for rod_init in self.rods:
                if rod_init["id"] == move[0]:
                    for rod_final in self.rods:
                        if rod_final["id"] == move[1]:
                            # find the initial rod and final rod (lists)
                            ring_to_move = rod_init["content"][-1]
                            # get the ring to move
                            rod_final["content"].append(ring_to_move)
                            # add it to the final list
                            rod_init["content"].remove(ring_to_move)
                            # remove it from the initial list
                            self.base_window()
                            screen.blit(ps.arial20.render(f"MOVE: {hn.step_index+1} / {len(hn.moves)}", True, self.red), (5,5))
                            screen.blit(ps.arial20.render(f"FROM {move[0]} TO {move[1]}", True, self.red), (5,30))
                            # draw the base of the window and write the number of moves and the current one
                            for rod in self.rods:
                                # draw rings for each rod
                                ring_y = 278
                                for ring_size in rod["content"]:
                                    ring_widh = 190 - self.widh_dif*(ring_size-1)
                                    ring_height = 20
                                    ring_x = rod["coord"] - ((ring_widh//2) - 3)
                                    pygame.draw.rect(screen, self.blue, pygame.Rect(ring_x, ring_y, ring_widh, ring_height))
                                    ring_y -= 22
            pygame.display.flip()
            # display
            hn.step_index += 1
            # add 1 to the step_index here to avoid bugs where the script by pass some display of rings moves
            # causing a complete mess in the result
        except IndexError:
            pass
            # if there is an index error, just pass, do nothing

    
    def rings_drawing_rev(self):
        """
        Function to move the ring but in reverse, designed for the prev. move button
        Note that despite the fact that the function is almost the same than the rings_drawing one, it is separated
        to avoid bugs where the script by pass some display of rings moves causing a complete mess in the result
        """
        try:
            # to understand the function, refer the coments in the previous fuction
            move = hn.moves[hn.step_index]
            for rod_init in self.rods:
                if rod_init["id"] == move[1]:
                    for rod_final in self.rods:
                        if rod_final["id"] == move[0]:
                            # the only change in the function is that the initial and final lists are inverted
                            ring_to_move = rod_init["content"][-1]
                            rod_final["content"].append(ring_to_move)
                            rod_init["content"].remove(ring_to_move)
                            self.base_window()
                            screen.blit(ps.arial20.render(f"MOVE: {hn.step_index+1} / {len(hn.moves)}", True, self.red), (5,5))
                            screen.blit(ps.arial20.render(f"FROM {move[1]} TO {move[0]}", True, self.red), (5,30))
                            for rod in self.rods:
                                ring_y = 278
                                for ring_size in rod["content"]:
                                    ring_widh = 190 - self.widh_dif*(ring_size-1)
                                    ring_height = 20
                                    ring_x = rod["coord"] - ((ring_widh//2) - 3)
                                    pygame.draw.rect(screen, self.blue, pygame.Rect(ring_x, ring_y, ring_widh, ring_height))
                                    ring_y -= 22
                                    pygame.display.flip()
        except IndexError:
            pass


    def first_drawing(self):
        """
        The function that draw the rods and the rings the first time
        """
        self.base_window()
        # call the base_window function defined previously in the class
        ring_y = 278
        for ring_size in self.left["content"]:
            ring_widh = self.left["coord"] - self.widh_dif*(ring_size-1)
            ring_height = 20
            ring_x = 197 - ((ring_widh//2) - 3)
            pygame.draw.rect(screen, ps.blue, pygame.Rect(ring_x, ring_y, ring_widh, ring_height))
            screen.blit(ps.arial20.render(f"MOVE: {hn.step_index+1} / {len(hn.moves)}", True, ps.red), (5,5))
            ring_y -= 22
            # draw the rings in their initial position
        pygame.display.flip()


pygame.init()
#init the pygame module
rings = rings_number_request()
# request the number of rings
ps = PygameSetup(rings)
hn = Hanoi(rings)
# init class

steps_number = {1:1, 2:3, 4:15, 5:31, 6:63, 7:127, 8:255, 9:511, 10:1023, 11:2047}
# defining dic with all the number steps for each number of rings to show you a stunning loading bar thx to the progress lib
hn.hanoi(rings, hn.left_rod, hn.right_rod, hn.center_rod)
# calculating the moves

now = datetime.datetime.now()
second = now.second
# init the second value for the first time

pygame.display.init()
# Pygame init
screen = pygame.display.set_mode(ps.screen_size)
pygame.display.set_caption("Hanoï Viewer")
# screen init

launched = True
# pygame work in a while loop
while launched:
    if ps.first_run:
        # if this is the first run (when the script is launched or the reset button is pressed)
        ps.first_drawing()
        ps.first_run = False
        
    now = datetime.datetime.now()
    if second != now.second:
        # using the datetime second to slow down the display in the automatic player.
        if ps.play:
            ps.rings_drawing()
        second = now.second

    for event in pygame.event.get():
        # for event get any event, like a clic in an aera of the window
        if event.type == pygame.QUIT:
            launched = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if the mouse button is down: so the user clicked somewhere, this return a tuple like this:
            # (x_position, y_position)
            # checking the position to see if this is on a button
            if (280<event.pos[0]<380) and (320<event.pos[1]<370):
                # PLAY button
                ps.play = True
                ps.buttons_drawing()
                pygame.display.flip()
            elif (420<event.pos[0]<520) and (320<event.pos[1]<370):
                # PAUSE button
                ps.play = False
                ps.buttons_drawing()
                pygame.display.flip()
            elif (550<event.pos[0]<700) and (320<event.pos[1]<370):
                # NEXT MOVE
                ps.rings_drawing()
            elif (100<event.pos[0]<250) and (320<event.pos[1]<370):
                # PREV. button
                if hn.step_index-1 >= 0:
                    hn.step_index -= 1
                ps.rings_drawing_rev()
                # reverse the last move
            elif (10<event.pos[0]<50) and (60<event.pos[1]<204):
                # RESET button
                hn.step_index = 0
                # reset the index
                ps.first_run = True
                # set the first run as True
                ps.left["content"] = [i for i in range(1, rings+1)]
                ps.center["content"] = []
                ps.right["content"] = []
                ps.rods = [ps.left, ps.center, ps.right]
                # reset the lists containing the rods
                ps.first_drawing()
                # draw the initial interface
    mouse = pygame.mouse.get_pos()
    # this line get the position of the cursor in real time, in a tuple: 
    # (x_position, y_position)
    # checking the position to see if this is over a button
    # if yes, change the color of the button
    if (100<mouse[0]<250) and (320<mouse[1]<370):
        # PERV. MOVE button
        pygame.draw.rect(screen, ps.pink, pygame.Rect(100, 320, 152, 50))
        screen.blit(ps.arial30.render("PREV. MOVE", True, ps.white), (101,327))
        pygame.display.flip()
    elif (280<mouse[0]<380) and (320<mouse[1]<370) and not(ps.play):
        # PLAY button
        pygame.draw.rect(screen, ps.pink, pygame.Rect(280, 320, 107, 50))
        screen.blit(ps.arial30.render("PLAY", True, ps.white), (302,327))
        pygame.display.flip()
    elif (420<mouse[0]<520) and (320<mouse[1]<370) and ps.play:
        # PAUSE button
        pygame.draw.rect(screen, ps.pink, pygame.Rect(420, 320, 100, 50))
        screen.blit(ps.arial30.render("PAUSE", True, ps.white), (430,327))
        pygame.display.flip()
    elif (550<mouse[0]<700) and (320<mouse[1]<370):
        # NEXT MOVE button
        pygame.draw.rect(screen, ps.pink, pygame.Rect(550, 320, 150, 50))
        screen.blit(ps.arial30.render("NEXT MOVE", True, ps.white), (552,327))
        pygame.display.flip()
    elif (10<mouse[0]<50) and (60<mouse[1]<204):
        # RESET button
        pygame.draw.rect(screen, ps.pink, pygame.Rect(10, 60, 40, 144))
        pos = 62
        for letter in "RESET":
            screen.blit(ps.arial30.render(letter, True, ps.white), (20,pos))
            pos+=26
        pygame.display.flip()
    else:
        # else, draw the 'normal' buttons
        ps.buttons_drawing()
        pygame.display.flip()
