import csv
from model import db, Store, connect_to_db

from server import app
connect_to_db(app)

with open('walmartlocations.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for line in reader:
        if line[0] == 'name':
            continue

        store_info = Store(
            name=line[0],
            address=line[1],
            city=line[2],
            state=line[3],
            zip=line[4],
            phone=line[5],
            hours=line[6],
            lat=float(line[7]),
            long=float(line[8]))
        
        db.session.add(store_info)

db.session.commit()
print("Done")

'''
file = open('walmartlocations.csv')

csvreader = csv.reader(file)


for line in csvreader:
    (
        name,
        address,
        city,
        state,
        zip,
        phone,
        hours,
        lat,
        long,
    ) = line.strip().split(",")

    zip = int(zip)
    lat = float(lat)
    long = float(long)


    store_info = Store(name=name, address=address, city=city, state=state, zip=zip, phone=phone, hours=hours, lat=lat, long=long)

    db.session.add(store_info)

#db.session.commit()

'''