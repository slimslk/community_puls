from datetime import datetime, UTC

from community_app import db


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(UTC))

    responses = db.relationship("Response", backref="question", lazy=True)

    def __str__(self):
        return f"Question: {self.text}"


class Statistic(db.Model):
    __tablename__ = "statistics"
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __str__(self):
        return "Statistic of question: {}:\n{} of agree\ns{} of disagree".format(
            self.question_id, self.agree_count, self.disagree_count
        )


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

    def __str__(self):
        return f"Category ID - {self.id}\nCategory name - {self.name}"
