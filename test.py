__author__ = 'kurtis'


from AISManager import AISManager

print "Starting now!"

manager = AISManager()
manager.start_scanning()

while len(manager.get_boats()) < 10:
    print "We have " + str(len(manager.get_boats())) +  " boats"

print vars(manager.get_boats())


