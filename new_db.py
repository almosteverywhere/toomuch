import models
from models import db
models.db.drop_all()
models.db.create_all()

# stuff to understand, how do python package importing works
