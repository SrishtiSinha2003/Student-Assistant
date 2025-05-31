#This is the entry point of your app.
#When you want to run your Flask app, you will run this file.

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(pport=5000 , debug=True)