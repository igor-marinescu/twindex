import fnmatch

filters = "*.txt;   *.jpg  ;  hello*.png; some*  ; *.png  "
files = ["some_text.txt", "some_img.jpg", "png_file.png", "123.png"]

filter_list = filters.split(";")

for file in files:
    for f in filter_list:
        f = f.strip()
        if not f:
            continue
        if fnmatch.fnmatch(file, f):
            print(f"{file} matches {f}")
        else:
            print(f"{file} does not matche {f}")
