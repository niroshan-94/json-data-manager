import os
import subprocess

from objects.menu_item import MenuItem

class MenuHelper[TReq,TRes]:
    def __init__(self,actions: dict[int, MenuItem[TReq,TRes]], title: str):
        actions[-1] = MenuItem("Back", lambda _: None)  # Add a "Back" option with key -1
        self.actions = actions
        self.title = title
        self.menuViewed = False

    def __print_menu(self):
        """Display the main menu."""
        self.__draw_unicode_box(f"{self.title}", 5)
        for k in [k for k in self.actions if k > 0]:
            print(f"{k:<3}-> {self.actions[k].title:<40}")

    def __try_parse_int(self, value) -> int:
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    def __draw_unicode_box(self, message: str, n: int = 4):
        lines = message.split('\n')
        # Find the longest line to determine the box width
        max_len = max(len(line) for line in lines)   
        print('_' * (max_len + n)) 
        # Content rows
        for line in lines:
            print(f'  {line.ljust(max_len)}  ')
        print(chr(8254) *(max_len + n))

    def __validate_input(self,choice):
        """
        Validate user input for menu choice.
        Returns the integer choice if valid, otherwise returns 0.
        """
        if choice.lower() == 'y':
            self.menuViewed = False  # Reset the menuViewed flag
            return -1  # Special case for viewing menu again
        if choice.lower() in ['cls', 'clear']:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
            self.menuViewed = False  # Reset the menuViewed flag
            return -1  # Special case for clearing screen
        c = self.__try_parse_int(choice)
        return c if c in self.actions else 0

    def view_menu(self) -> MenuHelper[TReq,TRes]:
        w = "Choose an option from menu "
        if(self.menuViewed == False):
            self.__print_menu()
        else:
            w += ". View menu (y)"
        self.menuViewed = True
        choice = input(f"{w}: ").strip()
        choice_int = self.__validate_input(choice)
        return self.actions[choice_int]