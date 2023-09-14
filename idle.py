#!/usr/bin/python3
import time
import PySimpleGUI as sg

"""
    Demo Program - Multithreaded Long Tasks GUI
    
    Presents one method for running long-running operations in a PySimpleGUI environment.
    
    The PySimpleGUI code, and thus the underlying GUI framework, runs as the primary, main thread
    The "long work" is contained in the thread that is being started.

    So that you don't have to import and understand the threading module, this program uses window.start_thread to run a thread.
    
    The thread is using TUPLES for its keys.  This enables you to easily find the thread events by looking at event[0].
        The Thread Keys look something like this:  ('-THREAD-', message)
        If event [0] == '-THREAD-' then you know it's one of these tuple keys.
         
    Copyright 2022 PySimpleGUI
"""

points = 0
build1 = 0
buildcost1 = 10
build2 = 0
buildcost2 = 100

def long_operation_thread(window):
    """
    A worker thread that communicates with the GUI through a queue
    This thread can block for as long as it wants and the GUI will not be affected
    :param seconds: (int) How long to sleep, the ultimate blocking call
    :param window: (sg.Window) the window to communicate with
    :return:
    """
    global points
    global added
    global build1
    global buildcost1
    global build2
    global buildcost2
    while True:
        added=build1+10*build2
        points+=added
        time.sleep(1)


def the_gui():
    """
    Starts and executes the GUI
    Reads data from a Queue and displays the data to the window
    Returns when the user exits / closes the window
    """
    global points
    global build1
    global buildcost1
    global build2
    global buildcost2

    sg.theme('Light Brown 3')

    layout = [[sg.Text("Epi-points :"),sg.Text('0', key="-POINTS-")],
              [sg.Button("CLICK")],
              [sg.Text("École primaire  |"),sg.Text(buildcost1, key="-TEXT1-")],
              [sg.Text('0', key="-BUILD1-")],
              [sg.Button("Construire une École Primaire")],
              [sg.Text("Collège  |"),sg.Text(buildcost2, key="-TEXT2-")],
              [sg.Text('0', key="-BUILD2-")],
              [sg.Button("Construire un Collège")],
              [sg.Button('Click Me I Do Nothing !'), sg.Button('Exit')],
    ]

    window = sg.Window('Multithreaded Window', layout)

    window.start_thread(lambda: long_operation_thread(window), ('-THREAD-', '-THEAD ENDED-'))
    current_time = 0
    paused = False
    start_time = int(round(time.time() * 100))
    # --------------------- EVENT LOOP ---------------------
    while True:
        # --------- Read and update window --------
        event, values = window.read(timeout=10)
        current_time = int(round(time.time() * 100)) - start_time
        print(event, values, points)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'CLICK':
            points+=1
        if event == 'Construire une École Primaire':          #BUILD1
            if points>=buildcost1:
                build1+=1
                points-=buildcost1
                buildcost1+=build1*2
                window["-TEXT1-"].update(buildcost1)
        if event == 'Construire un Collège':          #BUILD2
            if points>=buildcost2:
                build2+=1
                points-=buildcost2
                buildcost2+=build2*20
                window["-TEXT2-"].update(buildcost2)
        bct1=str(buildcost1)
        #window["-TEXT1-"].update('Building 1 | Cost : ',bct1)
        window["-BUILD1-"].update(build1)
        window["-BUILD2-"].update(build2)
        # --------- Display timer in window --------
        window['-POINTS-'].update(points)


    # if user exits the window, then close the window and exit the GUI func
    window.close()

if __name__ == '__main__':
    the_gui()
    print('Exiting Program')