from pytubefix import YouTube
import ttkbootstrap as ttkb
import tkinter as tk
from tkinter import  filedialog
from tkinter import ttk
import threading
import subprocess
import os
import imageio_ffmpeg


filename = r''

def choose_directory():
    global filename
    filename = filedialog.askdirectory()
    return filename


def download():
    def progress_function(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        stringvar.set(f"{int(percentage_of_completion)}%")
        pb['value'] = percentage_of_completion


    def start_download():
        try:
            link = entry.get()
            yt = YouTube(link, on_progress_callback=progress_function)
            if radio_var.get() == 'mp4':


                yd = yt.streams.get_audio_only()
                yd.download(output_path=filename, filename='audio.mp3')
                video = yt.streams.filter(adaptive=True, res="1080p").first()
                video.download(output_path=filename, filename='video.mp4')

                video_path = fr'{filename}\video.mp4'
                audio_path = fr'{filename}\audio.mp3'
                output_path = fr"{filename}\{yt.title}.mp4"

                stringvar.set('Merging Files')

                ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                subprocess.run(
                    [ffmpeg_exe, '-y', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', output_path],
                    check=True, capture_output=True
                )

                os.remove(fr'{filename}\video.mp4')
                os.remove(fr'{filename}\audio.mp3')
            else:
                yd = yt.streams.get_audio_only()
                yd.download(output_path=filename, filename=f'{yt.title}.mp3')
            entry.delete(0,tk.END)
            stringvar.set('Succesfuly Downloaded!')
            root.after(2000, lambda: stringvar.set(''))
            pb['value'] = 0
        except:
            stringvar.set("Error, Pleas check if this is the correct link")
            root.after(3000, lambda: stringvar.set(''))
            pb['value'] = 0

    threading.Thread(target=start_download).start()

root = ttkb.Window(themename='journal')
root.title('YTDownloader')
root.geometry('350x270')

label_dir = ttkb.Label(root,text='Choose directory to save file: ')
label_dir.pack(pady=8)

btn_dir = ttkb.Button(root,text='...',command=choose_directory,padding=3)
btn_dir.place(x=280,y=5)
# btn_dir.pack(side='top', anchor='e')

radio_var = ttkb.StringVar(value='mp4')
radiobtn1 = ttkb.Radiobutton(root, text='mp3', variable=radio_var, value='mp3')
radiobtn1.pack(pady = 10)
radiobtn2 = ttkb.Radiobutton(root, text='mp4', variable=radio_var, value='mp4')
radiobtn2.pack(pady = 5)

label = ttkb.Label(root, text='Entery link to a video: ')
label.pack(pady = 5)
entry = ttkb.Entry(root)
entry.pack()

btn = ttkb.Button(root, text='Download', command=download)
btn.pack(pady = 5)

stringvar = tk.StringVar()
label2 = tk.Label(root,textvariable=stringvar)
label2.pack()

pb = ttk.Progressbar(root)
pb.pack()

root.mainloop()
