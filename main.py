from alfieBackend.app import create_app
from flask import jsonify

app=create_app()

if __name__=="__main__":
    app.run(debug=True)