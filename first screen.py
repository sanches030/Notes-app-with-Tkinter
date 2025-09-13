from tkinter import *
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import simpledialog
from datetime import datetime
import ctypes
from tkinter import messagebox
import threading
import time
import customtkinter
import sqlite3
from db_notes import init_db

init_db()
root = Tk()
root.configure(bg="grey")
root.title("Alarm Notes")
root.geometry("600x600")
label = tk.Label(background="grey")

color_var = StringVar(value="Обери тип нотатки")

color_options = ["Обери тип нотатки", "Жовтий", "Зелений", "Червоний", "Синій"]
color_menu = tk.OptionMenu(root, color_var, color_var.get(), *color_options)
color_menu.pack()
color_menu.place(x=100, y=70)


# Поле для ввода нотатки
textbox = tk.Text(height=15, width=50)
textbox.place(x=100, y=100)



# Вибрати тип нотатки(колір)
def save_note():
    text = textbox.get("1.0", "end-1c").strip()
    color = color_var.get()

    if not text:
        messagebox.showwarning("Попередження", "Текст замітки порожній!")
        return
    
    if color == "Обери тип нотатки":
        messagebox.showwarning("Попередження", "Оберіть тип (колір) замітки!")
        return

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("INSERT INTO notes (text, color) VALUES (?, ?)", (text, color))
    conn.commit()
    conn.close()

    messagebox.showinfo("OK", "Замітка збережена!")


#Встановити нагадування
def reminder(time_rem, msg):
    try:
        local_time = float(time_rem) * 60
    except ValueError:
        messagebox.showerror("Error", "Будь ласка, введіть число для часу.")
        return
    time.sleep(local_time)
    messagebox.showinfo(title=None, message=msg)

def another_thread():
    time_rem = simpledialog.askstring("Час", "Введіть час у хвилинах:")
    if time_rem is None:
        return
    
    msg = textbox.get("1.0", "end-1c").strip()

    if not msg:
        messagebox.showwarning("Попередження", "Поле нотатки порожнє!")
        return
    
    r = threading.Thread(target=reminder, args=(time_rem, msg))
    r.start()

button_rem = customtkinter.CTkButton(root, text="Встановити нагадування", command=another_thread)
button_rem.grid(row=4, column=0, padx=100, pady=350)

button_save = customtkinter.CTkButton(root, text="Зберегти", command=save_note)
button_save.place(x=365, y=350)

def create_note_window(parent):
    note_win = tk.Toplevel(parent)
    note_win.geometry("600x600")
    note_win.title("Нова нотатка")
    note_win.configure(bg="gray")

    # Frame з білим фоном
    frame = tk.Frame(note_win, width=500, height=400, bg="white", highlightthickness=1, highlightbackground="black")
    frame.place(relx=0.5, rely=0.4, anchor="center")

    # Текстове поле
    textbox = tk.Text(
        frame,
        width=50,
        height=15,
        wrap="word",
        bd=0,
        bg="white",
        fg="black",
        insertbackground="black"
    )
    textbox.pack(padx=10, pady=10, fill="both", expand=True)

    # Теги для стилю
    textbox.tag_configure("header", font=("Arial", 18, "bold"), justify="center")
    textbox.tag_configure("normal", font=("Arial", 15), justify="left")

    def on_key_release(event):
        text = textbox.get("1.0", "end-1c")
        lines = text.split("\n")
        textbox.tag_remove("header", "1.0", "end")
        textbox.tag_remove("normal", "1.0", "end")
        if lines:
            textbox.tag_add("header", "1.0", "1.end")
            if len(lines) > 1:
                textbox.tag_add("normal", "2.0", "end")

    textbox.bind("<KeyRelease>", on_key_release)

    # Вибір кольору (типу)
    color_var = tk.StringVar(value="Обери тип нотатки")
    color_options = ["Обери тип нотатки", "Жовтий", "Зелений", "Червоний", "Синій"]
    color_menu = tk.OptionMenu(note_win, color_var, *color_options)
    color_menu.place(x=100, y=70)

    # Кнопка збереження
    def save_and_close():
        text = textbox.get("1.0", "end-1c")
        color = color_var.get()
        if not text.strip():
            messagebox.showwarning("Помилка", "Нотатка порожня!")
            return
        if color == "Обери тип нотатки":
            messagebox.showwarning("Помилка", "Оберіть тип нотатки!")
            return
        conn = sqlite3.connect("notes.db")
        c = conn.cursor()
        c.execute("INSERT INTO notes (text, color) VALUES (?, ?)", (text, color))
        conn.commit()
        conn.close()
        messagebox.showinfo("OK", "Нотатку збережено!")
        note_win.destroy()

    save_button = customtkinter.CTkButton(
        note_win,
        text="Зберегти",
        command=save_and_close,
        width=120,
        height=35,
        text_color="white"
    )
    save_button.place(relx=0.5, rely=0.9, anchor="center")


#Список нотаток
def show_notes():
    notes_win = tk.Toplevel(root)
    notes_win.title("Список нотаток")

    color_map = {
        "жовтий": "yellow",
        "червоний": "red",
        "зелений": "green",
        "синій": "blue",
        "білий": "white",
        "фіолетовий": "purple",
        "помаранчевий": "orange",
    }

    #кнопка створення нової нотатки
    new_note_button = customtkinter.CTkButton(
        notes_win,
        text="Створити нову нотатку",
        command=lambda: create_note_window(notes_win),
        width=200,
        height=35,
        fg_color="green",
        text_color="white"
    )
    new_note_button.pack(pady=10)

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, text, color FROM notes")
    for note_id, title, content, color in cursor.fetchall():
        frame = tk.Frame(
            notes_win,
            bg=color_map.get(color.lower(), "white"), 
            bd=2,
            relief="ridge",
            padx=5,
            pady=5
        )
        frame.pack(fill="x", padx=5, pady=5)

        tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg=color_map.get(color.lower(), "white")).pack(anchor="w")
        tk.Label(frame, text=content, font=("Arial", 10), bg=color_map.get(color.lower(), "white")).pack(anchor="w")


        # кнопка видалення для замітки
        btn_del = tk.Button(frame, text="Видалити", command=lambda nid=note_id, f=frame: delete_note(nid, f))
        btn_del.pack(anchor="e", pady=2)
    conn.close()


def delete_note(note_id, frame):
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

    frame.destroy()  

button_show = customtkinter.CTkButton(root, text="Список заміток", command=show_notes)
button_show.place(x=365, y=65)

root.mainloop()