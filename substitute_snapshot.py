from shutil import copyfile
day = "1"
src = "points.json"
dst = "substitute_"+day+".json"
copyfile(src, dst)