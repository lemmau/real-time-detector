import os

CORE_PATH = os.path.dirname(os.path.abspath(__file__))
CHECKPOINT = CORE_PATH + '/models/checkpoint_ssd300_kaggle.pth.tar'
TEST_DATA_PATH = CORE_PATH + '/data/test_data/'
KAGGLE_PATH = './core/data/kaggle-masks'
OUTPUT_PATH = './core/data/kaggle-masks'
#CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')  # requires `import os`
