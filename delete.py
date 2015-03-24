# This is a script to delete all migration files and the database
# Allows us to quickly "reset" the database

import os
import shutil

paths = ['api']

for path in paths:
    folder = os.path.join(path, 'migrations')
    try:
        shutil.rmtree(folder)
    except:
        print "couldn't delete %s" % folder
    else:
        print "deleted from %s" % folder

try:
    os.remove('db.sqlite3')
except:
    print "failed to delete db"
