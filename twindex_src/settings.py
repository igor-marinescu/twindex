import configparser
import wx

class Settings:

    def __init__(self, main_frame):
        
        self.saved_frame_rect = wx.Rect(wx.DefaultCoord, wx.DefaultCoord, 600, 500)
        self.main_frame = main_frame

        config = configparser.ConfigParser()
        config.read("settings.ini")

        try:
            self.saved_frame_rect = eval(config["window"]["position"])
        except:
            # [window] position in the config file has an invalid value, ignore
            pass
        main_frame.SetSize(self.saved_frame_rect)

        try:
            if(eval(config["window"]["maximized"])):
                main_frame.Maximize()
        except:
            pass

    def write(self):
        config = configparser.ConfigParser()
        config["window"] = {}
        config["window"]["position"] = repr(self.saved_frame_rect)
        config["window"]["maximized"] = repr(self.main_frame.IsMaximized())

        with open("settings.ini", 'w') as config_file:
            config.write(config_file)        

    def frame_moved(self):
        if not self.main_frame.IsMaximized():
            self.saved_frame_rect = self.main_frame.GetRect()

