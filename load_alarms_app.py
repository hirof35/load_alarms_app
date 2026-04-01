import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
import json
import os

# ファイル名
DATA_FILE = "alarms.json"

pygame.mixer.init()
alarm_list = set()

def load_alarms():
    """ファイルからアラームを読み込む"""
    global alarm_list
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                alarm_list = set(data)
                update_listbox()
        except:
            print("データの読み込みに失敗しました")

def save_alarms():
    """現在のアラームリストをファイルに保存する"""
    with open(DATA_FILE, "w") as f:
        json.dump(list(alarm_list), f)

def play_alarm():
    try:
        pygame.mixer.music.load("Clock-Alarm05-1(Mid).mp3")
        pygame.mixer.music.play(-1)
    except:
        print("音源ファイルを用意してください")

def stop_alarm():
    pygame.mixer.music.stop()
    stop_button.config(state="disabled")

def add_alarm():
    new_time = alarm_entry.get()
    if len(new_time) == 5 and ":" in new_time:
        if new_time not in alarm_list:
            alarm_list.add(new_time)
            save_alarms()  # 追加したら保存
            update_listbox()
            alarm_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "登録済みです")
    else:
        messagebox.showerror("エラー", "HH:MM形式で入力してください")

def delete_alarm():
    selected = listbox.curselection()
    if selected:
        time_to_remove = listbox.get(selected)
        alarm_list.remove(time_to_remove)
        save_alarms()  # 削除したら保存
        update_listbox()

def update_listbox():
    listbox.delete(0, tk.END)
    for t in sorted(list(alarm_list)):
        listbox.insert(tk.END, t)

def update_time():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    
    now_hm = current_time[:5]
    if now_hm in alarm_list and current_time[6:] == "00":
        stop_button.config(state="normal")
        threading.Thread(target=play_alarm, daemon=True).start()
        messagebox.showinfo("アラーム", f"{now_hm} です！")
            
    root.after(1000, update_time)

# --- GUI設定 ---
root = tk.Tk()
root.title("Auto-Save Alarm Clock")
root.geometry("400x500")

clock_label = tk.Label(root, font=("Helvetica", 40), pady=20)
clock_label.pack()

input_frame = tk.Frame(root)
input_frame.pack(pady=10)
alarm_entry = tk.Entry(input_frame, width=8, font=("Helvetica", 18))
alarm_entry.insert(0, "07:00")
alarm_entry.pack(side="left", padx=5)
add_button = tk.Button(input_frame, text="追加", command=add_alarm)
add_button.pack(side="left")

listbox = tk.Listbox(root, font=("Helvetica", 14), width=20, height=5)
listbox.pack(pady=5)

delete_button = tk.Button(root, text="選択したアラームを削除", command=delete_alarm)
delete_button.pack()

stop_button = tk.Button(root, text="音を止める", font=("Helvetica", 14), 
                        bg="red", fg="white", command=stop_alarm, state="disabled")
stop_button.pack(pady=20)

# 起動時にデータを読み込む
load_alarms()
update_time()

root.mainloop()
