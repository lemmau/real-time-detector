import sys
sys.path.insert(0, 'commons')
sys.path.insert(0, 'flask-back')
from app import app

if __name__ == '__main__':
    app.run()
