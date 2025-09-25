import pyautogui
import time
import keyboard
import logging

CLICK_COUNT = 3
CLICK_INTERVAL = 0.2
WAIT_MINUTES = 31

logging.basicConfig(filename="bongo.log", level=logging.INFO)

def get_click_position(timeout=5):
    print(f"{timeout}秒以内にクリックしてください...")
    start = time.time()
    while time.time() - start < timeout:
        if pyautogui.mouseDown():
            return pyautogui.position()
    raise RuntimeError("クリック位置が取得できませんでした")

def main():
    pyautogui.FAILSAFE = True
    x, y = get_click_position()
    print(f"位置を記録しました: ({x},{y})")

    while True:
        if keyboard.is_pressed("esc"):
            print("終了します")
            break

        for _ in range(CLICK_COUNT):
            pyautogui.click(x, y)
            time.sleep(CLICK_INTERVAL)

        logging.info("Clicked at (%d, %d)", x, y)
        time.sleep(WAIT_MINUTES * 60)

        
if __name__ == "__main__":
    main()
