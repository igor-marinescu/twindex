import os
import wx
import settings
import twin_finder
import subprocess
import filter

# class MyFrame
# class MyApp

#-----------------------------------------------------------------------------

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
        self.btn_search = wx.Button(self.pnl_main, wx.NewIdRef(), "&Search")
        self.btn_filter = wx.Button(self.pnl_main, wx.NewIdRef(), "&Filter")
        self.btn_del_r = wx.Button(self.pnl_main, wx.NewIdRef(), "Delete Right")
        self.btn_open_r = wx.Button(self.pnl_main, wx.NewIdRef(), "Open &Right")

        self.siz_bottom.Add(self.btn_open_l, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_del_l, flag=wx.TOP, border=5)
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_search, proportion=1, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_filter, flag=wx.TOP, border=5)
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
        self.btn_del_l.Bind(wx.EVT_BUTTON, self.on_btn_delete)
        self.btn_del_r.Bind(wx.EVT_BUTTON, self.on_btn_delete)
        self.btn_search.Bind(wx.EVT_BUTTON, self.on_btn_search)
        self.btn_filter.Bind(wx.EVT_BUTTON, self.on_btn_filter)

        # Populate Data --------------------------------------------------------
        self.settings = settings.Settings(self)
        self.txt_dir1.AppendText(self.settings.get_text("ui", "dir1"))
        self.txt_dir2.AppendText(self.settings.get_text("ui", "dir2"))

        # Add data to list
        self.list.InsertColumn(0, "File 1")
        self.list.InsertColumn(1, "File 2")
        self.list.InsertColumn(2, "Size")

        self.enable_buttons()

    #---------------------------------------------------------------------------
    def enable_buttons(self, enable=None):
        """ Enable or disable Open/Delete buttons
        """
        if not enable:
            enable = self.list.GetItemCount() > 0
        self.btn_open_l.Enable(enable)
        self.btn_del_l.Enable(enable)
        self.btn_del_r.Enable(enable)
        self.btn_open_r.Enable(enable)

    #---------------------------------------------------------------------------
    def error_box(self, text, caption = "Error"):
        """ Display Message Box with an Error message
        """
        dlg = wx.MessageDialog(self, text, caption, style=wx.OK|wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    #---------------------------------------------------------------------------
    def on_close(self, evt):
        """ Event called when Frame is closed
            Save the settings and destroy the Frame
        """
        self.settings.set_text("ui", "dir1", self.txt_dir1.GetLineText(0))
        self.settings.set_text("ui", "dir2", self.txt_dir2.GetLineText(0))
        self.settings.write()
        self.Destroy()

    #---------------------------------------------------------------------------
    def on_move_end(self, event):
        """ Event called when user finished moving the Frame
            Remember the new Frame's position in the settings - we need this
            in case the user closes the App and the Frame in maximized
            (we have to store Frame's position every time when not maximized)
        """
        self.settings.frame_moved()
        event.Skip()

    #---------------------------------------------------------------------------
    def on_size(self, event):
        # Why use wx.CallAfter()? Without it, resizing may happen before 
        # the layout is complete, and column sizes may be wrong.
        # CallAfter forces resizing AFTER the UI finishes laying out.
        wx.CallAfter(self.resize_columns)
        event.Skip()

    #---------------------------------------------------------------------------
    def list_has_vertical_scrollbar(self, listctrl):
        count = listctrl.GetItemCount()
        if count == 0:
            return False

        item_height = listctrl.GetItemRect(0).height
        total_height = item_height * count
        client_height = listctrl.GetClientSize().height

        return total_height > client_height
    
    #---------------------------------------------------------------------------
    def resize_columns(self):

        width = self.list.GetClientSize().width

        # If there's a vertical scrollbar, compensate for its width
        if self.list_has_vertical_scrollbar(self.list):
            width -= wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X)

        col_width = (width - 100) // 2

        self.list.SetColumnWidth(0, col_width)
        self.list.SetColumnWidth(1, col_width)
        self.list.SetColumnWidth(2, 100)

    #---------------------------------------------------------------------------
    def on_btn_open(self, event):
        """ Event called when one of Open (left or right) buttons are pressed
        """
        item_column = 0
        if event.GetId() == self.btn_open_r.GetId():
            item_column = 1

        selected = self.list.GetFirstSelected()
        if selected >= 0:
            item_text = self.list.GetItemText(selected, item_column)
            explorer_cmd = r'explorer /select,"' + item_text + r'"'
            subprocess.Popen(explorer_cmd)
        else:
            self.error_box("No file selected")

    #---------------------------------------------------------------------------
    def on_btn_delete(self, event):
        """ Event called when one of Delete (left or right) buttons are pressed
        """
        item_column = 0
        if event.GetId() == self.btn_del_r.GetId():
            item_column = 1

        selected = self.list.GetFirstSelected()
        if selected < 0:
            self.error_box("No file selected")
            return
        while selected >= 0:
            item_text = self.list.GetItemText(selected, item_column)

            strs = item_text + "\nAre you sure?"
            dlg = wx.MessageDialog(self, strs, "Delete File", wx.YES_NO|wx.NO_DEFAULT|wx.CANCEL|wx.ICON_QUESTION)
            res = dlg.ShowModal()
            dlg.Destroy()

            if res == wx.ID_YES:
                try:
                    os.remove(item_text)  
                except:
                    self.error_box("Cannot delete file:\n" + item_text)
                    break

                self.list_delete_item_by_name(item_text)
                self.enable_buttons()

            elif res == wx.ID_CANCEL:
                break

            selected = self.list.GetNextSelected(selected)

    #---------------------------------------------------------------------------
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

    #---------------------------------------------------------------------------
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
                err_text = dir1 + "\ndoes not exist"
                
        dir2 = self.txt_dir2.GetLineText(0)
        if dir2:
            if os.path.isdir(dir2):
                dir_list.append(dir2)
            else:
                err_text = dir2 + "\ndoes not exist"

        if not err_text and (len(dir_list) == 0):
            err_text = "No directory selected"

        if err_text:
            self.error_box(err_text)
            return

        self.list.DeleteAllItems()
        t_f = twin_finder.TwinFinder()
        tw_list = t_f.scan(dir_list)
        for t_rec in tw_list:
            index = self.list.InsertItem(self.list.GetItemCount(), t_rec[1])
            self.list.SetItem(index, 1, t_rec[2])
            self.list.SetItem(index, 2, str(t_rec[0]))
        self.enable_buttons()

    #---------------------------------------------------------------------------
    def list_delete_item_by_name(self, name):
        """ Iterate through the list and delete all items having name
        """
        while True:
            for item_idx in range(self.list.GetItemCount()):
                if (self.list.GetItemText(item_idx, 0) == name) \
                or (self.list.GetItemText(item_idx, 1) == name):
                    self.list.DeleteItem(item_idx)
                    break
            else:
                break

    #---------------------------------------------------------------------------
    def on_btn_filter(self, event):
        """ Event called when Search Button is pressed
            Invoke TwinFinder and search for duplicate files
        """
        filter1 = filter.FilterData()
        filter1.load(self.settings, "Filter1")
        dlg = filter.FilterDialog(self, filter1)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
             filter1.save(self.settings, "Filter1")
        dlg.Destroy()

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