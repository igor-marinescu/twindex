import configparser
import wx

class Settings:

    def __init__(self, main_frame):
        
        self.saved_frame_rect = wx.Rect(wx.DefaultCoord, wx.DefaultCoord, 600, 500)
        self.main_frame = main_frame

        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")

        try:
            self.saved_frame_rect = eval(self.config["window"]["position"])
        except:
            # [window] position in the config file has an invalid value, ignore
            pass
        main_frame.SetSize(self.saved_frame_rect)

        try:
            if(eval(self.config["window"]["maximized"])):
                main_frame.Maximize()
        except:
            pass

    def write(self):
        self.config["window"] = {}
        self.config["window"]["position"] = repr(self.saved_frame_rect)
        self.config["window"]["maximized"] = repr(self.main_frame.IsMaximized())

        with open("settings.ini", 'w') as config_file:
            self.config.write(config_file)        

    def frame_moved(self):
        if not self.main_frame.IsMaximized():
            self.saved_frame_rect = self.main_frame.GetRect()

    def get_text(self, category, key, default = ""):
        if category in self.config:
            return self.config[category].get(key, default)
        return default

    def set_text(self, category, key, value):
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value

    def get_int(self, category, key, default = 0):
        val = default
        if category in self.config:
            txt = self.config[category].get(key)
            if txt and len(txt) > 0:
                try:
                    val = int(txt)
                except:
                    val = default
        return val

    def set_int(self, category, key, value):
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = str(value)

    def get_flag(self, category, key, default = False):
        val = default
        if category in self.config:
            txt = self.config[category].get(key)
            if txt and len(txt) > 0:
                try:
                    if int(txt) > 0:
                        val = True
                except:
                    val = default
        return val

    def set_flag(self, category, key, value):
        if category not in self.config:
            self.config[category] = {}
        val_int = 0
        if value:
            val_int = 1
        self.config[category][key] = str(val_int)
