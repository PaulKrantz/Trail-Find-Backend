from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

#start changing things here
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    reviews = db.Column(db.String)

    def __init__(self, name, review):
        self.name = name
        self.reviews = review

class ReviewsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "reviews")

reviews_schema = ReviewsSchema()
reviewss_schema = ReviewsSchema(many=True)


@app.route("/reviews/add", methods=["POST"])
def add_reviews():
    name = request.json.get("name")
    reviews = request.json.get("reviews")

    record = Reviews(name, reviews)
    db.session.add(record)
    db.session.commit()

    return jsonify(reviews_schema.dump(record))

@app.route("/reviews/get", methods=["GET"])
def get_all_reviews():
    all_items = Reviews.query.all()
    
    return jsonify(reviewss_schema.dump(all_items))


if __name__ == "__main__":
    app.run(debug=True)