# AISManager.py
__author__ = 'Kurtis Harms'
import datetime, threading, time
import os
import gps
from subprocess import check_output
import Boat

class AISManager:
    def __init__(self):
        self.port = 'ttyACM0'
        self.gpsd_ip = 'localhost'
        self.gpsd_port = '2947'
        self.gpsd_report_type = 'AIS'
        self.is_scanning = False
        self.start_gpsd()
        self.session = self.create_session()
        self.scan_thread = threading.Thread(target=self.__scan_ais)
        self.boats = []

    # def __init__(self, port):
    #     self.__init__()
    #     self.port = port
    #
    # def __init__(self, port, gpsd_ip, gpsd_port, gpsd_report_type):
    #     self.__init__()
    #     self.port = port
    #     self.gpsd_ip = gpsd_ip
    #     self.gpsd_port = gpsd_port
    #     self.gpsd_report_type = gpsd_report_type

    def start_gpsd(self):
        # This function will check if there is an instance of GPSD running
        # If there is, it will not do anything
        # If there isn't, it will start an instance of gpsd
        gpsd_pid = self.get_pid('gpsd')
        if gpsd_pid == -1:
            # Okay, so no gpsd process is running. Let's start one!
            # We will not wait for it to start
            #gpsd_pid = os.spawnlp(os.P_NOWAIT, "gpsd")
            os.system('sudo gpsd -D 5 -N -n /dev/' + self.port)
            return
        else:
            # GPSD is already running! Let's just return. We might stop and retstart it here in the future
            return

    def get_pid(self, name):
        # Inspired by:
        # http://stackoverflow.com/questions/26688936/python-how-to-get-pid-by-process-name
        try:
            return int(check_output(["pidof", "-s", name]))
        except:
            return -1

    def create_session(self):
        session = gps.gps(self.gpsd_ip, self.gpsd_port)
        session.stream(gps.WATCH_ENABLE)
        return session

    def start_scanning(self):
        if not self.is_scanning:
            self.scan_thread.start()
            self.is_scanning = True

    def stop_scanning(self):
        # TODO this needs to have the is_scanning attribute checked by the thread for this to work
        if self.is_scanning:
            self.is_scanning = False

    def __scan_ais(self):
        while True:
            try:
                report = self.session.next()
                # Wait for a 'TPV' report and display the current time
                # To see all report data, uncomment the line below
                # print report
                if report['class'] == self.gpsd_report_type:
                    # Okay, let's create a Position Report and assign to a boat in our database of boats
                    boat = self.__get_boat_for_id(report['mmsi'])
                    # TODO make sure that this still works, even if some attributes are working
                    boat.report_position(report['lat'], report['lon'], report['heading'], report['speed'], report['accuracy'])

            except StopIteration:
                session = None
                print "GPSD has terminated"
            except KeyError:
                # TODO We need a better way of handling this when boats send incompete information!
                pass

    def get_boats(self):
        return self.boats

    # This function creates a boat with the given ID if it doesn't already exist
    # Returns existing boat if it exists, otherwise returns a new boat!
    def __get_boat_for_id(self, id):
        try:
            return self.get_boat(id)
        except LookupError:
            boat = Boat.Boat(id)
            self.boats.append(boat)
            return boat

    # This function returns a boat with the given ID if it exists, otherwise raises a LookupError
    def get_boat(self, id):
        for boat in self.boats:
            if boat.get_id() == id:
                return boat
        raise LookupError('No boat with that ID exists!')


