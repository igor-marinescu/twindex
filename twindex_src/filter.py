import wx

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
filter_text = [
    "None",
    "File name =",
    "File name !=",
    "File size =",
    "File size <",
    "File size >",
]

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

        self.siz_flt = []
        self.lbl_flt = []
        self.cmb_flt = []
        self.txt_flt = []

        for i in range(5):
            self.siz_flt.append(wx.BoxSizer(wx.HORIZONTAL))
            self.lbl_flt.append(wx.StaticText(self.pnl_main, wx.ID_ANY, label="Filter &" + str(i+1) + ":"))
            self.cmb_flt.append(wx.ComboBox(self.pnl_main, wx.ID_ANY, style=wx.CB_READONLY))
            self.txt_flt.append(wx.TextCtrl(self.pnl_main, wx.ID_ANY))

            self.cmb_flt[i].Append(filter_text)

            self.siz_flt[i].Add(self.lbl_flt[i], flag=wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=5)
            self.siz_flt[i].Add(self.cmb_flt[i], proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
            self.siz_flt[i].Add(self.txt_flt[i], flag=wx.ALL, border=5)

            self.szr_main.Add(self.siz_flt[i], flag=wx.EXPAND)

        self.siz_bottom = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok = wx.Button(self.pnl_main, wx.ID_OK)
        self.btn_cancel = wx.Button(self.pnl_main, wx.ID_CANCEL)
        self.btn_cancel.SetDefault()
        
        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_ok, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_cancel, flag=wx.ALL, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(wx.StaticLine(self.pnl_main), flag=wx.EXPAND|wx.ALL)
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