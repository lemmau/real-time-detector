import os

# relative paths
CORE_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = CORE_PATH + '/models/checkpoint_ssd300_kaggle.pth(31-07 1149AM).tar'
CHECKPOINT_NEW = CORE_PATH + '/models/checkpoint_ssd300-masks&glasses.pth(E5710).tar'
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

FIRST_DAY_MONTH_SPANISH = 'Primer dia del mes'
LAST_DAY_MONTH_SPANISH = 'Ultimo dia del mes'
FIRST_DAY_MONTH_CRON = '1'
LAST_DAY_MONTH_CRON = 'last'
PERIODICIDAD_MENSUAL = 'mensual'
PERIODICIDAD_SEMANAL = 'semanal'
PERIODICIDAD_DIARIA = 'diaria'