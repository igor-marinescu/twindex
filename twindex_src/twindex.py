import wx
import configparser

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------

data = [("World", "Python"),
        ("wxWidgets", "Data"),
        ("ListCtrl", "Report"),
        ("Index", "Column"),
        ("Width", "Header")]

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          "List control report",
                          size=(380, 220))

        # Centre List ----------------------------------------------------------
        self.panel1 = wx.Panel(self)
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)

        self.list = wx.ListCtrl(self.panel1, wx.NewIdRef(), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list.InsertColumn(0, "Data #1")
        self.list.InsertColumn(1, "Data #2")

        # Add the rows
        for item in data:
            index = self.list.InsertItem(self.list.GetItemCount(), item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetItem(index, col+1, text)

        self.sizer1.Add(self.list, 1, wx.EXPAND | wx.ALL, 5)
        self.panel1.SetSizer(self.sizer1)

        # Bottom Buttons -------------------------------------------------------
        self.panel2 = wx.Panel(self)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.buttons = []
        for i in range(0, 2):
            self.buttons.append(wx.Button(self.panel2, wx.NewIdRef(), "Button &"+str(i)))
            self.sizer2.Add(self.buttons[i], proportion=0, flag=wx.ALL, border=2)

        self.sizer2.AddStretchSpacer()
        self.panel2.SetSizer(self.sizer2)

        #Layout sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel1, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.panel2, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        self.saved_frame_rect = None
        self.SetSize(wx.DefaultCoord, wx.DefaultCoord, 600, 500)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MOVE_END, self.on_move_end)
        self.read_settings()

    def on_move_end(self, event):
        if not self.IsMaximized():
            self.saved_frame_rect = self.GetRect()
        event.Skip()

    def on_size(self, event):
        # Why use wx.CallAfter()? Without it, resizing may happen before 
        # the layout is complete, and column sizes may be wrong.
        # CallAfter forces resizing AFTER the UI finishes laying out.
        wx.CallAfter(self.resize_columns)
        event.Skip()

    def on_close(self, evt):
        self.write_settings()
        self.Destroy()

    def read_settings(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        try:
            self.saved_frame_rect = eval(config["window"]["position"])
            self.SetSize(self.saved_frame_rect)
        except:
            # [window] position in the config file has an invalid value, ignore
            pass
        try:
            if(eval(config["window"]["maximized"])):
                self.Maximize()
        except:
            pass

    def write_settings(self):
        config = configparser.ConfigParser()
        config["window"] = {}
        config["window"]["position"] = repr(self.saved_frame_rect)
        config["window"]["maximized"] = repr(self.IsMaximized())

        with open("settings.ini", 'w') as config_file:
            config.write(config_file)        

    def list_has_vertical_scrollbar(self, listctrl):
        count = listctrl.GetItemCount()
        if count == 0:
            return False

        item_height = listctrl.GetItemRect(0).height
        total_height = item_height * count
        client_height = listctrl.GetClientSize().height

        return total_height > client_height
    
    def resize_columns(self):

        width = self.list.GetClientSize().width

        # If there's a vertical scrollbar, compensate for its width
        if self.list_has_vertical_scrollbar(self.list):
            width -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

        col_width = width // 2

        self.list.SetColumnWidth(0, col_width)
        self.list.SetColumnWidth(1, col_width)

#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):

        #------------

        frame = MyFrame()
        self.SetTopWindow(frame)
        frame.Show(True)

        return True

#---------------------------------------------------------------------------

def main():
    app = MyApp(False)
    app.MainLoop()

#---------------------------------------------------------------------------

if __name__ == "__main__" :
    main()