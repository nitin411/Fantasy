from shutil import copyfile
day = "3"
src = "points.json"
dst = "substitute_"+day+".json"
copyfile(src, dst)