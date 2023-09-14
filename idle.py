#!/usr/bin/python3
import time
import PySimpleGUI as sg

points=0.0
build1=0
buildcost1=10.0
build2=0
buildcost2=100.0
upgrade1=0.0
upgrcost1=100.0
upgrade2=0.0
upgrcost2=1000.0
added=0.0

def long_operation_thread(window):

    global points
    global added
    global build1
    global buildcost1
    global build2
    global buildcost2
    global upgrade1
    global upgrcost1
    global upgrade2
    global upgrcost2
    pb1=0.0
    pb2=0.0
    while True: #update the epi/sec and the concurrent total of epi
        if upgrade1==1:
            pb1=build1*1.1 
        else:
            pb1=build1
        if upgrade2==1:
            pb2=build2*10*1.1 
        else:
            pb2=build2
        added=pb1+pb2
        points+=added
        time.sleep(1)


def the_gui():

    global points
    global build1
    global buildcost1
    global build2
    global buildcost2
    global upgrade1
    global upgrcost1
    global upgrade2
    global upgrcost2
    global added

    sg.theme('Light Brown 3')

    points_view = [[sg.Text("Epi-points :"),sg.Text('0', key="-POINTS-")],
              [sg.Button("CLICK")],
              [sg.Text("Epi-points/sec :"),sg.Text('0', key="-PERSEC-")],
              [sg.Text("École primaire  |"),sg.Text(buildcost1, key="-TEXT1-")],
              [sg.Text('0', key="-BUILD1-")],
              [sg.Button("Construire une École Primaire")],
              [sg.Text("Collège  |"),sg.Text(buildcost2, key="-TEXT2-")],
              [sg.Text('0', key="-BUILD2-")],
              [sg.Button("Construire un Collège")],
    ]

    upgrades_view = [[sg.Text("Bureaux Primaires +10% |"),sg.Text(upgrcost1, key="-UPG1-")],
              [sg.Button("Acheter des bureaux")],
              [sg.Text("Chaises Collèges +10% |"),sg.Text(upgrcost2, key="-UPG2-")],
              [sg.Button("Acheter des chaises")],
    ]

    layout = [[
        sg.Column(points_view),
        sg.VerticalSeparator(),
        sg.Column(upgrades_view),
        ]
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
        #print(event, values, points)
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
        if event == 'Acheter des bureaux':          #UPGR1
            if points>=upgrcost1 and upgrade1==0:
                upgrade1=1
                points-=upgrcost1
        if event == 'Construire un Collège':          #BUILD2
            if points>=buildcost2:
                build2+=1
                points-=buildcost2
                buildcost2+=build2*20
                window["-TEXT2-"].update(buildcost2)
        if event == 'Acheter des chaises':          #UPGR2
            if points>=upgrcost2 and upgrade2==0:
                upgrade2=1
                points-=upgrcost2
        bct1=str(buildcost1)
        #window["-TEXT1-"].update('Building 1 | Cost : ',bct1)
        window["-BUILD1-"].update(build1)
        window["-BUILD2-"].update(build2)
        # --------- Display timer in window --------
        window['-POINTS-'].update(round(points,2))
        window['-PERSEC-'].update(round(added,2))


    # if user exits the window, then close the window and exit the GUI func
    window.close()

if __name__ == '__main__':
    the_gui()
    print('Exiting Program')