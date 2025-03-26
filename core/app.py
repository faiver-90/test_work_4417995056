from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.controllers import bp
from models.model import Base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

with engine.begin() as conn:
    Base.metadata.create_all(conn)

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
