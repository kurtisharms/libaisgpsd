__author__ = 'Kurtis Harms'
import datetime

class PositionReport:
    def __init__(self, date_time, latitude, longitude, heading, speed, is_accurate):
        self.date_time = date_time
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading
        self.speed = speed
        self.is_accurate = is_accurate


    def get_date_time(self):
        return self.date_time

    def get_date(self):
        pass

    def get_time(self):
        pass

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_speed(self):
        return self.speed