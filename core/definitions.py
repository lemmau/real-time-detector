import os

# relative paths
CORE_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = CORE_PATH + '/models/checkpoint_ssd300_complete.pth(E2000).tar'
CHECKPOINT_NEW = CORE_PATH + '/models/checkpoint_ssd300-masks&glasses.pth(E5710).tar'
TEST_DATA_PATH = CORE_PATH + '/data/test_data/'
COLAB_REPO = '/content/drive/My Drive/Colab Notebooks/SSD300/repo/'

# dataset relative paths
KAGGLE_PATH = './core/data/all-3x'
OUTPUT_PATH = './core/data/all-3x'
LOG_PATH = './core/data/log-complete.txt'

# RGB Colors for classes
BACKGROUND_RGB = '#FFFFFF'
WITH_MASK_RGB = '#3cb44b'
WITH_GLASSES_RGB = '#3BF7F7'
WITH_MASK_AND_GLASSES_RGB = '#00F218'
CLEAN_RGB = '#F30B0B'
WITH_FACE_SHIELD_RGB = '#3BA6F7' #TODO 
#CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')  # requires `import os`

# Objects
MASK = 'Barbijo'
GLASSES = 'Proteccion ocular'
FACE_SHIELD = 'Mascara'

INFRACTION_ID = 5

MIN_SCORE=0.5
MAX_OVERLAP=0.001
MAX_OBJECTS=200

FIRST_DAY_MONTH_SPANISH = 'Primer dia del mes'
LAST_DAY_MONTH_SPANISH = 'Ultimo dia del mes'
FIRST_DAY_MONTH_CRON = '1'
LAST_DAY_MONTH_CRON = 'last'
PERIODICIDAD_MENSUAL = 'mensual'
PERIODICIDAD_SEMANAL = 'semanal'
PERIODICIDAD_DIARIA = 'diaria'

EMAIL_SENDER_CRON_ID = 'emailSenderCron'
