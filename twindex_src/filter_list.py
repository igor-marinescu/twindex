import wx
import copy
import settings
import filter

class FilterListDialog(wx.Dialog):

    def __init__(self, parent, filter_list):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Filter List", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.filter_list = filter_list

        # Main -----------------------------------------------------------------
        self.pnl_main = wx.Panel(self)
        self.szr_main = wx.BoxSizer(wx.VERTICAL)

        # Center - List --------------------------------------------------------
        self.siz_center = wx.BoxSizer(wx.HORIZONTAL)

        self.lst_filter = wx.CheckListBox(self.pnl_main, wx.ID_ANY)
        self.lst_filter.Bind(wx.EVT_LISTBOX, self.on_list_sel_changed)
        self.lst_filter.Bind(wx.EVT_LISTBOX_DCLICK, self.on_list_dclick)
        self.siz_center.Add(self.lst_filter, proportion=1, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        # Right - Buttons ------------------------------------------------------
        self.szr_right = wx.BoxSizer(wx.VERTICAL)
        self.btn_add = wx.Button(self.pnl_main, wx.ID_ANY, "&Add")
        self.btn_up = wx.Button(self.pnl_main, wx.ID_ANY, "&Up")
        self.btn_down = wx.Button(self.pnl_main, wx.ID_ANY, "Dow&n")
        self.btn_delete = wx.Button(self.pnl_main, wx.ID_ANY, "&Delete")
        self.btn_edit = wx.Button(self.pnl_main, wx.ID_ANY, "&Edit")

        self.szr_right.Add(self.btn_add, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.szr_right.Add(self.btn_up, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.szr_right.Add(self.btn_down, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.szr_right.Add(self.btn_delete, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=5)
        self.szr_right.Add(self.btn_edit, flag=wx.LEFT|wx.TOP|wx.RIGHT, border=5)

        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add_button)
        self.btn_up.Bind(wx.EVT_BUTTON, self.on_up_button)
        self.btn_down.Bind(wx.EVT_BUTTON, self.on_down_button)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete_button)
        self.btn_edit.Bind(wx.EVT_BUTTON, self.on_edit_button)

        self.siz_center.Add(self.szr_right)

        self.szr_main.Add(self.siz_center, proportion=1, flag=wx.EXPAND)
        self.szr_main.Add(wx.StaticLine(self.pnl_main), flag=wx.EXPAND|wx.ALL)

        # Bottom - Buttons --------------------------------------------------------
        self.siz_bottom = wx.BoxSizer(wx.HORIZONTAL)
    
        self.btn_ok = wx.Button(self.pnl_main, wx.ID_OK)
        self.btn_cancel = wx.Button(self.pnl_main, wx.ID_CANCEL)
        self.btn_cancel.SetDefault()
        
        self.Bind(wx.EVT_BUTTON, self.on_ok_button, self.btn_ok)

        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_ok, flag=wx.BOTTOM|wx.TOP|wx.RIGHT, border=5)
        self.siz_bottom.Add(self.btn_cancel, flag=wx.BOTTOM|wx.TOP|wx.RIGHT, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(self.siz_bottom, flag=wx.EXPAND)
        self.pnl_main.SetSizer(self.szr_main)

        # size the dialog to fit the content managed by the sizer
        #self.szr_main.Fit(self)

        # Dialog sizer
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(self.pnl_main, 1, wx.EXPAND)

        self.SetSizer(dlgSizer)
        self.SetMinSize(self.GetSize())

        # Populate data --------------------------------------------------------
        for f in self.filter_list:
            self.lst_filter.Append(f.generate_name(), copy.deepcopy(f))
            self.lst_filter.Check(self.lst_filter.GetCount() - 1, f.enabled)

        self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def enable_right_buttons(self):
        """ Method decides which Buttons on the right side are enabled
        """
        selected = self.lst_filter.GetSelection()
        is_selected = (selected != wx.NOT_FOUND)
        not_empty = (self.lst_filter.GetCount() > 0)
        first = not_empty and (selected == 0)
        last = not_empty and (selected == (self.lst_filter.GetCount() - 1))

        self.btn_up.Enable(not_empty and is_selected and not first)
        self.btn_down.Enable(not_empty and is_selected and not last)
        self.btn_delete.Enable(not_empty and is_selected)
        self.btn_edit.Enable(not_empty and is_selected)

    #---------------------------------------------------------------------------
    def edit_element(self, index):
        filter_data = self.lst_filter.GetClientData(index)
        if filter_data != None:
            dlg = filter.FilterDialog(self, filter_data)
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                self.lst_filter.SetString(index, filter_data.generate_name())

    #---------------------------------------------------------------------------
    def exchange_elements(self, idx0, idx1):
        """ Exchange two elements in the list
        """
        count = self.lst_filter.GetCount()
        if (idx0 >= 0) and (idx1 >= 0) and (idx0 < count) and (idx1 < count):
            item0_txt = self.lst_filter.GetString(idx0)
            item0_data = self.lst_filter.GetClientData(idx0)
            item0_checked = self.lst_filter.IsChecked(idx0)
            item1_txt = self.lst_filter.GetString(idx1)
            item1_data = self.lst_filter.GetClientData(idx1)
            item1_checked = self.lst_filter.IsChecked(idx1)
            self.lst_filter.SetString(idx0, item1_txt)
            self.lst_filter.SetClientData(idx0, item1_data)
            self.lst_filter.Check(idx0, item1_checked)
            self.lst_filter.SetString(idx1, item0_txt)
            self.lst_filter.SetClientData(idx1, item0_data)
            self.lst_filter.Check(idx1, item0_checked)

    #---------------------------------------------------------------------------
    def on_list_sel_changed(self, event):
        """ Event called when an item on the list is selected or the selection changes
        """
        self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def on_list_dclick(self, event):
        """ Event called when the listbox is double-clicked
            Edit selected element from the list
        """
        selected = self.lst_filter.GetSelection()
        if selected != wx.NOT_FOUND:
            self.edit_element(selected)

    #---------------------------------------------------------------------------
    def on_add_button(self, event):
        """ Event called when 'Add' button is pressed
            Add new element to the list
        """

        filter_new = filter.FilterData()
        dlg = filter.FilterDialog(self, filter_new)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            self.lst_filter.Append(filter_new.generate_name(), filter_new)
            self.lst_filter.SetSelection(self.lst_filter.GetCount() - 1)
            self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def on_up_button(self, event):
        """ Event called when 'Up' button is pressed
            Move selected item up in the list
        """
        selected = self.lst_filter.GetSelection()
        if (selected != wx.NOT_FOUND) and (selected > 0):
            self.exchange_elements(selected, selected - 1)
            self.lst_filter.SetSelection(selected - 1)
            self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def on_down_button(self, event):
        """ Event called when 'Down' button is pressed
            Move selected item down in the list
        """
        selected = self.lst_filter.GetSelection()
        if (selected != wx.NOT_FOUND) and (selected < (self.lst_filter.GetCount() - 1)):
            self.exchange_elements(selected, selected + 1)
            self.lst_filter.SetSelection(selected + 1)
            self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def on_delete_button(self, event):
        """ Event called when 'Delete' button is pressed
            Delete selected element from the list
        """
        selected = self.lst_filter.GetSelection()
        if selected != wx.NOT_FOUND:
            self.lst_filter.Delete(selected)
            if(self.lst_filter.GetCount() > 0):
                if(selected >= self.lst_filter.GetCount()):
                    selected = self.lst_filter.GetCount() - 1
                self.lst_filter.SetSelection(selected)
            self.enable_right_buttons()

    #---------------------------------------------------------------------------
    def on_edit_button(self, event):
        """ Event called when 'Edit' button is pressed
            Edit selected element from the list
        """
        selected = self.lst_filter.GetSelection()
        if selected != wx.NOT_FOUND:
            self.edit_element(selected)

    #---------------------------------------------------------------------------
    def on_ok_button(self, event):
        """ Event called when user presses OK button
            Remove all old elements from list
            Copy all data from UI elements to list
        """
        self.filter_list.clear()
        for idx in range(self.lst_filter.GetCount()):
            f = self.lst_filter.GetClientData(idx)
            if f != None:
                f.enabled = self.lst_filter.IsChecked(idx)
            self.filter_list.append(f)

        self.EndModal(wx.ID_OK)

#---------------------------------------------------------------------------

if __name__ == "__main__" :

    app = wx.App()

    filter_list = []
    for i in range(10):
        f = filter.FilterData()
        filter_list.append(f)

    dlg = FilterListDialog(None, filter_list)
    val = dlg.ShowModal()
    if val == wx.ID_OK:
        print("OK pressed")
    else:
        print("Cancel pressed")

    dlg.Destroy()
    app.MainLoop() 