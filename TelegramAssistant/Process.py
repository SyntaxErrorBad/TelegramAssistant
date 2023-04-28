import os
import pyautogui
import keyboard
import screen_brightness_control as sbc
import openai


from config import *



class TelegramProcess:
    def __init__(self,message,Root,bot) -> None:
        self.message = message
        self.Root = Root
        self.bot = bot

    def Power_OFF(self):
        os.system('shutdown -s -t 0')
    
    def Screenshot(self):
        file_name = 'photo.png'
        img = pyautogui.screenshot(file_name)
        img.save(file_name)
        self.bot.send_photo(self.message.chat.id, img)
        os.remove(file_name)

    def Block_Keyboard(self,Check):
        if Check:
            for i in range(150):
                keyboard.block_key(i)
            Check = False

        else:
            for i in range(150):
                keyboard.unblock_key(i)
            Check = True
        
        return Check
    
    def Write_Text_Keyboard(self,Text):
        if Text == "Add Text":
            keyboard.write(self.message)
        elif Text == "Remove Text":
            keyboard.send("backspace")
        elif Text == "Press Enter":
            keyboard.send("enter")
