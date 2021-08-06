# required modules
import pytube
import tkinter
import os
import requests
import tempfile
import threading
import tkinter.ttk
import tkinter.messagebox
import urllib.error
# window size, title
root = tkinter.Tk()
root.title("YT Downloader by AJR")
root.geometry("540x304")
root.resizable(False, False)
url = tkinter.StringVar()
stream_list = []
# temporary file for window icon
tmpfile = tempfile.mkdtemp()
try:
    logo_url = "https://ajanjairam.github.io/assets/img/ajr_logo.ico"
    r1 = requests.get(logo_url, allow_redirects=True)
    open(tmpfile + "\\ajr.ico", 'wb').write(r1.content)
    root.iconbitmap(tmpfile + "\\ajr.ico")
except requests.exceptions.ConnectionError:
    pass
except Exception as e:
    tkinter.messagebox.showerror("Error", e)


def download_video():
    '''downloading the selected videos'''
    global video
    download_video = video.streams[comboBox1.current()]
    download_video.download()
    button2.config(text="Download")
    label3.config(text="Downloaded: " + video.title)


def download_video_thread():
    '''stop window from freezing'''
    button2.config(text="Downloading")
    threading.Thread(target=download_video).start()


def check_url():
    '''checking for the input url and displaying title'''
    global video
    global tmpfile
    global stream_list
    global button2, label3
    try:
        video = pytube.YouTube(url.get())
        for stream in video.streams:
            sle = (stream.mime_type.capitalize().replace("/", ":") + " " + str(stream.resolution)).replace(" None", "")
            stream_list.append(sle)
    except urllib.error.URLError:
        response1 = tkinter.messagebox.askretrycancel("No connection!", "Please check your internet and try again.")
        if not(response1):
            root.destroy()
    except pytube.exceptions.VideoUnavailable:
        tkinter.messagebox.showerror("Video Error", "Video unavailable or private.")
    except pytube.exceptions.RegexMatchError:
        tkinter.messagebox.showwarning("Link Error", "Please type or paste a YouTube link.")
    else:
        comboBox1["values"] = tuple(stream_list)
        comboBox1.current(0)
        button2 = tkinter.Button(root, text="Download", command=download_video_thread)
        button1.config(text="Check")
        label3 = tkinter.Label(root, text="Video: " + video.title, wraplength=500)
        button2.grid(row=1, column=2, padx=(5, 20), pady=20)
        label3.grid(row=2, column=0, columnspan=3, padx=5)


def check_url_thread():
    '''stop window from freezing'''
    button1.config(text="Checking")
    threading.Thread(target=check_url).start()


# tkinter widgets
label1 = tkinter.Label(root, text="Paste Link")
entry1 = tkinter.Entry(root, textvariable=url, width=50)
button1 = tkinter.Button(root, text="Check", command=check_url_thread)
label2 = tkinter.Label(root, text="Available Formats")
comboBox1 = tkinter.ttk.Combobox(root, width=20, state="readonly")
label1.grid(row=0, column=0, padx=(20, 5), pady=(20, 0))
entry1.focus()
entry1.grid(row=0, column=1, pady=(20, 0))
button1.grid(row=0, column=2, padx=(10, 20), pady=(20, 0))
label2.grid(row=1, column=0, padx=(20, 5), pady=20)
comboBox1.grid(row=1, column=1, pady=20)
root.mainloop()
# deleting temporary files
try:
    os.remove(tmpfile + "\\ajr.ico")
    os.rmdir(tmpfile)
except PermissionError:
    pass
except FileNotFoundError:
    pass
