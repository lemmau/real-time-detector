#BACK+CORE
import sys
sys.path.insert(0, 'commons')
sys.path.insert(0, 'flask-back')
from app import app, socketIo

if __name__ == '__main__':
    socketIo.run(app)

#GRAPHER
# import core.src.grapher as grapher

# if __name__ == "__main__":
#     grapher.main()

#CREATE DATA LISTS
# import core.src.create_data_lists as create_data_lists

