from blog.app import create_app
from blog.config import Configuration


if __name__ == '__main__':
    app = create_app(Configuration)
    app.run(port=5001, host='0.0.0.0')
