#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
import os
import sys
import filecmp

class TwinFinder:
    """ The module finds duplicate files in multiple locations."""

    def __init__(self):
        self.file_list = []
        self.file_dict = {}
        self.twin_files = []

    def append_files_to_list(self, path):
        """ Using os.walk(path) get all the files inside of <path> location.
            For every file found, create a tuple (<file_size>, <file_name>)
            and add to the global list of files: <file_list>
        """
        # Generate the file names in a directory tree by walking the tree either top-down or bottom-up.
        # For each directory in the tree rooted at directory top (including top itself), 
        # it yields a 3-tuple (<dirpath>, <dirnames>, <filenames>).
        # <dirpath> is a string, the path to the directory. 
        # <dirnames> is a list of the names of the subdirectories in <dirpath> 
        # (including symlinks to directories, and excluding '.' and '..'). 
        # <filenames> is a list of the names of the non-directory files in dirpath.
        #
        # Example, in case of the following directory tree:
        # --+
        #   +--[dir1]
        #   |     +-- fileA.copy
        #   |     +-- fileC.copy
        #   |
        #   +--[dir2]
        #   |     +-- fileB.copy
        #   |
        #   +-- fileA.txt
        #   +-- fileB.txt
        #   +-- fileC.txt
        #
        # The following is generated:
        #   ('.', ['dir1', 'dir2'], ['fileA.txt', 'fileB.txt', 'fileC.txt'])
        #   ('.\\dir1', [], ['fileA.copy', 'fileC.copy'])
        #   ('.\\dir2', [], ['fileB.copy'])

        os_walk_res = os.walk(path)

        # For every file found add a record (tuple) to the <file_list>:
        #  (<file_size>, <file_name>)
        for rec in os_walk_res:
            for file in rec[2]:
                file_name = os.path.join(rec[0], file)
                file_size = os.path.getsize(file_name)
                self.file_list.append((file_size, file_name))

    def scan(self, folder_list):
        """ Search all duplicate files in locations specified in <folder_list>.
            Return a list of found duplicate files ("twins"), where every record from
            the list is a tuple: (file_size, file_name1, file_name2)
        """

        self.file_list.clear()

        # Parse every folder from arguments
        for loc in folder_list:
            # Check folder is a directory
            if not os.path.isdir(loc):
                raise ValueError(f"Invalid location (not a directory): {loc}")
            # Walk the directory, add all found files to the list
            self.append_files_to_list(loc)

        # Sort the list by file_size
        #self.file_list = sorted(self.file_list, key=lambda file_size: file_size[0])

        # Add found files to the dictionary,
        # where the dictionary key is the file size, and the dictionary value
        # is a list of files that have the size:
        #   { 
        #       <size_x> : [file_name1, file_name2],
        #       <size_y> : [file_name3],
        #       <size_z> : [file_name4, file_name5, file_name6]
        #           ...
        #   }
        self.file_dict.clear()
        for (file_size, file_name) in self.file_list:
            # A file with this size has not yet been added? Add now.
            if file_size not in self.file_dict:
                self.file_dict[file_size] = [file_name]
            # A file with this size already exists? Append it to the list.
            else:
                self.file_dict[file_size].append(file_name)

        # Detect duplicate files
        # For every pair of duplicate files the following tuple is added
        # to the <twin_files> list:
        #       (<file_size>, <file_name1>, <file_name2>)
        self.twin_files.clear()
        for f_size, f_list in self.file_dict.items():
            # More than 1 file with the same size?
            while len(f_list) > 1:
                f1 = f_list[0]
                for f2 in f_list[1:]:
                    if filecmp.cmp(f1, f2):
                        self.twin_files.append((f_size, f1, f2))
                f_list = f_list[1:]
        return self.twin_files

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Command arguments missing, no directory specified")
        print("Invoke: twin_finder.py <dir1> [dir2] [dir3] [dirN]")
        print("Nothing to do, exit")
        exit()

    twin_finder = TwinFinder()
    tw_list = twin_finder.scan(sys.argv[1:])
    for t_rec in tw_list:
        print(t_rec)