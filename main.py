import sys
sys.path.insert(0, 'commons')
sys.path.insert(0, 'flask-back')
from app import app, socketIo

if __name__ == '__main__':
    socketIo.run(app)
