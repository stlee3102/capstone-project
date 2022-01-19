import csv
from model import db, Store, connect_to_db

from server import app
connect_to_db(app)

with open('walmartlocations.csv', 'r') as csvfile:

    #cvs.reader returns an array
    reader = csv.reader(csvfile, delimiter=',')

    for line in reader:

        #skip headings line
        if line[0] == 'name': 
            continue

        #fill in store info
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
