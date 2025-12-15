import wx

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
and_or_cmd = ["AND", "OR"]
only_exclude_list = ["Only Files", "Exclude Files"]
file_size_cmd_list = ["==", ">", "<", "!="]

#
# [Only Files/Exclude Files V]
#   -------------------------
#   File names: [           ]
#   [And/Or V]
#   Directory names: [      ]
#   -------------------------
#   File size: [>,<,=,!= V]
#   [And/Or V]
#   File size: [>,<,=,!= V]
#   -------------------------

class FilterDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Filter")

        # Main -----------------------------------------------------------------
        self.pnl_main = wx.Panel(self)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)

        # [Only Files/Exclude Files V]
        self.cmb_only = wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY)
        self.cmb_only.Append(only_exclude_list)
        self.szr_main.Add(self.cmb_only, flag=wx.ALL, border=5)

        self.szr_main.Add(wx.StaticLine(self.pnl_main), flag=wx.EXPAND|wx.ALL)

        # File names: [**********]
        self.siz_fname = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_fname = wx.StaticText(self.pnl_main, wx.ID_ANY, label="&File names:")
        self.txt_fname = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.siz_fname.Add(self.lbl_fname, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        self.siz_fname.Add(self.txt_fname, proportion=1, flag=wx.ALL, border=5)
        self.szr_main.Add(self.siz_fname, flag=wx.EXPAND)

        # [And/Or V]
        self.cmb_fcmd1 = wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY)
        self.cmb_fcmd1.Append(and_or_cmd)
        self.szr_main.Add(self.cmb_fcmd1, flag=wx.ALL, border=5)

        # Directory names: [********]
        self.siz_dname = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_dname = wx.StaticText(self.pnl_main, wx.ID_ANY, label="&Dir names:")
        self.txt_dname = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.siz_dname.Add(self.lbl_dname, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        self.siz_dname.Add(self.txt_dname, proportion=1, flag=wx.ALL, border=5)
        self.szr_main.Add(self.siz_dname, flag=wx.EXPAND)

        self.szr_main.Add(wx.StaticLine(self.pnl_main), flag=wx.EXPAND|wx.ALL)

        # File size: [>,<,=,!= V]
        self.siz_fsiz1 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_fsiz1 = wx.StaticText(self.pnl_main, wx.ID_ANY, label="File &size:")
        self.cmb_fsiz1 = wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY)
        self.txt_fsiz1 = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.cmb_fsiz1.Append(file_size_cmd_list)
        self.siz_fsiz1.Add(self.lbl_fsiz1, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        self.siz_fsiz1.Add(self.cmb_fsiz1, flag=wx.ALL, border=5)
        self.siz_fsiz1.Add(self.txt_fsiz1, proportion=1, flag=wx.ALL, border=5)
        self.szr_main.Add(self.siz_fsiz1, flag=wx.EXPAND)

        # [And/Or V]
        self.cmb_fcmd2 = wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY)
        self.cmb_fcmd2.Append(and_or_cmd)
        self.szr_main.Add(self.cmb_fcmd2, flag=wx.ALL, border=5)

        # File size: [>,<,=,!= V]
        self.siz_fsiz2 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_fsiz2 = wx.StaticText(self.pnl_main, wx.ID_ANY, label="File &size:")
        self.cmb_fsiz2 = wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY)
        self.txt_fsiz2 = wx.TextCtrl(self.pnl_main, wx.ID_ANY)
        self.cmb_fsiz2.Append(file_size_cmd_list)
        self.siz_fsiz2.Add(self.lbl_fsiz2, flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
        self.siz_fsiz2.Add(self.cmb_fsiz2, flag=wx.ALL, border=5)
        self.siz_fsiz2.Add(self.txt_fsiz2, proportion=1, flag=wx.ALL, border=5)
        self.szr_main.Add(self.siz_fsiz2, flag=wx.EXPAND)

        self.szr_main.Add(wx.StaticLine(self.pnl_main), flag=wx.EXPAND|wx.ALL)

        self.siz_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok = wx.Button(self.pnl_main, wx.ID_OK)
        self.btn_cancel = wx.Button(self.pnl_main, wx.ID_CANCEL)
        self.btn_cancel.SetDefault()
        
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_ok, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_cancel, flag=wx.ALL, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(self.siz_bottom, flag=wx.EXPAND)
        self.pnl_main.SetSizer(self.szr_main)

        # size the dialog to fit the content managed by the sizer
        self.szr_main.Fit(self)

#---------------------------------------------------------------------------

if __name__ == "__main__" :
    app = wx.App()
    dlg = FilterDialog(None)
    val = dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop() 