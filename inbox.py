import os
from tkinter import messagebox
import traceback
import socket
import threading
import multiprocessing

def sanitize(filename):
    pattern = r'[<>:"/\\|?*\x00-\x1F]'
    strippedfilename = re.sub(pattern, '', filename)
    if filename.lower in [CON,
                          PRN,
                          AUX,
                          NUL,
                          COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, COM0,
                          LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9, LPT0]:
        raise OSError
    return strippedfilename

def handle_client(clientsocket):
    try:
        clientsocket.send(b"SUBJ:")
        subject = clientsocket.recv(4096).decode().rstrip('\n')
        clientsocket.send(b"CNTT:")
        content = clientsocket.recv(4096).decode().rstrip('\n')
        with open(sanitize(subject) + ".txt", w) as mail:
            mail.write(content)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        clientsocket.close()

def daemon():
    with open(".lock", "w") as f:
        f.write(str(os.getpid()))
    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('0.0.0.0', 4556))
        serversocket.listen(64)
        while True:
            clientsocket, address = serversocket.accept()
            clientthread = threading.Thread(target=handleclient, args=(clientsocket,))
            clientthread.start()
    except Exception as e:
        os.remove(".lock")
        print("inbox crashed!! not good")
        trace = traceback.format_exc()
        messagebox.showerror("Inbox Daemon has crashed!!", "error traceback: \n"+trace)

if __name__ == "__main__":
    messagebox.showinfo("inbox.py", "starting the inbox.py daemon")
    tinbox = multiprocessing.Process(target=daemon)
    tinbox.daemon = True
    tinbox.start()
