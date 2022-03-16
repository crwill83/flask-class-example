from app import app, db
from app.models import User, Post, Product


if __name__ == "__main__":
    app.run()

@app.shell_context_processor
def shell_context():
    return {'db':db, 'User':User, 'Post':Post, 'Product':Product}