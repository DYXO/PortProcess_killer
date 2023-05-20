import os
import psutil
import PySimpleGUI as sg

layout = [
    [sg.Text("On which port should the process be killed?", justification='center')],
    [sg.Input(key="-PORT-", size=(15, 1), justification='center')],
    [sg.Button('Kill', key="-KILL-", size=(15, 1), pad=((75, 75), 0))],
    [sg.Output(size=(25, 10), key="-OUTPUT-", pad=((10, 10), (0, 10)))]
]

window = sg.Window('Port Killer', layout, size=(300, 200), element_justification='center')

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "-KILL-":
        port = values["-PORT-"]
        if port:
            processes = psutil.process_iter()
            process_found = False

            for process in processes:
                try:
                    process_connections = process.connections()
                    for connection in process_connections:
                        if connection.laddr.port == int(port) and connection.status == 'LISTEN':
                            process_pid = process.pid
                            print(f"Process running on port {port} has PID: {process_pid}")
                            os.system(f'taskkill /PID {process_pid} /F')
                            process_found = True
                            break
                except psutil.AccessDenied:
                    pass

            if not process_found:
                print(f"No process found running on port {port}.")
        else:
            print("Please enter a port number.")

window.close()