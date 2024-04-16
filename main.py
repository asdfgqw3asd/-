import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Функция для добавления записи об активности
def add_activity():
    room = room_entry.get()
    activity = activity_entry.get()
    if room and activity:
        try:
            conn = sqlite3.connect('activity.db')
            c = conn.cursor()
            c.execute('INSERT INTO activity (room, activity) VALUES (?, ?)', (room, activity))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успешно", "Запись добавлена!")
            update_activity_list()
            room_entry.delete(0, tk.END)
            activity_entry.delete(0, tk.END)
        except sqlite3.Error as error:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {error}")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля!")

# Функция для просмотра активности в аудиториях
def view_activity():
    update_activity_list()

# Функция для удаления активности
def delete_activity():
    selected_item = activity_list.selection()
    if selected_item:
        activity_id = activity_list.item(selected_item)['values'][0]
        try:
            conn = sqlite3.connect('activity.db')
            c = conn.cursor()
            c.execute('DELETE FROM activity WHERE id = ?', (activity_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успешно", "Запись удалена!")
            update_activity_list()
        except sqlite3.Error as error:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {error}")
    else:
        messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись для удаления!")

# Функция для обновления списка активностей
def update_activity_list():
    activity_list.delete(*activity_list.get_children())
    try:
        conn = sqlite3.connect('activity.db')
        c = conn.cursor()
        c.execute('SELECT * FROM activity')
        rows = c.fetchall()
        conn.close()
        for row in rows:
            activity_list.insert('', 'end', values=row)
    except sqlite3.Error as error:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {error}")

# Создание базы данных SQLite, если её нет
def create_database():
    try:
        conn = sqlite3.connect('activity.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS activity
                     (id INTEGER PRIMARY KEY, room TEXT, activity TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {error}")

# Создание GUI
root = tk.Tk()
root.title("Учёт активности в аудиториях")

# Создание виджетов
room_label = tk.Label(root, text="Аудитория:")
room_entry = tk.Entry(root)
activity_label = tk.Label(root, text="Активность:")
activity_entry = tk.Entry(root)
add_button = tk.Button(root, text="Добавить запись", command=add_activity)
delete_button = tk.Button(root, text="Удалить запись", command=delete_activity)
view_button = tk.Button(root, text="Просмотреть активность", command=view_activity)
activity_list = ttk.Treeview(root, columns=('ID', 'Аудитория', 'Активность'), show='headings')
activity_list.heading('ID', text='ID')
activity_list.heading('Аудитория', text='Аудитория')
activity_list.heading('Активность', text='Активность')

# Размещение виджетов
room_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
room_entry.grid(row=0, column=1, padx=5, pady=5)
activity_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
activity_entry.grid(row=1, column=1, padx=5, pady=5)
add_button.grid(row=2, column=0, padx=5, pady=5, sticky="WE")
delete_button.grid(row=2, column=1, padx=5, pady=5, sticky="WE")
view_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="WE")
activity_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Создание базы данных, если её нет
create_database()

# Обновление списка при запуске приложения
update_activity_list()

# Запуск основного цикла приложения
root.mainloop()
