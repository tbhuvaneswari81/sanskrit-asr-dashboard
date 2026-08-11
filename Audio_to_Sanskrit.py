import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import threading

# Load Whisper model once
status_text = "Loading Whisper model..."
model = whisper.load_model("large-v3")


def browse_file():
    filename = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[
            ("Audio Files", "*.mp3 *.wav *.m4a *.flac")
        ]
    )

    if filename:
        audio_path.set(filename)


def convert_audio():

    file = audio_path.get()

    if file == "":
        messagebox.showerror("Error", "Please select an audio file.")
        return

    status.set("Converting... Please wait.")

    try:

        result = model.transcribe(
            file,
            language="sa",
            fp16=False
        )

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, result["text"])

        status.set("Completed")

    except Exception as e:
        status.set("Error")
        messagebox.showerror("Error", str(e))


def start_conversion():
    threading.Thread(target=convert_audio).start()


def save_text():

    text = text_box.get("1.0", tk.END).strip()

    if text == "":
        messagebox.showwarning("Warning", "Nothing to save.")
        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if filename:

        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        messagebox.showinfo("Saved", "File saved successfully.")


root = tk.Tk()

root.title("Audio to Sanskrit (Devanagari)")
root.geometry("800x600")

audio_path = tk.StringVar()

status = tk.StringVar()
status.set(status_text)

title = tk.Label(
    root,
    text="Audio to Sanskrit Converter",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

entry = tk.Entry(
    frame,
    textvariable=audio_path,
    width=60
)

entry.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(
    frame,
    text="Browse",
    command=browse_file
)

browse_btn.pack(side=tk.LEFT)

convert_btn = tk.Button(
    root,
    text="Convert",
    font=("Arial", 12),
    command=start_conversion
)

convert_btn.pack(pady=10)

text_box = tk.Text(
    root,
    height=18,
    width=90,
    font=("Mangal", 14)
)

text_box.pack(pady=10)

save_btn = tk.Button(
    root,
    text="Save Text",
    command=save_text
)

save_btn.pack(pady=5)

status_label = tk.Label(
    root,
    textvariable=status,
    fg="blue"
)

status_label.pack()

root.mainloop()