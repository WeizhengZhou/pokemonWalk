import sys
from datetime import datetime
from datetime import timedelta

from geopy.geocoders import Nominatim
from geopy.distance import vincenty


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

def ReadPoints(filename):
  print 'reading from: ' + filename
  points = []
  with open(filename + '.txt') as f:
    for row in f:
      if len(row) == 1:
        continue
      point = row.split(',')
      lat = round(float(point[0]), 5)
      lng = round(float(point[1]), 5)
      points.append((lat, lng))
  return points

def GenerateTrip(start, end, start_time, speed):
  dist = round(GetDistance(start, end), 3)
  trip_time = int(dist / speed)
  print str(start) + ' -> ' + str(end) +  ', dist: ' + str(dist) + ', start_time: ' + str(start_time)
  wpt_tags = []
  for i in xrange(trip_time):
    lat, lon = GomputeLocation(start, end, trip_time, i)
    time = start_time + timedelta(seconds=i)
    time_tag = time_template % (time.month, time.day, time.hour, time.minute, time.second)
    wpt_tag = wpt_template % (lat, lon, time_tag)
    wpt_tags.append(wpt_tag)
  return wpt_tags, trip_time

def GererateTrips(points, start_time, speed):
  wpt_tags = []
  round_duration = 0
  for i in range(len(points) - 1):
    tags, trip_duration = GenerateTrip(points[i], points[i + 1], start_time, speed)
    wpt_tags.extend(tags)
    round_duration += trip_duration
    start_time += timedelta(seconds=trip_duration)
  return wpt_tags, round_duration

def Route(points=[], speed=1.5, filename='data', n_run=10):
  if len(points) == 1:
    points.append((points[0][0] + 2e-5, points[0][1] + 2e-5))
  wpt_tags = []
  start_time = datetime.utcnow()
  total_duration = 0
  for i in range(n_run):
    tags, round_duration = GererateTrips(points, start_time, speed)
    wpt_tags.extend(tags)
    start_time += timedelta(seconds=round_duration)
    total_duration += round_duration

  print 'total_duration: ' + str(total_duration) + ', num_points: ' + str(len(wpt_tags))

  gpx_filename = filename + '.gpx'
  print 'wrting to file: ' + gpx_filename
  with open(gpx_filename, 'w') as f:
    f.write(xml_tag + '\n')
    f.write(gpx_open_tag+ '\n')
    for wpt in wpt_tags:
      f.write('  ' + wpt + '\n')
    f.write(gpx_close_tag)


def main():
  args = sys.argv
  speed = float(sys.argv[1])
  filename = args[2]
  n_run = int(args[3]) if len(args) > 2 else None

  Route(ReadPoints(filename), speed, filename, n_run)
  

if __name__ == "__main__":
    main()


