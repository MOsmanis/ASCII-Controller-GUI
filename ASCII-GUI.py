from inputs import get_gamepad
import subprocess
import curses
from pyfiglet import figlet_format

class DesignConfig():
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        if 'font' in kwargs:
            self.font = kwargs.get('font')
        else:
            self.font = 'starwars'
        if 'message' in keys:
            self.message = kwargs.get('message')
        else:
            self.message = 'welcome'
            
class CursesController():
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        if 'config' in keys:
            self.config = kwargs.get('config')
        else:
            self.config = DesignConfig()
        if 'button_names' in keys:
            self.button_names = kwargs.get('button_names')
        else:
            self.button_names = [""]
    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        curses.curs_set(False)
        #Create Pad with button names
        #CHANGE THE HEIGHT (5)
        names_template = ""
        self.button_widths = []
        i = 0
        formatted_name = ""
        for button in self.button_names:
           formatted_name = figlet_format(button, font=self.config.font)
           names_template = names_template + formatted_name
           self.button_widths.append(len(formatted_name.split('\n')[0]))
        self.button_height = len(formatted_name.split('\n')) -1 #dont count the line that comes after last endline symbol
        print(self.button_height)
        self.button_max_width = max(self.button_widths)
        self.button_pad = curses.newpad(5*len(self.button_names), self.button_max_width + 1)
        self.button_pad.addstr(0, 0, names_template)
        print(names_template)
        self.button_y = int((curses.LINES - 1) / 2) - int(self.button_height/2)
        self.middle_of_screen = int((curses.COLS - 1) / 2)
        print("button y =" + str(self.button_y))

        self.stdscr.border()
        self.stdscr.refresh()
        self.button_pad.refresh(0,0 , self.button_y, self.middle_of_screen - int(self.button_widths[0]/2) , self.button_y + self.button_height-1, self.middle_of_screen + int(self.button_widths[0] / 2))

    def write(self, index):
        self.stdscr.erase()
        self.stdscr.border()
        self.stdscr.refresh()
        self.button_pad.refresh(index * self.button_height, 0, self.button_y, self.middle_of_screen - int(self.button_widths[index] / 2),
                                self.button_y + self.button_height-1, self.middle_of_screen + int(self.button_widths[index] / 2))
    def writeWelcomeMessage(self):
        self.selected.clear()
        self.selected.addstr(0,0,figlet_format(self.config.message, font=self.config.font))
    def closeCurses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    

def menu():
    def retropie():
        subprocess.call(['emulationstation'])
    def steamlink():
        subprocess.call(['steamlink'])
    def desktop():
        subprocess.call(['startx'])
    def shutdown():
        subprocess.call(['shutdown','-h','now'])
    def restart():
        subprocess.call(['shutdown','-r','now'])
        
    active_button=0;

    buttons = []
    buttons.append(['RetroPie',retropie])
    buttons.append(['Steam Link',steamlink])
    buttons.append(['Desktop',desktop])
    buttons.append(['Shut Down',shutdown])
    buttons.append(['Restart',restart])
    button_names = [i[0] for i in buttons]
    config = DesignConfig(font='cyberlarge')
    curses_controller = CursesController(config=config, button_names=button_names)
    curses_controller.initCurses()

    while 1:

        events = get_gamepad()
        for event in events:
            if event.code=='ABS_HAT0Y':
                if event.state==-1:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(active_button)
                elif event.state==1:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(active_button)
            elif event.code=='ABS_Y' and event.device.name=='usb gamepad':
                if event.state==0:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(active_button)
                elif event.state==255:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(active_button)
            elif event.code=='ABS_Y' and event.device.name=='Microsoft X-Box 360 pad':
                if event.state<=-32000:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(active_button)
                elif event.state>32000:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(active_button)
            elif event.code=='BTN_SOUTH' or event.code=='BTN_THUMB2':
                if event.state==1:
                    buttons[active_button][1]()
                    curses_controller.writeWelcomeMessage()

def main():

    try:
        menu()
    except KeyboardInterrupt:
        #curses_controller.closeCurses()
        exit()
    
if __name__ == '__main__':
    main()
        
