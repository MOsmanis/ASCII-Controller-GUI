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
    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        self.stdscr.addstr(0,0,figlet_format(self.config.message, font=self.config.font))
    def write(self, message):
        self.stdscr.clear()
        self.stdscr.addstr(0,0,figlet_format(message, font=self.config.font))
    def writeWelcomeMessage(self):
        self.stdscr.clear()
        self.stdscr.addstr(0,0,figlet_format(self.config.message, font=self.config.font))
    def closeCurses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    

def menu(curses_controller):
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
        
    active_button=-1;

    buttons = []
    buttons.append(['RetroPie',retropie])
    buttons.append(['Steam Link',steamlink])
    buttons.append(['Desktop',desktop])
    buttons.append(['Shut Down',shutdown])
    buttons.append(['Restart',restart])

    
         
    while 1:
        curses_controller.stdscr.refresh()
        events = get_gamepad()
        for event in events:
            if event.code=='ABS_HAT0Y':
                if event.state==-1:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(buttons[active_button][0])
                elif event.state==1:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(buttons[active_button][0])
            elif event.code=='ABS_Y' and event.device.name=='usb gamepad':
                if event.state==0:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(buttons[active_button][0])
                elif event.state==255:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(buttons[active_button][0])
            elif event.code=='ABS_Y' and event.device.name=='Microsoft X-Box 360 pad':
                if event.state<=-32000:
                    last_active = active_button
                    active_button = active_button-1
                    if active_button<0:
                        active_button = len(buttons) -1
                    curses_controller.write(buttons[active_button][0])
                elif event.state>32000:
                    last_active = active_button
                    active_button = active_button+1
                    if active_button>=len(buttons):
                        active_button = 0
                    curses_controller.write(buttons[active_button][0])
            elif event.code=='BTN_SOUTH' or event.code=='BTN_THUMB2':
                if event.state==1:
                    buttons[active_button][1]()
                    curses_controller.writeWelcomeMessage()

def main():
    config = DesignConfig(font='cyberlarge')
    curses_controller = CursesController(config=config)
    curses_controller.initCurses()
    try:
        menu(curses_controller)
    except KeyboardInterrupt:
        curses_controller.closeCurses()
        exit()
    
if __name__ == '__main__':
    main()
        
