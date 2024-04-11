import threading

import cv2
import keyboard

import core
import yaml
import pyautogui
import random
import time
import win32gui
import tkinter as tk
from functions import invent_enabled, bank_ready, \
    Image_count, mini_map_image, skill_lvl_up_new, spaces, \
    random_combat, random_quests, random_skills, \
    random_inventory, random_breaks, find_Object_precise, \
    exit_bank, Image_Rec_single_closest, Image_Rec_single, pick_item_new, deposit_secondItem_new, Image_Rec_single_2, \
    Image_count_alpha, invent_count, screen_Image, Image_Rec_single_3

global hwnd, iflag, icoord, newTime_break, \
    timer, timer_break, ibreak

iflag = False
newTime_break = False

with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)


class BotThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num
        self.running = True

    def run(self):
        start_time = time.time()
        loop_count = 0
        while self.running:
            # Call your main function with the user-input value
            main(self.num, loop_count, start_time)
            loop_count += 1
            time.sleep(1)

    def stop(self):
        self.running = False


def gfindWindow(data):  # find window name returns PID of the window
    global hwnd
    hwnd = win32gui.FindWindow(None, data)
    # hwnd = win32gui.GetForegroundWindow()860
    print('findWindow:', hwnd)
    win32gui.SetActiveWindow(hwnd)
    # win32gui.ShowWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 865, 830, True)


try:
    gfindWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass

try:
    x_win, y_win, w_win, h_win = core.getWindow(data[0]['Config']['client_title'])
except BaseException:
    print("Unable to find window:", data[0]['Config']['client_title'], "| Please see list of window names below:")
    core.printWindows()
    pass


def random_break(start, c):
    global newTime_break
    startTime = time.time()
    a = random.randrange(0, 4)
    if startTime - start > c:
        options[a]()
        newTime_break = True


def randomizer(timer_breaks, ibreaks):
    global newTime_break
    global timer_break
    global ibreak
    random_break(timer_breaks, ibreaks)
    if newTime_break:
        timer_break = timer()
        ibreak = random.randrange(600, 2000)
        newTime_break = False


def timer():
    startTime = time.time()
    return startTime


def random_pause():
    global newTime_break
    b = random.uniform(20, 250)
    print('pausing for ' + str(b) + ' seconds')
    time.sleep(b)
    newTime_break = True


iflag = False

options = {0: random_inventory,
           1: random_combat,
           2: random_skills,
           3: random_quests,
           4: random_pause}


def pick_bar():
    Image_Rec_single_2('g_bar2.png', 5, 5, 0.7, 'left', 10, True)
    random_breaks(0.5, 1.5)


def pick_gem():
    Image_Rec_single_2('diamond2.png', 5, 5, 0.7, 'left', 10, True)
    random_breaks(0.5, 1.5)


def pick_mould():
    pick_item_new(265, 153)
    random_breaks(0.5, 1.5)


def bank_spot_edgeville():
    x, y = find_Object_precise(1, 0, 0, 717, 782)  # green
    # print(x, y)


def smith_spot_edgeville():
    find_Object_precise(2)  # amber


def smith_object(smith_item):
    Image_Rec_single_2(smith_item, 5, 5, 0.7, 'left', 10, True)


def smith_items(num, bar, vol, smith_item, Human_Break=True):
    j = round((num * vol) / 13) + 1
    while j > 0:
        bank_spot_edgeville()
        random_breaks(7.5, 9)
        deposit_secondItem_new()
        random_breaks(0.3, 0.5)
        pick_bar()
        random_breaks(0.3, 0.5)
        #  pick_mould()
        #  random_breaks(0.3, 0.5)
        pick_gem()
        exit_bank()
        random_breaks(0.05, 0.2)
        # invent = invent_enabled()
        # print(invent)
        # if invent == 0:
        #     pyautogui.press('esc')
        inv = (Image_count(bar, 0.7, 0, 0, 971, 725)/4)
        # print(inv)
        smith_spot_edgeville()
        random_breaks(7.5, 9)
        smith_object(smith_item + '.png')
        while inv > 0:  # replace 0 with vol
            cv2.waitKey()
            if keyboard.is_pressed('='):  # q to quit
                quit()
            if skill_lvl_up_new('craft_lvl.png') != 0:
                print('level up')
                random_breaks(0.2, 3)
                pyautogui.press('space')
                random_breaks(0.1, 3)
                pyautogui.press('space')
                a = random.randrange(0, 2)
                # print(a)
                spaces(a)
                smith_spot_edgeville()
                random_breaks(1, 2)
                smith_object(smith_item + '.png')
            inv = (Image_count(bar, 0.7, 0, 0, 971, 725)/4)
            # print(inv)
        j -= 1
        if Human_Break:
            c = random.triangular(0.1, 30, 1)
            time.sleep(c)


def pick_nature_rune():
    Image_Rec_single('nature_rune.png', 5, 5, 0.7, 'left', 10, True)


def pick_alch_item():
    Image_Rec_single('d_neck_4.png', 5, 5, 0.7, 'left', 10, True)


def pick_magic():
    Image_Rec_single_3('high_alc.png', 5, 5, 0.7, 'left', 10, True)


def pick_magic_menu():
    Image_Rec_single('magic_menu.png', 5, 5, 0.7, 'left', 10, True)


def invent_count_sync(object, threshold=0.8, left=0, top=0, right=0, bottom=0):
    # Capture screenshot
    screen_Image(left, top, right, bottom, name='screenshot.png')
    # Perform image counting synchronously
    return Image_count(object, threshold, left, top, right, bottom)


def high_alchemy(num, vol, Human_Break=True):
    j = round((num * vol) / 26) + 1
    while j > 0:
        bank_spot_edgeville()
        random_breaks(.5, 1.5)
        pick_alch_item()
        exit_bank()
        random_breaks(0.05, 0.2)
        inv = invent_count_sync('d_neck_4.png')/3
        print(inv)
        pick_magic_menu()
        random_breaks(2, 3)
        while inv > 1.9:  # replace 0 with vol
            if skill_lvl_up_new('magic_lvl.png') != 0:
                print('level up')
                random_breaks(0.2, 3)
                pyautogui.press('space')
                random_breaks(0.1, 3)
                pyautogui.press('space')
                a = random.randrange(1, 2)
                spaces(a)

            cv2.waitKey(1000)
            pick_magic()
            inv = invent_count_sync('d_neck_4.png')/3
            print(inv)
            pick_alch_item()

        random_breaks(0.5, 1)
        pyautogui.press('esc')
        j -= 1
        if Human_Break:
            c = random.triangular(0.1, 10, .6)
            time.sleep(c)

def pick_note():
    Image_Rec_single_3('d_neck_note.png', 5, 5, 0.7, 'left', 10, True)

def high2(num):
    pick_magic_menu()
    while True:
        if keyboard.is_pressed('='):  # q to quit
            quit()
        pick_magic()
        pick_note()
        # random_breaks(0.3, .5)




gem = 'diamond_icon.png'
bar = 'gold_bar.png'
item = 'd_neck'
high_alch_item = ''


def run_bot():
    num_value = int(entry_num.get())
    # Call your main function with the user-input value
    root.destroy()
    main(num_value)


def main(num):
    cv2.waitKey(1000)
    print(num)
    smith_items(num, bar, 1, item, True)
    # high_alchemy(num, 1, True)
    # high2(num)

# Create the main window
root = tk.Tk()
root.title("Bot Configuration")

# Lift the window to the forefront
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)

# Create a label and entry widget for the num variable
label_num = tk.Label(root, text="Enter value for 'num':")
label_num.grid(row=0, column=0, padx=10, pady=5)
entry_num = tk.Entry(root)
entry_num.grid(row=0, column=1, padx=10, pady=5)

# Create a button to run the bot
btn_run = tk.Button(root, text="Run Bot", command=run_bot)
btn_run.grid(row=1, columnspan=2, padx=10, pady=10)

root.mainloop()
