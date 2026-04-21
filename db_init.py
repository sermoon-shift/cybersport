from flask_sqlalchemy import SQLAlchemy

from models.base_model import Base

db = SQLAlchemy(model_class=Base)
