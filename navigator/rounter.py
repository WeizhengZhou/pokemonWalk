import sys
from datetime import datetime
from datetime import timedelta
from geopy.distance import vincenty
import random
# import applescript



SPEED = 3
STAY_TIME = 360
STOP_RANGE = 1e-5
xml_tag = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
gpx_open_tag = '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="mapstogpx.com" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">'
gpx_close_tag = '</gpx>'
time_template = '2016-%02d-%02dT%02d:%02d:%02dZ'
wpt_template = '<wpt lat="%f" lon="%f"><time>%s</time></wpt>'


def GetDistance(start, end):
  dist = vincenty(start, end).meters
  return dist


def GomputeLocation(start, end, trip_time, t):
  lat_speed = (end[0] - start[0]) / trip_time
  lon_speed = (end[1] - start[1]) / trip_time
  return (round(start[0] + t * lat_speed, 5), round(start[1] + t * lon_speed, 5)) 


def GetTag(time, lat, lng):
  time_tag = time_template % (time.month, time.day, time.hour, time.minute, time.second)
  wpt_tag = wpt_template % (lat, lng, time_tag)
  return wpt_tag

def Route(points):
  start_point = points[0]
  end_point = points[1]

  trip_time = int(GetDistance(start_point, end_point) / SPEED)
  trip_time = max(trip_time, 1)

  time = datetime.utcnow()
  print str(start_point) + ' -> ' + str(end_point) + ', trip_time = ' + str(trip_time)

  wpt_tags = []
  for i in xrange(trip_time):
    lat, lon = GomputeLocation(start_point, end_point, trip_time, i)  
    time += timedelta(seconds=1)
    wpt_tags.append(GetTag(time, lat, lon))
  for i in xrange(STAY_TIME):
    time += timedelta(seconds=1)
    wpt_tags.append(GetTag(
      time,
      end_point[0] + random.random() * STOP_RANGE, 
      end_point[1] + random.random() * STOP_RANGE, ))

  WriteToFile(wpt_tags)


def WriteToFile(wpt_tags):
  gpx_filename = 'pokemonData.gpx'
  print 'wrting to file: ' + gpx_filename
  with open(gpx_filename, 'w') as f:
    f.write(xml_tag + '\n')
    f.write(gpx_open_tag+ '\n')
    for wpt in wpt_tags:
      f.write('  ' + wpt + '\n')
    f.write(gpx_close_tag)



cmd = """

delay 0.01
activate application "Xcode"
tell application "System Events"
  tell process "Xcode"
    click menu item "pokemonData" of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1
  end tell
end tell
tell application "Xcode"
  set miniaturized of window 1 to true
end tell
activate application "Google Chrome"

"""

def RunXcode():
  applescript.AppleScript(cmd).run()


def main():
  # p1 = (37.8071,-122.4315)
  # delta_lng = -1e-3
  # delta_lat = 1e-3
  p1 = (37.8076, -122.4292)
  delta_lng = -1e-6
  delta_lat = 1e-6

  p2 = (p1[0] + delta_lng, p1[1] + delta_lat)
  Route([p1, p2])
  # Route([(37.8071,-122.4315), (37.8075, -122.435)])
  
  RunXcode()

  

if __name__ == '__main__':
  main()
