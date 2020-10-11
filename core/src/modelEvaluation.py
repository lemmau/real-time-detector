import commons.model
import torch
import matplotlib.pyplot as plt
import numpy as np
from commons.utils import *
from .datasets import PascalVOCDataset
from tqdm import tqdm
from pprint import PrettyPrinter
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)
from ..definitions import OUTPUT_PATH

pp = PrettyPrinter()
data_folder = OUTPUT_PATH  # folder with images
keep_difficult = True  # difficult ground truth objects must always be considered in mAP calculation, because these objects DO exist!
batch_size = 1
workers = 4
device = torch.device('cpu')
# checkpoint = 'core\models\checkpoint_ssd300_kaggle.pth(31-07 1149AM).tar' # 5693
checkpoint = 'core\models\checkpoint_ssd300_complete.pth(E3000).tar' # 6228
# checkpoint = 'core\models\checkpoint_ssd300_kaggle.pth.tar'

checkpoint = torch.load(checkpoint, map_location='cpu')
model = checkpoint['model']
model = model.to(device)

test_dataset = PascalVOCDataset(data_folder,
                                split='test',
                                keep_difficult=keep_difficult)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False,
                                          collate_fn=test_dataset.collate_fn, num_workers=workers, pin_memory=True)


def evaluatemAP(test_loader, model):
    model.eval()

    det_boxes = list()
    det_labels = list()
    det_scores = list()
    true_boxes = list()
    true_labels = list()
    true_difficulties = list()

    with torch.no_grad():
        for i, (images, boxes, labels, difficulties) in enumerate(tqdm(test_loader, desc='Evaluating')):
            images = images.to(device)
            predicted_locs, predicted_scores = model(images)

            det_boxes_batch, det_labels_batch, det_scores_batch = model.detect_objects(predicted_locs, predicted_scores,
                                                                                       min_score=0.3, max_overlap=0.45,
                                                                                       top_k=200)

            # Store this batch's results for mAP calculation
            boxes = [b.to(device) for b in boxes]
            labels = [l.to(device) for l in labels]
            difficulties = [d.to(device) for d in difficulties]

            det_boxes.extend(det_boxes_batch)
            det_labels.extend(det_labels_batch)
            det_scores.extend(det_scores_batch)
            true_boxes.extend(boxes)
            true_labels.extend(labels)
            true_difficulties.extend(difficulties)

        # Calculate mAP
        APs, mAP = calculate_mAP(det_boxes, det_labels, det_scores, true_boxes, true_labels, true_difficulties)

    # Print AP for each class
    pp.pprint(APs)

    print('\nMean Average Precision (mAP): %.3f' % mAP)

def runMain():
    evaluatemAP(test_loader, model)
