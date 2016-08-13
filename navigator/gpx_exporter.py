import datetime
import logging


FILE_NAME = './data/pokemonData.gpx'
XML_TAG = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>'
GPX_OPEN_TAG = '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="mapstogpx.com" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">'
GPX_CLOSE_TAG = '</gpx>'
TIME_TEMPLATE = '2016-%02d-%02dT%02d:%02d:%02dZ'
WPT_TEMPLATE = '<wpt lat="%f" lon="%f"><time>%s</time></wpt>'


def ToGpxTag(lat, lng, time):
  time_tag = TIME_TEMPLATE % (time.month, time.day, time.hour, time.minute, time.second)
  wpt_tag = WPT_TEMPLATE % (lat, lng, time_tag)
  return wpt_tag


def ToGpxFile(points):
  print 'Writing GPX data to %s.' % FILE_NAME
  with open(FILE_NAME, 'w') as f:
    f.write(XML_TAG + '\n')
    f.write(GPX_OPEN_TAG+ '\n')
    for lat, lng, time in points:
      wpt = ToGpxTag(lat, lng, time)
      f.write('  ' + wpt + '\n')
    f.write(GPX_CLOSE_TAG + '\n')


def main():
  points = [
      [37.0, 122, datetime.datetime(2016, 1, 1, 6, 0, 1)],
      [37.1, 122.1, datetime.datetime(2016, 1, 1, 6, 0, 2)],
  ]
  ToGpxFile(points)
  

if __name__ == '__main__':
  main()
