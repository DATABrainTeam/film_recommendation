import os
from app_container import create_app

app = create_app()

if __name__ == '__main__':
    app.run(port=int(os.environ['PORT']))
