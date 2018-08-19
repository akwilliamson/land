with open ('formatted.csv') as f:
    r = f.readlines()

for i in range(len(r)):
    row = r[i]
    number = r[i].split(',')[0][0]
    filename = "tmks_zone_"+number+".csv"
    with open(filename,'a') as f:
        f.write(row)
