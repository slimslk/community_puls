from community_app import create_app
from community_app.models.questions import *
from community_app.models.responses import *

if __name__ == "__main__":
    app = create_app()
    app.run()
