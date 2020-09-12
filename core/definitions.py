import os

# relative paths
CORE_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = CORE_PATH + '/models/checkpoint_ssd300_kaggle.pth(31-07 1149AM).tar'
CHECKPOINT_NEW = CORE_PATH + '/models/checkpoint_ssd300-masks&glasses.pth(E1256).tar'
TEST_DATA_PATH = CORE_PATH + '/data/test_data/'
COLAB_REPO = '/content/drive/My Drive/Colab Notebooks/SSD300/repo/'

# dataset relative paths
KAGGLE_PATH = './core/data/kaggle-masks'
OUTPUT_PATH = './core/data/kaggle-masks'
LOG_PATH = './core/data/log.txt'

# RGB Colors for classes
BACKGROUND_RGB = '#ffffff'
WITH_MASK_RGB = '#3cb44b'
WITH_GLASSES_RGB = '#3cb44b'
WITH_MASK_AND_GLASSES_RGB = '#000000'
CLEAN_RGB = '#e6194B'
#CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')  # requires `import os`

# Objects
MASK = 'Barbijo'
GLASSES = 'Proteccion ocular'
FACE_SHIELD = 'Mascara'

INFRACTION_ID = 4

MIN_SCORE=0.5
MAX_OVERLAP=0.001
MAX_OBJECTS=200