from app import db, create_app
import models

db.create_all(app=create_app())
