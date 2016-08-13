import json
import time

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map

import navigator
import gpx_exporter
import walker as walker_module
import simulate_location

app = Flask(__name__)

MAP_KEY = 'AIzaSyBqOJSlg7MMZC3Tl-K8BaD74PJ8t3ZEp30'


walker = walker_module.Walker(37.7915, -122.3896)

@app.route('/')
def index():
	# pdb.set_trace()
  return render_template('index.html', auto_refresh=True)


@app.route('/set_loc', methods=['POST'])
def set_lat_lng():
  # global PRE_LAT, PRE_LNG

  # lat = float(request.args.get('lat', ''))
  # lng = float(request.args.get('lon', ''))
  
  # print str(lat) + ',' + str(lng)
  # navigator.Route([(PRE_LAT, PRE_LNG), (lat, lng)])
  
  # PRE_LAT = lat
  # PRE_LNG = lng
  return 'ok'

@app.route('/step', methods=['POST'])
def step():
  global walker

  direction= request.args.get('direction', 'north')
  prev_point = walker.GetCurrPoint()
  curr_point = walker.Step(direction)
  gpx_exporter.ToGpxFile([prev_point, curr_point])
  print (prev_point, curr_point)
  
  simulate_location.RunXcode()

  response = {
    'data': {
        'lat': curr_point[0],
        'lng': curr_point[1],
    }
  }
  
  return json.dumps(response)


@app.route('/speed', methods=['POST'])
def speed():
  global walker

  mode = request.args.get('mode', 'slow')
  x = int(mode[1:])
  walker.SetSpeed(x * 1e-5) 
     
  print 'Set speed = %f' % walker.speed
  return 'ok'


@app.route('/hatch', methods=['POST'])
def hatch():
  global walker

  walker.SetSpeed(5 * 1e-5) 
  
  points = walker.Hatch(hatch_duration=3600)
  gpx_exporter.ToGpxFile(points)
  simulate_location.RunXcode() 

  print 'hatcing eggs until %s' % points[-1][2]
  return 'ok'





if __name__ == "__main__":
    app.run(debug=True)