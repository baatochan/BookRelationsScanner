import os
from app.app import app
from app.app_init import init_app

if __name__ == "__main__":
    app.config.from_object('config.default')
    app.config.from_object(os.environ.get('CONFIG_FILE'))
    app.app_context().push()

    init_app()

    app.run()
