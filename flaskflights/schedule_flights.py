import calendar
from datetime import *
from time import strftime
import calendar
from flaskflights.models import AvailableFlights, Aircraft


def addToCalender():
    syberJet1 = Aircraft(name='SyberJet 1', model='SJ30i', capacity=6)
    syberJet2 = Aircraft(name='SyberJet 2', model='SJ30i', capacity=6)
    cirrus1 = Aircraft(name='Cirrus 1', model='SF50', capacity=4)
    cirrus2 = Aircraft(name='Cirrus 2', model='SF50', capacity=4)
    hondaJet1 = Aircraft(name='HondaJet 1', model='Elite', capacity=5)
    hondaJet2 = Aircraft(name='HondaJet 2', model='Elite', capacity=5)

    # from dairy flat
    month = calendar.monthcalendar(2022, 6)
    week = [week for week in month]
    for month in range(0, 4):
        for i in range(5):
            dateFlight = week[i][4]
            if dateFlight:
                dairyToRotoSyd = AvailableFlights(timeOfFlight="8:00 A.M.", dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=4,flyingFrom='Dairy Flat',stopsAt='Rotorua', flyingTo='Sydney',aircraft=syberJet1,seatsLeft=syberJet1.capacity)
            dateFlight = week[i][0]
            for day in range(5):
                if dateFlight:
                    toRotoM = AvailableFlights(timeOfFlight="8:00 A.M.",dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=day,flyingFrom='Dairy Flat',stopsAt=None,flyingTo='Rotorua',aircraft=cirrus1,seatsLeft=cirrus1.capacity)
                    toRotoA = AvailableFlights(timeOfFlight="6:00 P.M.",dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=day,flyingFrom='Dairy Flat',stopsAt=None,flyingTo='Rotorua',aircraft=cirrus2,seatsLeft=cirrus2.capacity)
            dateFlight = week[i][1]
            if dateFlight:
                toTuutaT = AvailableFlights(timeOfFlight="1:00 P.M.",dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=1,flyingFrom='Dairy Flat',stopsAt=None,flyingTo='Tuuta', aircraft=hondaJet1,seatsLeft=hondaJet1.capacity)
            dateFlight = week[i][5]
            if dateFlight:
                toTuutaF = AvailableFlights(timeOfFlight="1:00 P.M.",dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=4,flyingFrom='Dairy Flat',stopsAt=None,flyingTo='Tuuta',aircraft=hondaJet1, seatsLeft=hondaJet1.capacity)
            dateFlight = week[i][0]
            if dateFlight:
                toTekapo = AvailableFlights(timeOfFlight="3:00 P.M.", dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=0,flyingFrom='Dairy Flat',stopsAt=None,flyingTo='Tekapo',aircraft=hondaJet2,seatsLeft=hondaJet2.capacity)
            for days in range(0, 6, 2):
                dateFlight = week[i][days]
                if dateFlight:
                    toGBI = AvailableFlights(timeOfFlight="9:00 A.M.",dateOfFlight=strftime("%{}/%{}/%2022".format(dateFlight, month)),dayOfFlight=days,flyingFrom='Dairy Flat', stopsAt=None,flyingTo='Great Barrier Island',aircraft=cirrus1,seatsLeft=cirrus1.capacity)


addToCalender()
