from flask import Flask
from database import create_table
from routes import task_routes


app = Flask(__name__)

create_table()

app.register_blueprint(task_routes)


if __name__ == "__main__":
    app.run(debug=True)