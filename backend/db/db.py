import sqlite3
import sys
from typing import Optional

sys.path.append("/Users/noam/Documents/noam_code")
from todolist.backend import tdlist
from todolist.backend import task

conn = sqlite3.connect(
    "/Users/noam/Documents/noam_code/todolist/backend/db/my_todo_app.db",
    check_same_thread=False,
)

create_todo_lists_sql = """
CREATE TABLE IF NOT EXISTS todo_lists (
    list_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
"""

create_tasks_sql = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (list_id) REFERENCES todo_lists (list_id),
    UNIQUE(task_id, list_id)
);
"""

# with conn:
#     conn.execute(create_todo_lists_sql)
#     conn.execute(create_tasks_sql)
# conn.execute("INSERT INTO todo_lists (name) VALUES (?)", ("Groceries",))
# cur = conn.execute("DELETE FROM todo_lists")
# lists = cur.fetchall()
# print(lists)


def create_new_list_in_db(tdlist: tdlist.TDList):
    # conn = sqlite3.connect("my_todo_app.db")
    sql_check = f"SELECT * FROM todo_lists WHERE name = '{tdlist.list_name}';"
    sql = f"INSERT INTO todo_lists (name) VALUES ('{tdlist.list_name}');"
    with conn:
        result = conn.execute(sql_check)
        if result.fetchone():
            return "List name already exists", 400
        else:
            conn.execute(sql)
            return "Created_new_list", 200


def select_list(tdlist: Optional[tdlist.TDList] = None):
    # conn = sqlite3.connect("my_todo_app.db")
    if tdlist:
        sql = f"SELECT * FROM todo_lists where name = '{tdlist.list_name}'"
    else:
        sql = "SELECT * FROM todo_lists"
    with conn:
        result = conn.execute(sql)
        output = []
        for row in result:
            output.append(row)
        return output, 200


def select_tasks_from_list(tdlist: tdlist.TDList):
    # conn = sqlite3.connect("my_todo_app.db")
    sql = f"SELECT * FROM tasks where list_id = {tdlist.list_id}"
    with conn:
        result = conn.execute(sql)
        output = []
        for row in result:
            output.append(row)
        return output, 200


def select_task_by_task_id(task: task.Task):
    sql = f"SELECT * FROM tasks where task_id = {task.task_id}"
    with conn:
        result = conn.execute(sql)
        output = []
        for row in result:
            output.append(row)
        return output, 200


def select_all_tasks():
    # conn = sqlite3.connect("my_todo_app.db")
    sql = f"SELECT * FROM tasks"
    with conn:
        result = conn.execute(sql)
        output = []
        for row in result:
            output.append(row)
        return output, 200


def insert_task_to_list(task: task.Task):
    # SQL statement to insert a new task
    if task.task_id:
        insert_task_sql = """
        INSERT INTO tasks (task_id, list_id, description, completed)
        VALUES (?, ?, ?, ?);
        """
    else:
        insert_task_sql = """
        INSERT INTO tasks (list_id, description, completed)
        VALUES (?, ?, ?);
        """
    # conn = sqlite3.connect("my_todo_app.db")
    with conn:
        cursor = conn.cursor()
        # Execute the INSERT statement
        if task.task_id:
            cursor.execute(
                insert_task_sql,
                (task.task_id, task.list_id, task.description, task.completed),
            )
        else:
            cursor.execute(
                insert_task_sql, (task.list_id, task.description, task.completed)
            )
        return "Succesful", 200


def delete_task_from_list(task: task.Task):
    # SQL statement to delete a task
    delete_task_sql = "DELETE FROM tasks WHERE task_id = ?;"

    with conn:
        # Connect to your SQLite database
        cursor = conn.cursor()
        # Execute the DELETE statement
        cursor.execute(delete_task_sql, (task.task_id,))
    return "Succesful", 200


def delete_list(tdlist: tdlist.TDList):
    # Assumes there list_id is valid
    with conn:
        cursor = conn.cursor()

        # Delete tasks associated with the list_id
        cursor.execute("DELETE FROM tasks WHERE list_id = ?", (tdlist.list_id,))

        # Delete the list from todo_lists
        cursor.execute("DELETE FROM todo_lists WHERE list_id = ?", (tdlist.list_id,))


def assert_task_id_and_list_correspond(task_id, list_id):
    try:
        list_id = int(list_id)
        task_id = int(task_id)
    except:
        return (
            f"Both of List_ID and Task_ID must be Integers: {list_id}, {task_id}",
            400,
        )
    task1 = task.Task(task_id=task_id, list_id=list_id, description="", completed=False)
    result = select_task_by_task_id(task1)[0]
    if len(result) != 1:
        return (
            f"task does not exist with task_id: {task_id} and list_id: {list_id}",
            400,
        )
    found_task = result[0]
    if found_task[1] != list_id:
        return (
            f"found task's list id does not match what was provided: list_id: {list_id}, found_list_id: {found_task[1]}",
            400,
        )
    else:
        return found_task, 200


if __name__ == "__main__":
    print(select_list())
    # tdl1 = tdlist.TDList(list_name="hey", list_id=1)
    # tdl2 = tdlist.TDList(list_name="bye", list_id=1)
    # create_new_list_in_db(tdl1)
    # create_new_list_in_db(tdl2)
    # # list = select_list(name="l1")
    # # id = list.fetchone()[0]
    # # print(id)
    # # print(delete_list(tdlist=tdl1))
    # # print(select_list())
    # # # print(f"list id: {id}")
    # t1 = task.Task(description="heyyooo", completed=False, list_id=1)
    # insert_task_to_list(t1)
    # t2 = task.Task(description="wassup", completed=False, list_id=1)
    # insert_task_to_list(t2)

    # t1 = task.Task(description="see you", completed=False, list_id=2)
    # insert_task_to_list(t1)
    # t2 = task.Task(description="ciao", completed=False, list_id=2)
    # insert_task_to_list(t2)

    # # print(select_tasks_from_list(tdl1))
    print(select_all_tasks())
    # delete_task_from_list(task=t1)
    # for i in select_tasks_from_list(id):
    #     print(i)
    # print("\n")
    # insert_task_to_list(task=t1)
    # for i in select_tasks_from_list(id):
    #     print(i)
    # print("after")
    # for i in select_tasks_from_list(id):
    #     print(i)
