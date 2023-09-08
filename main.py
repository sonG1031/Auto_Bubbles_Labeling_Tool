from pynput import mouse 
from pynput import keyboard
import pyautogui
from roboflow import Roboflow

coord = []
flag = False
cropped_img_path = "cropped.png"
rf = Roboflow(api_key="onmlowwu2Z6sNNupWM5Z")
project = rf.workspace().project("webtoon-bubble-detection")
model = project.version(8).model

def click(x,y,button,pressed):
    global coord
    global flag
    if flag and pressed:
        x = int(x)
        y = int(y)
        coord.append(x)
        coord.append(y)

        if len(coord) == 4:
            print(f"coord : {coord}")
            
            left = coord[0]
            top = coord[1]
            right = coord[2]
            bottom = coord[3]
            cropped_img = pyautogui.screenshot().crop((left, top, right, bottom))
            cropped_img.save(cropped_img_path)
            
            positions = model.predict(cropped_img_path, confidence=50, overlap=50).json()["predictions"]
            print(positions)
            for pos in reversed(positions):
                if pos['class'] == "misc-text" or pos['class'] == "only-text" or pos['class'] == "small-text" or pos['class'] == "sound-text":
                    continue
                pyautogui.press('b')

                move_pos = [
                    left + pos["x"], 
                    top + pos["y"],
                    left + pos["x"] + pos["width"],
                    top + pos["y"] + pos["height"]
                ]
                
                print(f"move_pos : {move_pos}")

                pyautogui.moveTo(move_pos[0], move_pos[1], 0.1)
                pyautogui.dragTo(move_pos[2], move_pos[3], 0.1)
                pyautogui.click()

                pyautogui.press('m')
                pyautogui.moveTo(left, top)
                pyautogui.click()

            pyautogui.press('s')

            coord = []

            
mouseListener = mouse.Listener(on_click = click)
mouseListener.start()

def on_press(key):
    global flag

    if key == keyboard.Key.shift:
        print("Start")
        flag = True
    elif key == keyboard.Key.alt_l:
        print("Stopped")
        flag = False
        coord = []
    elif key == keyboard.Key.enter:
        print("Quit")
        mouseListener.stop()
        return False

with keyboard.Listener(on_press= on_press) as keyboardListener:
    keyboardListener.join()

