import math
import datetime
import gpx_exporter


LAT_STEP = 1e-5
LNG_STEP = 1e-3
SPEED = 1e-5
TIME_DELTA = 1


class Walker(object):

  def __init__(self, lat, lng, speed=SPEED):
    self.lat = lat
    self.lng = lng
    self.speed = speed

    self.pre_lat = self.lat
    self.pre_lng = self.lng

  def SetSpeed(self, speed):
    self.speed = speed

  def GetCurrPoint(self):
    return (round(self.lat, 5), round(self.lng, 5), datetime.datetime.now())

  def StepNorth(self):
    print 'Moving north.'
    return self.StepDelta(self.speed, 0 )

  def StepSouth(self):
    print 'Moving south.'
    return self.StepDelta(-self.speed, 0)

  def StepEast(self):
    print 'Moving east.'
    return self.StepDelta(0, self.speed)

  def StepWest(self):
    print 'Moving west.'
    return self.StepDelta(0, -self.speed)
  
  def Step(self, direction):
    if direction == 'north':
      return self.StepNorth()
    elif direction == 'south':
      return self.StepSouth()
    elif direction == 'west':
      return self.StepWest()
    elif direction == 'east':
      return self.StepEast()
    else:
      raise

  def StepDelta(self, delta_lat, delta_lng, curr_time=None):
    if not curr_time:
      curr_time = datetime.datetime.now() + datetime.timedelta(seconds=TIME_DELTA)
    self.pre_lat = self.lat
    self.pre_lng = self.lng
    self.lat += delta_lat
    self.lng += delta_lng
    print '(%f, %f) -> (%f, %f)' % (self.pre_lat, self.pre_lng, self.lat, self.lng)
    return (round(self.lat, 5), round(self.lng, 5), curr_time)

  def Hatch(self, hatch_duration=3600):
    points = []
    curr_time = datetime.datetime.now()
    # For one hour.
    for i in range(hatch_duration / 10):
      for j in range(5):
        points.append(self.StepDelta(self.speed, 0, curr_time))
        curr_time += datetime.timedelta(seconds=TIME_DELTA)
      for j in range(5):
        points.append(self.StepDelta(-self.speed, 0, curr_time))
        curr_time += datetime.timedelta(seconds=TIME_DELTA)
    print 'Hatching eggs until %s.' % str(curr_time)
    return points


def main():
  walker = Walker(37, -121)
  points = []
  for i in range(10):
    point = walker.StepSouth()
    points.append(point)
    print point
  gpx_exporter.ToGpxFile(points)
    


if __name__ == '__main__':
  main()