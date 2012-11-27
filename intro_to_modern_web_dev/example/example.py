from flask import Flask, render_template

from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Initialize the database, which will be stored in memory.
engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)

# This is used by our model class.
Base = declarative_base()


# Define the user model as a class that inherits from Base.
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# Create the database tables based on the models we defined.
Base.metadata.create_all(engine)

# Add some sample data to the database just for this example.
session = Session()
session.add(User(id=6, name='Frank'))
session.commit()


# Create an instance of our Flask web application.
application = Flask(__name__)


# Define the views that comprise our application.
@application.route('/')
def hello():
    return 'Hello World!'


@application.route('/hello_template')
def hello_template():
    return render_template('hello.html')


@application.route('/users/<int:user_id>/')
def view_user(user_id):
    """Retrieve a user from the database and show details about them."""
    user = get_user(user_id)
    return render_template('user.html', user=user)


def get_user(user_id):
    """Retrieve a user from the database."""
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user


# If this script is being run from a shell, start the dev server.
if __name__ == '__main__':
    application.run()


