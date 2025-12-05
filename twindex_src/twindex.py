import wx
import settings

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
        wx.Frame.__init__(self, None, -1, "List control report")

        # Main -----------------------------------------------------------------
        self.pnl_main = wx.Panel(self)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)

        # Top ------------------------------------------------------------------
        self.siz_dir1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_dir1 = wx.StaticText(self.pnl_main, wx.ID_ANY, label='Folder &1:')
        self.txt_dir1 = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.btn_dir1 = wx.Button(self.pnl_main, wx.ID_ANY, "Browse...")

        self.siz_dir1.Add(self.lbl_dir1, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, border=5)
        self.siz_dir1.Add(self.txt_dir1, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.siz_dir1.Add(self.btn_dir1, flag=wx.TOP|wx.RIGHT, border=5)

        self.siz_dir2 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_dir2 = wx.StaticText(self.pnl_main, wx.ID_ANY, label='Folder &2:')
        self.txt_dir2 = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.btn_dir2 = wx.Button(self.pnl_main, wx.ID_ANY, "Browse...")

        self.siz_dir2.Add(self.lbl_dir2, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT, border=5)
        self.siz_dir2.Add(self.txt_dir2, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        self.siz_dir2.Add(self.btn_dir2, flag=wx.TOP|wx.RIGHT, border=5)

        # Center ---------------------------------------------------------------
        self.siz_center = wx.BoxSizer(wx.VERTICAL)
        self.list = wx.ListCtrl(self.pnl_main, wx.NewIdRef(), style=wx.LC_REPORT | wx.LC_HRULES)
        self.siz_center.Add(self.list, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)

        # Bottom ---------------------------------------------------------------
        self.siz_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_open1 = wx.Button(self.pnl_main, wx.NewIdRef(), "Open &Left")
        self.btn_del1 = wx.Button(self.pnl_main, wx.NewIdRef(), "Delete Left")
        self.btn_search = wx.Button(self.pnl_main, wx.NewIdRef(), "Search")
        self.btn_del2 = wx.Button(self.pnl_main, wx.NewIdRef(), "Delete Right")
        self.btn_open2 = wx.Button(self.pnl_main, wx.NewIdRef(), "Open &Right")

        self.siz_bottom.Add(self.btn_open1, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_del1, flag=wx.TOP, border=5)
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_search, proportion=1, flag=wx.ALL, border=5)
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_del2, flag=wx.TOP, border=5)
        self.siz_bottom.Add(self.btn_open2, flag=wx.ALL, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(self.siz_dir1, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_dir2, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_center, proportion=1, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_bottom, flag=wx.EXPAND)
        self.pnl_main.SetSizer(self.szr_main)

        #self.SetAutoLayout(1)
        #self.szr_main.Fit(self)

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MOVE_END, self.on_move_end)
        self.btn_open1.Bind(wx.EVT_BUTTON, self.on_btn1)

        # Add data to list
        self.list.InsertColumn(0, "Data #1")
        self.list.InsertColumn(1, "Data #2")

        # Add the rows
        for item in data:
            index = self.list.InsertItem(self.list.GetItemCount(), item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetItem(index, col+1, text)

        self.settings = settings.Settings(self)

    def on_key_combo(self, event):
        window = self.FindWindowById(self.acc_dict[event.GetId()])
        window.SetFocus()

    def on_move_end(self, event):
        self.settings.frame_moved()
        event.Skip()

    def on_size(self, event):
        # Why use wx.CallAfter()? Without it, resizing may happen before 
        # the layout is complete, and column sizes may be wrong.
        # CallAfter forces resizing AFTER the UI finishes laying out.
        wx.CallAfter(self.resize_columns)
        event.Skip()

    def on_close(self, evt):
        self.settings.write()
        self.Destroy()

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

    def on_btn1(self, event):
        print("Button")

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