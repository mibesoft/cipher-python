import os
for path, subdirs, files in os.walk('templates/wordpress/Foundation'):
    for name in files:
        print (os.path.join(path, name))