__author__ = 'Kurtis Harms'
import datetime
from PositionReport import PositionReport

class Boat:
    def __init__(self, boat_id):
        self.boat_id = boat_id
        self.position_reports = []
        self.is_accurate = False

    def get_id(self):
        return self.boat_id

    def get_position_reports(self):
        return self.position_reports

    def get_latest_position_report(self):
        return self.position_reports[-1]

    def add_position_report(self, position_report):
        self.position_reports.append(position_report)

    def report_position(self, latitude, longitude, heading, speed, is_accurate):
        self.position_reports.append(PositionReport(datetime.datetime.now(), latitude, longitude, heading, speed, is_accurate))
        self.is_accurate = False

    def is_accurate(self):
        return self.is_accurate
