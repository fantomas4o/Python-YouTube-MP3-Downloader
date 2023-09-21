import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube
import os

destination_variable = None

def download_mp3(url, destination='.', quality='best'):
    global destination_variable
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        destination_folder = destination_variable.get() if isinstance(destination_variable, tk.StringVar) else destination_variable
        audio_stream.download(output_path=destination_folder)
        base, ext = os.path.splitext(audio_stream.title)
        new_file = os.path.join(destination_folder, base + '.mp3')
        os.rename(os.path.join(destination_folder, audio_stream.default_filename), new_file)
        messagebox.showinfo("Download Completed", "The file was successfully downloaded and renamed to MP3 format.")
        return new_file
    except Exception as e:
        messagebox.showerror("Error", f"Error while downloading: {str(e)}")
        return None

def choose_destination():
    global destination_variable
    chosen_folder = filedialog.askdirectory()
    destination_variable.set(chosen_folder)

def paste_url(root):
    clipboard_text = root.clipboard_get()
    url_entry.delete(0, tk.END)
    url_entry.insert(0, clipboard_text)

def main():
    global destination_variable
    global url_entry
    root = tk.Tk()
    root.title("Download MP3 Files")
    root.geometry("500x250")

    url_label = tk.Label(root, text="URL:")
    url_label.pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.pack()

    paste_button = tk.Button(root, text="Paste URL", command=lambda: paste_url(root))
    paste_button.pack()

    destination_label = tk.Label(root, text="Destination:")
    destination_label.pack()
    destination_variable = tk.StringVar(root, value=os.getcwd())
    destination_entry = tk.Entry(root, textvariable=destination_variable)
    destination_entry.pack()
    destination_button = tk.Button(root, text="Select Folder", command=choose_destination)
    destination_button.pack()

    quality_label = tk.Label(root, text="Select Audio Quality:")
    quality_label.pack()
    quality_options = ['best', 'high', 'medium', 'low']
    quality_variable = tk.StringVar(root)
    quality_variable.set(quality_options[0])
    quality_menu = tk.OptionMenu(root, quality_variable, *quality_options)
    quality_menu.pack()

    download_button = tk.Button(root, text="Download", command=lambda: download_mp3(url_entry.get(), destination_variable, quality_variable.get()))
    download_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
