import wx

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

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        id = wx.NewIdRef()
        self.list = wx.ListCtrl(self, id,
                                style=wx.LC_REPORT|
                                      wx.SUNKEN_BORDER)

        # Add some columns
        self.list.InsertColumn(0, "Data #1")
        self.list.InsertColumn(1, "Data #2")

        # Add the rows
        for item in data:
            index = self.list.InsertItem(self.list.GetItemCount(), item[0])
            for col, text in enumerate(item[1:]):
                self.list.SetItem(index, col+1, text)

        # Set the width of the columns
        self.list.SetColumnWidth(0, 120)
        self.list.SetColumnWidth(1, 120)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.list, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

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