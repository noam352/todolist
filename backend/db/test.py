import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect("my_todo_app.db")
cursor = conn.cursor()

# Execute the query to get table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results from the executed query
tables = cursor.fetchall()

# Print the names of the tables
for table in tables:
    print(table[0])

# Close the connection
conn.close()
