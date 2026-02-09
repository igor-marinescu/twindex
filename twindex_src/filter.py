import wx
import settings
import fnmatch
import os

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
or_and_cmd = ["OR", "AND"]
only_exclude_list = ["Only Files", "Exclude Files"]
file_size_cmd_list = ["", "==", ">", "<", "!="]

class FilterData:

    def __init__(self):
        self.enabled = False
        self.exclude_files = 0
        self.file_names = ""
        self.dir_names = ""
        self.file_and_dir = 0
        self.cmd_size1 = 0
        self.file_size1 = 0
        self.cmd_size2 = 0
        self.file_size2 = 0
        self.size1_and_size2 = 0

    def generate_name(self):
        """ Generate a filter name based on its fields
        """

        # File names and Dir names
        name1 = ""
        if self.file_names and self.dir_names:
            name1 = f"'{self.file_names}' {or_and_cmd[self.file_and_dir]} {self.dir_names}"
        elif self.file_names:
            name1 = f"'{self.file_names}'"
        elif self.dir_names:
            name1 = f"'{self.dir_names}'"

        # File size
        name2 = ""
        if self.cmd_size1 and self.cmd_size2:
            name2 = f"size {file_size_cmd_list[self.cmd_size1]} {str(self.file_size1)}"
            name2 += f" {or_and_cmd[self.size1_and_size2]} "
            name2 += f"size {file_size_cmd_list[self.cmd_size2]} {str(self.file_size2)}"
        elif self.cmd_size1:
            name2 = f"size {file_size_cmd_list[self.cmd_size1]} {str(self.file_size1)}"
        elif self.cmd_size2:
            name2 = f"size {file_size_cmd_list[self.cmd_size2]} {str(self.file_size2)}"

        # Empty?
        if not name1 and not name2:
            return "<Empty>"
        
        name = f"{only_exclude_list[self.exclude_files]} : "
        if name1 and name2:
            name += f"({name1}) AND ({name2})"
        elif name1:
            name += name1
        elif name2:
            name += name2
        return name

    def load(self, settings, filter_name):
        self.enabled = settings.get_flag(filter_name, "enabled")
        self.exclude_files = settings.get_int(filter_name, "exclude_files")
        self.file_names = settings.get_text(filter_name, "file_names")
        self.dir_names = settings.get_text(filter_name, "dir_names")
        self.file_and_dir = settings.get_int(filter_name, "file_and_dir")
        self.cmd_size1 = settings.get_int(filter_name, "cmd_size1")
        self.file_size1 = settings.get_int(filter_name, "file_size1")
        self.cmd_size2 = settings.get_int(filter_name, "cmd_size2")
        self.file_size2 = settings.get_int(filter_name, "file_size2")
        self.size1_and_size2 = settings.get_int(filter_name, "size1_and_size2")

    def save(self, settings, filter_name):
        settings.set_flag(filter_name, "enabled", self.enabled)
        settings.set_int(filter_name, "exclude_files", self.exclude_files)
        settings.set_text(filter_name, "file_names", self.file_names)
        settings.set_text(filter_name, "dir_names", self.dir_names)
        settings.set_int(filter_name, "file_and_dir", self.file_and_dir)
        settings.set_int(filter_name, "cmd_size1", self.cmd_size1)
        settings.set_int(filter_name, "file_size1", self.file_size1)
        settings.set_int(filter_name, "cmd_size2", self.cmd_size2)
        settings.set_int(filter_name, "file_size2", self.file_size2)
        settings.set_int(filter_name, "size1_and_size2", self.size1_and_size2)

    def check(self, file_name, file_size):

        if not self.enabled:
            return False
        
        file_match_flag = False
        dir_match_flag = False

        # Convert "*.txt; *.jpg; some*" -> ["*.txt", "*.jpg", "some*"]
        flt_file_names = self.file_names.split(";")
        flt_dir_names = self.file_names.split(";")

        # Split "C:\\hello\\world.txt" -> "C:\\hello", "world.txt"
        file_name_head, file_name_tail = os.path.split(file_name)

        # Check if file_name tail matches any of the file filters
        for flt in flt_file_names:
            flt.strip()
            if flt and fnmatch.fnmatch(file_name_tail, flt):
                print(file_name_tail, "matches", flt)
                file_match_flag = False
                break

        # Check if file_name head matches any of the dir filters
        for flt in flt_dir_names:
            flt.strip()
            if flt and fnmatch.fnmatch(file_name_head, flt):
                print(file_name_head, "matches", flt)
                dir_match_flag = False
                break

        if flt_file_names and flt_dir_names:
            if self.file_and_dir:
                return file_match_flag and dir_match_flag
            else:
                return file_match_flag or dir_match_flag
        elif flt_file_names:
            return file_match_flag
        elif flt_dir_names:
            return dir_match_flag
        return False
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

    def __init__(self, parent, filter_data):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Filter")
        self.filter_data = filter_data

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
        self.cmb_fcmd1.Append(or_and_cmd)
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
        self.cmb_fcmd2.Append(or_and_cmd)
        self.szr_main.Add(self.cmb_fcmd2, flag=wx.ALL, border=5)

        # File size: [>,<,=,!= V]
        self.siz_fsiz2 = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_fsiz2 = wx.StaticText(self.pnl_main, wx.ID_ANY, label="File size:")
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
        
        self.Bind(wx.EVT_BUTTON, self.on_ok_button, self.btn_ok)

        self.siz_bottom.AddStretchSpacer()
        self.siz_bottom.Add(self.btn_ok, flag=wx.ALL, border=5)
        self.siz_bottom.Add(self.btn_cancel, flag=wx.ALL, border=5)

        # ----------------------------------------------------------------------
        self.szr_main.Add(self.siz_bottom, flag=wx.EXPAND)
        self.pnl_main.SetSizer(self.szr_main)

        # size the dialog to fit the content managed by the sizer
        self.szr_main.Fit(self)

        # Populate data
        self.cmb_only.SetSelection(filter_data.exclude_files)
        self.txt_fname.AppendText(filter_data.file_names)
        self.cmb_fcmd1.SetSelection(filter_data.file_and_dir)
        self.txt_dname.AppendText(filter_data.dir_names)
        self.cmb_fsiz1.SetSelection(filter_data.cmd_size1)
        self.txt_fsiz1.AppendText(str(filter_data.file_size1))
        self.cmb_fcmd2.SetSelection(filter_data.size1_and_size2)
        self.cmb_fsiz2.SetSelection(filter_data.cmd_size2)
        self.txt_fsiz2.AppendText(str(filter_data.file_size2))

    #---------------------------------------------------------------------------
    def on_ok_button(self, event):
        """ Event called when user presses OK button
            Copy all data from UI elements to filter
        """
        filter_temp = FilterData()
        error_text = None

        if self.cmb_only.GetSelection() != wx.NOT_FOUND:
            filter_temp.exclude_files = self.cmb_only.GetSelection()
        else:
            error_text = "Only Files/Exclude Files not selected"

        filter_temp.file_names = self.txt_fname.GetLineText(0)

        filter_temp.file_and_dir = 0
        if self.cmb_fcmd1.GetSelection() != wx.NOT_FOUND:
            filter_temp.file_and_dir = self.cmb_fcmd1.GetSelection()

        filter_temp.dir_names = self.txt_dname.GetLineText(0)

        filter_temp.cmd_size1 = 0
        if self.cmb_fsiz1.GetSelection() != wx.NOT_FOUND:
            filter_temp.cmd_size1 = self.cmb_fsiz1.GetSelection()

        try:
            filter_temp.file_size1 = int(self.txt_fsiz1.GetLineText(0))
        except:
            error_text = "File size(1) contains invalid value"

        filter_temp.size1_and_size2 = 0
        if self.cmb_fcmd2.GetSelection() != wx.NOT_FOUND:
            filter_temp.size1_and_size2 = self.cmb_fcmd2.GetSelection()

        filter_temp.cmd_size2 = 0
        if self.cmb_fsiz2.GetSelection() != wx.NOT_FOUND:
            filter_temp.cmd_size2 = self.cmb_fsiz2.GetSelection()

        try:
            filter_temp.file_size2 = int(self.txt_fsiz2.GetLineText(0))
        except:
            error_text = "File size(2) contains invalid value"

        if error_text:
            dlg = wx.MessageDialog(self, error_text, "Error", style=wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.filter_data.exclude_files = filter_temp.exclude_files
        self.filter_data.file_names = filter_temp.file_names
        self.filter_data.file_and_dir = filter_temp.file_and_dir
        self.filter_data.dir_names = filter_temp.dir_names
        self.filter_data.cmd_size1 = filter_temp.cmd_size1
        self.filter_data.file_size1 = filter_temp.file_size1
        self.filter_data.size1_and_size2 = filter_temp.size1_and_size2
        self.filter_data.cmd_size2 = filter_temp.cmd_size2
        self.filter_data.file_size2 = filter_temp.file_size2

        self.EndModal(wx.ID_OK)

#---------------------------------------------------------------------------

if __name__ == "__main__" :

    app = wx.App()

    filter1 = FilterData()
    filter1.enabled = True
    filter1.file_names = "*.txt"
    
    dlg = FilterDialog(None, filter1)
    val = dlg.ShowModal()
    if val == wx.ID_OK:
        print("You pressed OK")
        filter1.check("C:\\hello\\world.txt", 0)
    else:
        print("You pressed Cancel")

    print(filter1.dir_names)

    dlg.Destroy()
    app.MainLoop() 