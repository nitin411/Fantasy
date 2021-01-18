from shutil import copyfile
day = "4"
src = "points.json"
dst = "substitute_"+day+".json"
copyfile(src, dst)