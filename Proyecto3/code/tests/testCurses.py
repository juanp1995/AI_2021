# from time import sleep
# import curses, curses.panel

# def make_panel(h,l, y,x, str):
#     win = curses.newwin(h,l, y,x)
#     win.erase()
#     win.box()
#     win.addstr(2, 2, str)

#     panel = curses.panel.new_panel(win)
#     return win, panel

# def test(stdscr):
#     try:
#         curses.curs_set(0)
#     except:
#         pass
#     stdscr.box()
#     stdscr.addstr(2, 2, "panels everywhere")
#     win1, panel1 = make_panel(10,20, 5,5, "Panel 1")
#     win2, panel2 = make_panel(10,12, 8,8, "Panel 2")
#     curses.panel.update_panels(); stdscr.refresh()
#     sleep(1)

#     panel1.top(); curses.panel.update_panels(); stdscr.refresh()
#     sleep(1)

#     for i in range(20):
#         panel2.move(8, 8+i)
#         curses.panel.update_panels(); stdscr.refresh()
#         sleep(0.1)

#     sleep(1)

# if __name__ == '__main__':
#     curses.wrapper(test)





import sys, os, json, time, datetime, math, curses, threading

COUNTER = 0

def my_raw_input(window, r, c, prompt_string):
    curses.echo()
    window.addstr(r, c, prompt_string)
    window.refresh()
    input = window.getch(7,2)
    return input

def count(window):
    global COUNTER
    while True:
        window.addstr(3, 0, '%d'%(COUNTER))
        if COUNTER >= 1000:
            COUNTER = 0
        COUNTER += 1
        window.refresh()

def main(args):
    # create stdscr
    stdscr = curses.initscr()
    stdscr.nodelay(1)
    stdscr.clear()

    # allow echo, set colors
    curses.echo()
    curses.start_color()
    curses.use_default_colors()

    # define 2 windows
    command_window = curses.newwin(3, 30, 0, 0)
    display_window = curses.newwin(6, 30, 5, 0)
    command_window.border()
    display_window.border()

    # thread to refresh display_window
    x = threading.Thread(target=count, args=(display_window,))
    x.start()

    # main thread, waiting for user's command.
    while True:
        command = my_raw_input(command_window, 0, 0, 'Enter your command :')
        if command == 'q':
            break
        else:
            command_window.addstr(1, 0, "command")

    x.join()
    curses.endwin()

curses.wrapper(main)