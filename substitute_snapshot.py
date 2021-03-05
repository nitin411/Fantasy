from shutil import copyfile
day = "2"
src = "points.json"
dst = "substitute_"+day+".json"
copyfile(src, dst)
