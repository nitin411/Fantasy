from shutil import copyfile
day = "3"
src = "points.json"
dst = "substitute_"+day+".json"

with open(src,'r') as f:
    points = f.read()
    snapshot = points.replace('data =', 'data_day_{} ='.format(day))

with open(dst, 'w') as f:
    f.write(snapshot)
