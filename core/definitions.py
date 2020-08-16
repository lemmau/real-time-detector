import os

# relative paths
CORE_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = CORE_PATH + '/models/checkpoint_ssd300_kaggle.pth.tar'
CHECKPOINT_NEW = CORE_PATH + '/models/checkpoint_ssd300-masks.pth.tar'
TEST_DATA_PATH = CORE_PATH + '/data/test_data/'
COLAB_REPO = '/content/drive/My Drive/Colab Notebooks/SSD300/repo/'

# dataset relative paths
KAGGLE_PATH = './core/data/kaggle-masks'
OUTPUT_PATH = './core/data/kaggle-masks'

# RGB Colors for classes
BACKGROUND_RGB = '#ffffff'
WITH_MASK_RGB = '#3cb44b'
WITH_GLASSES_RGB = '#3cb44b'
WITHOUT_MASK_RGB = '#e6194B'
#CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')  # requires `import os`
