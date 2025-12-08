import os
import wx
import settings
import twin_finder

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Twindex")

        # Main -----------------------------------------------------------------
        self.pnl_main = wx.Panel(self)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)

        # Top ------------------------------------------------------------------
        self.siz_dir1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_dir1 = wx.StaticText(self.pnl_main, wx.ID_ANY, label='Dir &1:')
        self.txt_dir1 = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.btn_dir1 = wx.Button(self.pnl_main, wx.ID_ANY, "Browse...")

        self.siz_dir1.Add(self.lbl_dir1, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, border=5)
        self.siz_dir1.Add(self.txt_dir1, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.siz_dir1.Add(self.btn_dir1, flag=wx.TOP|wx.RIGHT, border=5)

        self.siz_dir2 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_dir2 = wx.StaticText(self.pnl_main, wx.ID_ANY, label='Dir &2:')
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
        self.btn_open_l = wx.Button(self.pnl_main, wx.NewIdRef(), "Open &Left")
        self.btn_del_l = wx.Button(self.pnl_main, wx.NewIdRef(), "Delete Left")
        self.btn_search = wx.Button(self.pnl_main, wx.NewIdRef(), "Search")
        self.btn_del_r = wx.Button(self.pnl_main, wx.NewIdRef(), "Delete Right")
        self.btn_open_r = wx.Button(self.pnl_main, wx.NewIdRef(), "Open &Right")

        self.siz_bottom.Add(self.btn_open_l, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_del_l, flag=wx.TOP, border=5)
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_search, proportion=1, flag=wx.ALL, border=5)
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_del_r, flag=wx.TOP, border=5)
        self.siz_bottom.Add(self.btn_open_r, flag=wx.ALL, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(self.siz_dir1, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_dir2, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_center, proportion=1, flag=wx.EXPAND)
        self.szr_main.Add(self.siz_bottom, flag=wx.EXPAND)
        self.pnl_main.SetSizer(self.szr_main)

        #self.SetAutoLayout(1)
        #self.szr_main.Fit(self)

        # Bind events ----------------------------------------------------------
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_MOVE_END, self.on_move_end)
        self.btn_dir1.Bind(wx.EVT_BUTTON, self.on_btn_browse)
        self.btn_dir2.Bind(wx.EVT_BUTTON, self.on_btn_browse)
        self.btn_open_l.Bind(wx.EVT_BUTTON, self.on_btn_open)
        self.btn_open_r.Bind(wx.EVT_BUTTON, self.on_btn_open)
        self.btn_search.Bind(wx.EVT_BUTTON, self.on_btn_search)

        # Populate Data --------------------------------------------------------
        self.settings = settings.Settings(self)
        self.txt_dir1.AppendText(self.settings.get_text("ui", "dir1"))
        self.txt_dir2.AppendText(self.settings.get_text("ui", "dir2"))

        # Add data to list
        self.list.InsertColumn(0, "File 1")
        self.list.InsertColumn(1, "File 2")
        self.list.InsertColumn(2, "Size")

    def on_close(self, evt):
        """ Event called when Frame is closed
            Save the settings and destroy the Frame
        """
        self.settings.set_text("ui", "dir1", self.txt_dir1.GetLineText(0))
        self.settings.set_text("ui", "dir2", self.txt_dir2.GetLineText(0))
        self.settings.write()
        self.Destroy()

    def on_move_end(self, event):
        self.settings.frame_moved()
        event.Skip()

    def on_size(self, event):
        # Why use wx.CallAfter()? Without it, resizing may happen before 
        # the layout is complete, and column sizes may be wrong.
        # CallAfter forces resizing AFTER the UI finishes laying out.
        wx.CallAfter(self.resize_columns)
        event.Skip()

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

        col_width = (width - 100) // 2

        self.list.SetColumnWidth(0, col_width)
        self.list.SetColumnWidth(1, col_width)
        self.list.SetColumnWidth(2, 100)

    def on_btn_open(self, event):
        left = False
        if event == None:
            return
        if event.GetId() == self.btn_open_l.GetId():
            print("Button Left")
        elif event.GetId() == self.btn_open_r.GetId():
            print("Button Right")
        else:
            return

    def on_btn_browse(self, event):
        """ Event called when Browse Dir1 or Browse Dir2 is pressed
        """
        txt_ctrl = self.txt_dir1
        # Check which button pressed Dir1 or Dir2?
        if event.GetId() == self.btn_dir2.GetId():
            txt_ctrl = self.txt_dir2
        dlg = wx.DirDialog(self, "Choose directory", txt_ctrl.GetLineText(0),
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            txt_ctrl.Clear()
            txt_ctrl.AppendText(dlg.GetPath())

    def on_btn_search(self, event):
        """ Event called when Search Button is pressed
            Invoke TwinFinder and search for duplicate files
        """
        dir_list = []
        err_text = None

        dir1 = self.txt_dir1.GetLineText(0)
        if dir1:
            if os.path.isdir(dir1):
                dir_list.append(dir1)
            else:
                err_text = "Directory 1 (" + dir1 + ") does not exist"
                
        dir2 = self.txt_dir2.GetLineText(0)
        if dir2:
            if os.path.isdir(dir2):
                dir_list.append(dir2)
            else:
                err_text = "Directory 2 (" + dir2 + ") does not exist"

        if len(dir_list) == 0:
            err_text = "No directory selected"

        if err_text:
            dlg = wx.MessageDialog(self, err_text, caption="Error", style=wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            return

        self.list.DeleteAllItems()
        t_f = twin_finder.TwinFinder()
        tw_list = t_f.scan(dir_list)
        for t_rec in tw_list:
            index = self.list.InsertItem(self.list.GetItemCount(), t_rec[1])
            self.list.SetItem(index, 1, t_rec[2])
            self.list.SetItem(index, 2, str(t_rec[0]))

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