from flask import Flask
from flask import request 
from flask import abort
from flask import jsonify
import random


endpoint1_rectangle = {
  "top_left":(5,10),
  "bottom_right":(10,5)
}
enpoint2_rectangle = [
  {
    "id":1,
    "rectangle": {
      "top_left":(5,10),
      "bottom_right":(10,5)
    }
  },
  {
    "id":2,
    "rectangle":{
    "top_left":(7,7),
    "bottom_right":(20,2)
    }
  },
  {
    "id":3,
    "rectangle":{
      "top_left":(33,45),
      "bottom_right":(52,23)
    }
  },
]

app = Flask(__name__)



#RESTful API 1:
#To run : curl -i -H "Content-Type: application/json" -X POST -d '{"point":[6,7]}' http://127.0.0.1:5000/is_point_covered

@app.route('/is_point_covered', methods=['POST'])
def is_point_covered():
  """   
  Determines if a point is in a known rectangle 

  Request: JSON payload containing an array for X and Y values {"point":[X,Y]}

  Response: JSON payload returning true or false 

  """

  if not request.json or not 'point' in request.json:
    abort(400)

  pointGiven=request.json
  rec= endpoint1_rectangle
  covered = False

  if (((rec['top_left'][0])<(pointGiven["point"][0])<(rec['bottom_right'][0])) and 
    ((rec['bottom_right'][1])<(pointGiven["point"][1])<(rec['top_left'][1]))): 
    covered=True

  return jsonify({'is_point_covered': covered}), 201


#RESTful API 2:
#To run: curl --header "Content-Type: application/json" --request POST --data '{"point":[40,50]}' http://127.0.0.1:5000/point_covered_by

@app.route('/point_covered_by', methods=['POST'])
def point_covered_by():  
  """
  Given a point, it returns the id of all known rectangles that covers that point 

  Request: JSON payload containing an array for X and Y values {"point:[X,Y]"}

  Response: JSON payload returning an array of all the rectangle ids that cover the given point 
  """
  if not request.json or not 'point' in request.json:
    abort(400)

  pointGiven=request.json
  enpoint= enpoint2_rectangle
  rectangleResult=[]
  
  x=0
  for rectangle in enpoint:
    rec= rectangle['rectangle']
    if (((rec['top_left'][0])<(pointGiven["point"][0])<(rec['bottom_right'][0])) and 
      ((rec['bottom_right'][1])<(pointGiven["point"][1])<(rec['top_left'][1]))): 
        rectangleResult.append(rectangle['id'])
    x=x+1
  return jsonify({'rectangle_ids': rectangleResult})


#Restful API 3:
#To run: curl --header "Content-Type: application/json" --request POST --data '{"top_left":[7,9],"bottom_right":[8,6]}' http://127.0.0.1:5000/random_covered_point

@app.route('/random_covered_point', methods=['POST'])
def random_covered_point():
  """
  It returns a random point that lies in a rectangle 

  Request: JSON payload containing a rectangle, which is made up of a top left and bottom right point '{"top_left":[X,Y],"bottom_right":[X,Y]}'

  Response: JSON payload containing a point that is within the rectangle 
  """
  if not request.json or (not 'top_left' in request.json) or (not 'bottom_right' in request.json):
    abort(400)

  rectangle= request.json

  topLeftLimitX= rectangle['top_left'][0]
  topLeftLimitY= rectangle['top_left'][1]
  bottomRightLimitX= rectangle['bottom_right'][0]
  bottomRightLimitY= rectangle['bottom_right'][1]

  limitX= random.randrange(topLeftLimitX,bottomRightLimitX)
  limitY= random.randrange(bottomRightLimitY,topLeftLimitY)
  return jsonify({'point:':[limitX,limitY] })

#This must remain at the bottom of the file
if __name__ == "__main__":
  app.run()

