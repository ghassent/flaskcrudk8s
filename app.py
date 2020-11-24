from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import socket
from flask_cors import CORS
import pymongo
from pymongo import ReplicaSetConnection
from pymongo import ReadPreference


app = Flask(__name__)
# |======== CORS CONFIG =========|
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# app.config["MONGO_URI"] = "mongodb://mongo-0:27017"
# mongo = PyMongo(app)
#
# ##Create a MongoDB client
# client = pymongo.MongoClient('mongodb://35.222.235.16:30805/')
#
# ##Specify the database to be used
# db = client.test
# db = ReplicaSetConnection('35.184.143.42:30805,35.184.143.42:31215,35.184.143.42:30641', replicaSet='rs0')['test']
# client = pymongo.MongoClient("mongodb://34.68.254.194:31623,34.68.254.194:31926/?replicaSet=rs0")
client = pymongo.MongoClient("mongodb://mongo-0.mongo:27017,mongo-1.mongo:27017,mongo-2.mongo:27017/?replicaSet=rs0")

db = client.test

# db = mongo.db
@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome ..................... to Tasks app! I am running inside {} pod!".format(hostname)
    )
@app.route("/tasks")
def get_all_tasks():
    tasks = db.task.find()
    data = []
    for task in tasks:
        item = {
            "ID": str(task["_id"]),
            "TASK": task["task"]
        }
        data.append(item)
    return jsonify(
        data=data
    )
@app.route("/task", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    db.task.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )
@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = db.task.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = db.task.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    db.task.remove()
    return jsonify(
        message="All Tasks deleted!"
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# #from mongoengine import connect
# #from pymongo import ReplicaSetConnection
#
# from pymongo import ReplicaSetConnection
# from pymongo import ReadPreference
#
# db = ReplicaSetConnection('35.184.143.42:30805,35.184.143.42:31215', replicaSet='rs0')['test']
# #db.read_preference = ReadPreference.SECONDARY
# #db.secondary_acceptable_latency_ms = 0.001
#
# #print(ReplicaSetConnection("mongo-0.mongo:27017", replicaSet='rs0'))
# #db  = connect(
# #    'test',
# #    host='35.184.143.42',
# #    port=30805
# #)
#
# #db = connect('test', host='mongodb://35.184.143.42:30805', replicaSet='rs0')
#
# #client = pymongo.MongoClient('mongodb://35.184.143.42:30805')
#
# ##Specify the database to be used
# #db = client.test
#
# ##Specify the collection to be used
# print(db)
#
# col = db.myTestCollection
#
# #print(col)
#
# ##Insert a single document
# col.insert({'hello':'world11'})
#
# ##Find the document that was previously written#
# x = db.myTestCollection.find({})
# for i in x:
# ##Print the result to the screen
#     print(i)
#
# ##Close the connection
#client.close()