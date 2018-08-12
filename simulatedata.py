from influxdb import InfluxDBClient
from datetime import datetime
import random
import time, sys


influxdb_server = 'localhost'
influxdb_port = 8086
databaseName = 'simhome'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

influxCl = InfluxDBClient(influxdb_server, influxdb_port, '', '', databaseName)
influxCl.create_database(databaseName)
buf = []
data_name = "temperature"
room = "outdoor"
value = 0
import pyowm


from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

def get_temp():
    owm = pyowm.OWM(API_key='5260a0d3bc6c64d64538e574d18680ae')
    observation = owm.weather_at_place('The Hague,nl')
    w = observation.get_weather()
    fields = w.get_temperature('celsius')
    del fields["temp_kf"]
    #w = observation.to_JSON() #{"reception_time": 1534010670, "Location": {"name": "The Hague", "coordinates": {"lon": 4.31, "lat": 52.08}, "ID": 2747372, "country": "NL"}, "Weather": {"reference_time": 1534010100, "sunset_time": 1534014813, "sunrise_time": 1533961262, "clouds": 20, "rain": {}, "snow": {}, "wind": {"speed": 5.1, "deg": 250}, "humidity": 59, "pressure": {"press": 1021, "sea_level": null}, "temperature": {"temp": 290.84, "temp_kf": null, "temp_max": 291.15, "temp_min": 290.15}, "status": "Clouds", "detailed_status": "few clouds", "weather_code": 801, "weather_icon_name": "02d", "visibility_distance": 10000, "dewpoint": null, "humidex": null, "heat_index": null}}

    buf = [{  "measurement": data_name,
                    "time": datetime.now().strftime(DATE_FORMAT),
                    "fields": fields,
                    "tags": {
                        "room": room,
                    }
                }]
    value = fields["temp"]+random.random()
    buf = buf + [{  "measurement": data_name,
                    "time": datetime.now().strftime(DATE_FORMAT),
                    "fields": {
                        "temp": value
                    },
                    "tags": {
                        "room": "livingroom",
                    }
                }]
    print(buf)
    influxCl.write_points(buf)
sched.add_job(get_temp, 'interval', minutes=5)
sched.start()
try:
    while 1:
        time.sleep(200)
except KeyboardInterrupt:
    sys.exit(0)
#sched.shutdown()

