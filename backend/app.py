from community_app import create_app
from community_app.routers.question import questions_bp
from community_app.routers.response import responses_bp
from community_app.routers.category import category_bp
from community_app.models.question import Question, Statistic
from community_app.models.response import Response


app = create_app()

app.register_blueprint(questions_bp)
app.register_blueprint(responses_bp)
app.register_blueprint(category_bp)


if __name__ == "__main__":
    app.run()
