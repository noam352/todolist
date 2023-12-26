from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

import sys

sys.path.append("/Users/noam/Documents/noam_code")

from todolist.backend import task, tdlist
from todolist.backend.db import db


app = Flask(__name__)


@app.route("/")
def home():
    pass


@app.route("/lists", methods=["POST"])
@cross_origin()
def create_list():
    if request.content_type == "application/json":
        data = request.json
        if "list_name" not in data:
            return "list_name must be provided", 400
        elif not isinstance(data["list_name"], str):
            return jsonify("list_name must be a string"), 400
        elif len(data["list_name"]) > 45:
            return "list_name must not be longer than 45 characters", 400
        new_list = tdlist.TDList(list_name=data["list_name"])
        return db.create_new_list_in_db(new_list)
    else:
        return "Unsupported Media Type", 415


@app.route("/lists/<list_id>", methods=["DELETE"])
@cross_origin()
def delete_list(list_id):
    try:
        list_id = int(list_id)
    except:
        return "list_id must be an integer", 400
    new_list = tdlist.TDList(list_name=None, list_id=list_id)
    db.delete_list(new_list)
    return f"Succesfuly deleted list with list_id: {list_id}", 200


@app.route("/lists/search", methods=["GET", "POST"])
@cross_origin()
def search_list():
    if request.content_type == "application/json":
        data = request.json
        if "list_name" not in data:
            return "list_name must be provided", 400
        elif not isinstance(data["list_name"], str):
            return "list_name must be a string", 400
        elif len(data["list_name"]) > 45:
            return "list_name must not be longer than 45 characters", 400
        searched_list = tdlist.TDList(list_name=data["list_name"])
        result = db.select_list(tdlist=searched_list)[0]
        if len(result) == 0:
            return f"List does not exist with specified name: {data['list_name']}", 400
        found_list = result[0]
        list_id, list_name = found_list
        searched_list.set_id(list_id=list_id)
        found_tasks = db.select_tasks_from_list(searched_list)
        tasks = [
            task.Task(
                task_id=task_id,
                list_id=list_id,
                description=description,
                completed=completed,
            ).__dict__
            for task_id, list_id, description, completed in found_tasks[0]
        ]
        output = {"list_id": list_id, "tasks": tasks}
        return jsonify(output), 200
    else:
        return "Unsupported Media Type", 415


@app.route("/lists/<list_id>/tasks", methods=["POST"])
@cross_origin()
def add_task_to_list(list_id):
    if request.content_type == "application/json":
        data = request.json
        if "list_name" not in data:
            return "list_name must be provided", 400
        elif not isinstance(data["list_name"], str):
            return "list_name must be a string", 400
        elif len(data["list_name"]) > 45:
            return "list_name must not be longer than 45 characters", 400
        else:
            try:
                list_id = int(list_id)
            except:
                return f"List_ID must be an integer {list_id} is not", 400
        searched_list = tdlist.TDList(list_name=data["list_name"])
        result = db.select_list(tdlist=searched_list)[0]
        if len(result) == 0:
            return f"List does not exist with specified name: {data['list_name']}", 400
        found_list = result[0]
        found_list_id, found_list_name = found_list
        if found_list_id != list_id:
            return (
                f"List_Id specified does not match list_id associacted with the provided List_Name: {data['list_name']}",
                400,
            )
        t = task.Task(
            list_id=list_id,
            description=data.get("description", None),
            completed=data.get("completed", False),
        )
        db.insert_task_to_list(t)
        return "Succesful", 200
    else:
        return "Unsupported Media Type", 415


@app.route("/lists/<list_id>/tasks/<task_id>", methods=["DELETE"])
@cross_origin()
def delete_task_from_list(list_id, task_id):
    return_message, status_code = db.assert_task_id_and_list_correspond(
        list_id=list_id, task_id=task_id
    )
    if status_code == 400:
        return return_message, status_code
    task1 = task.Task(task_id=task_id, list_id=list_id, description="", completed=False)
    return db.delete_task_from_list(task=task1)


@app.route("/lists/<list_id>/tasks/<task_id>", methods=["PUT"])
@cross_origin()
def update_task_in_list(list_id, task_id):
    if request.content_type == "application/json":
        data = request.json
        return_message, status_code = db.assert_task_id_and_list_correspond(
            list_id=list_id, task_id=task_id
        )
        if status_code == 400:
            return return_message, status_code
        elif "description" not in data:
            return "description must be in the payload", 400
        task1 = task.Task(
            task_id=task_id, list_id=list_id, description="", completed=False
        )
        db.delete_task_from_list(task=task1)
        task1.description = data["description"]
        db.insert_task_to_list(task=task1)
        return "Succesful", 200
    else:
        return "Unsupported Media Type", 415


@app.route("/lists/<list_id>/tasks/<task_id>/complete", methods=["PUT"])
@cross_origin()
def complete_task_from_list(list_id, task_id):
    return_value, status_code = db.assert_task_id_and_list_correspond(
        list_id=list_id, task_id=task_id
    )
    if status_code == 400:
        return return_value, status_code
    task1 = task.Task(task_id=task_id, list_id=list_id, description="", completed=False)
    db.delete_task_from_list(task=task1)
    task2 = task.Task(
        task_id=task_id, list_id=list_id, description=return_value[2], completed=True
    )
    return db.insert_task_to_list(task=task2)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
