from flask import Flask

from controllers.controllers import bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')