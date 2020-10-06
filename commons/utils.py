import json
import os
import torch
import random
import xml.etree.ElementTree as ET
import torchvision.transforms.functional as FT
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)

device = torch.device('cpu')

checkpoint_name = 'checkpoint_ssd300_complete.pth.tar'

voc_labels = ('with_mask', 'with_glasses', 'with_mask_and_glasses', 'with_face_shield' ,'clean')
label_map = {k: v + 1 for v, k in enumerate(voc_labels)}
label_map['background'] = 0
rev_label_map = {v: k for k, v in label_map.items()}  # Inverse mapping

distinct_colors = ['#FFFFFF', '#3cb44b', '#3BF7F7', '#00F218', '#3BA6F7', '#F30B0B']
label_color_map = {k: distinct_colors[i] for i, k in enumerate(label_map.keys())}

images_to_train = 1550

def find_intersection(set_1, set_2):
    lower_bounds = torch.max(set_1[:, :2].unsqueeze(1), set_2[:, :2].unsqueeze(0))  # (n1, n2, 2)
    upper_bounds = torch.min(set_1[:, 2:].unsqueeze(1), set_2[:, 2:].unsqueeze(0))  # (n1, n2, 2)
    intersection_dims = torch.clamp(upper_bounds - lower_bounds, min=0)  # (n1, n2, 2)
    return intersection_dims[:, :, 0] * intersection_dims[:, :, 1]  # (n1, n2)

def find_jaccard_overlap(set_1, set_2): # https://en.wikipedia.org/wiki/Jaccard_index

    # Find intersections
    intersection = find_intersection(set_1, set_2)  # (n1, n2)

    # Find areas of each box in both sets
    areas_set_1 = (set_1[:, 2] - set_1[:, 0]) * (set_1[:, 3] - set_1[:, 1])  # (n1)
    areas_set_2 = (set_2[:, 2] - set_2[:, 0]) * (set_2[:, 3] - set_2[:, 1])  # (n2)

    # Find the union
    # PyTorch auto-broadcasts singleton dimensions
    union = areas_set_1.unsqueeze(1) + areas_set_2.unsqueeze(0) - intersection  # (n1, n2)

    return intersection / union  # (n1, n2)

def create_data_lists(kaggle_path, output_folder):
    kaggle_path = os.path.abspath(kaggle_path)

    train_images = list()
    train_objects = list()
    n_objects = 0

    allIds = listdir(os.path.join(kaggle_path, 'images'))

    random.shuffle(allIds)
    
    ids = allIds[:images_to_train]
    
    ids = [f.split('.')[0] for f in ids]
    # ids = [".".join(f.split(".")[:-1]) for f in os.listdir(os.path.join(kaggle_path, 'images')) if os.path.isfile(f)][:700]

    for id in ids:
        # Parse annotation's XML file
        objects = parse_annotation(os.path.join(kaggle_path, 'annotations', id + '.xml'))
        if len(objects) == 0:
            continue
        n_objects += len(objects)
        train_objects.append(objects)
        train_images.append(os.path.join(kaggle_path, 'images', id + '.png')) #TODO: Validar si funciona bien con un png tambien porque solo se probo con ".jpg"

    assert len(train_objects) == len(train_images)

    with open(os.path.join(output_folder, 'TRAIN_images.json'), 'w') as j:
        json.dump(train_images, j)
    with open(os.path.join(output_folder, 'TRAIN_objects.json'), 'w') as j:
        json.dump(train_objects, j)
    with open(os.path.join(output_folder, 'label_map.json'), 'w') as j:
        json.dump(label_map, j)  # save label map too

    print('\nThere are %d training images containing a total of %d objects. Files have been saved to %s.' % (
        len(train_images), n_objects, os.path.abspath(output_folder)))

    # Test data
    test_images = list()
    test_objects = list()
    n_objects = 0

    # with open(os.path.join(kaggle_path, 'ImageSets/Main/test.txt')) as f:
    #     ids = f.read().splitlines()
    ids = allIds[images_to_train:]
    ids = [f.split('.')[0] for f in ids]

    for id in ids:
        # Parse annotation's XML file
        objects = parse_annotation(os.path.join(kaggle_path, 'annotations', id + '.xml'))
        if len(objects) == 0:
            continue
        test_objects.append(objects)
        n_objects += len(objects)
        test_images.append(os.path.join(kaggle_path, 'images', id + '.png'))

    assert len(test_objects) == len(test_images)

    with open(os.path.join(output_folder, 'TEST_images.json'), 'w') as j:
        json.dump(test_images, j)
    with open(os.path.join(output_folder, 'TEST_objects.json'), 'w') as j:
        json.dump(test_objects, j)

    print('\nThere are %d test images containing a total of %d objects. Files have been saved to %s.' % (
        len(test_images), n_objects, os.path.abspath(output_folder)))

def parse_annotation(annotation_path):
    tree = ET.parse(annotation_path)
    root = tree.getroot()

    boxes = list()
    labels = list()
    difficulties = list()
    for object in root.iter('object'):

        difficult = int(object.find('difficult').text == '1')

        label = object.find('name').text.lower().strip()
        if label not in label_map:
            continue

        bbox = object.find('bndbox')
        xmin = int(bbox.find('xmin').text) - 1
        ymin = int(bbox.find('ymin').text) - 1
        xmax = int(bbox.find('xmax').text) - 1
        ymax = int(bbox.find('ymax').text) - 1

        boxes.append([xmin, ymin, xmax, ymax])
        labels.append(label_map[label])
        difficulties.append(difficult)

    return {'boxes': boxes, 'labels': labels, 'difficulties': difficulties}

def transform(image, boxes, labels, difficulties, split):
    assert split in {'TRAIN', 'TEST'}

    # Mean and standard deviation of ImageNet data that our base VGG from torchvision was trained on
    # see: https://pytorch.org/docs/stable/torchvision/models.html
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    new_image = image
    new_boxes = boxes
    new_labels = labels
    new_difficulties = difficulties

    # Skip the following operations for evaluation/testing
    if split == 'TRAIN':
        # A series of photometric distortions in random order, each with 50% chance of occurrence, as in Caffe repo
        new_image = photometric_distort(new_image)

        # Convert PIL image to Torch tensor
        new_image = FT.to_tensor(new_image)

        # Expand image (zoom out) with a 50% chance - helpful for training detection of small objects
        # Fill surrounding space with the mean of ImageNet data that our base VGG was trained on
        if random.random() < 0.5:
            new_image, new_boxes = expand(new_image, boxes, filler=mean)

        # Randomly crop image (zoom in)
        new_image, new_boxes, new_labels, new_difficulties = random_crop(new_image, new_boxes, new_labels,
                                                                         new_difficulties)

        # Convert Torch tensor to PIL image
        new_image = FT.to_pil_image(new_image)

        # Flip image with a 50% chance
        if random.random() < 0.5:
            new_image, new_boxes = flip(new_image, new_boxes)

    # Resize image to (300, 300) - this also converts absolute boundary coordinates to their fractional form
    new_image, new_boxes = resize(new_image, new_boxes, dims=(300, 300))

    # Convert PIL image to Torch tensor
    new_image = FT.to_tensor(new_image)

    # Normalize by mean and standard deviation of ImageNet data that our base VGG was trained on
    new_image = FT.normalize(new_image, mean=mean, std=std)

    return new_image, new_boxes, new_labels, new_difficulties

def photometric_distort(image):

    new_image = image

    distortions = [FT.adjust_brightness,
                   FT.adjust_contrast,
                   FT.adjust_saturation,
                   FT.adjust_hue]

    random.shuffle(distortions)

    for d in distortions:
        if random.random() < 0.5:
            if d.__name__ == 'adjust_hue':
                # Caffe repo uses a 'hue_delta' of 18 - we divide by 255 because PyTorch needs a normalized value
                adjust_factor = random.uniform(-18 / 255., 18 / 255.)
            else:
                # Caffe repo uses 'lower' and 'upper' values of 0.5 and 1.5 for brightness, contrast, and saturation
                adjust_factor = random.uniform(0.5, 1.5)

            # Apply this distortion
            new_image = d(new_image, adjust_factor)

    return new_image

def expand(image, boxes, filler):
    # Calculate dimensions of proposed expanded (zoomed-out) image
    original_h = image.size(1)
    original_w = image.size(2)
    max_scale = 4
    scale = random.uniform(1, max_scale)
    new_h = int(scale * original_h)
    new_w = int(scale * original_w)

    # Create such an image with the filler
    filler = torch.FloatTensor(filler)  # (3)
    new_image = torch.ones((3, new_h, new_w), dtype=torch.float) * filler.unsqueeze(1).unsqueeze(1)  # (3, new_h, new_w)

    # Place the original image at random coordinates in this new image (origin at top-left of image)
    left = random.randint(0, new_w - original_w)
    right = left + original_w
    top = random.randint(0, new_h - original_h)
    bottom = top + original_h
    new_image[:, top:bottom, left:right] = image

    # Adjust bounding boxes' coordinates accordingly
    new_boxes = boxes + torch.FloatTensor([left, top, left, top]).unsqueeze(0)

    return new_image, new_boxes

def random_crop(image, boxes, labels, difficulties):
    original_h = image.size(1)
    original_w = image.size(2)
    # Keep choosing a minimum overlap until a successful crop is made
    while True:
        # Randomly draw the value for minimum overlap
        min_overlap = random.choice([0., .1, .3, .5, .7, .9, None])  # 'None' refers to no cropping

        # If not cropping
        if min_overlap is None:
            return image, boxes, labels, difficulties

        max_trials = 50
        for _ in range(max_trials):
            min_scale = 0.3
            scale_h = random.uniform(min_scale, 1)
            scale_w = random.uniform(min_scale, 1)
            new_h = int(scale_h * original_h)
            new_w = int(scale_w * original_w)

            # Aspect ratio has to be in [0.5, 2]
            aspect_ratio = new_h / new_w
            if not 0.5 < aspect_ratio < 2:
                continue

            # Crop coordinates (origin at top-left of image)
            left = random.randint(0, original_w - new_w)
            right = left + new_w
            top = random.randint(0, original_h - new_h)
            bottom = top + new_h
            crop = torch.FloatTensor([left, top, right, bottom])  # (4)

            # Calculate Jaccard overlap between the crop and the bounding boxes
            overlap = find_jaccard_overlap(crop.unsqueeze(0),
                                           boxes)
            overlap = overlap.squeeze(0)

            # If not a single bounding box has a Jaccard overlap of greater than the minimum, try again
            if overlap.max().item() < min_overlap:
                continue

            # Crop image
            new_image = image[:, top:bottom, left:right]

            # Find centers of original bounding boxes
            bb_centers = (boxes[:, :2] + boxes[:, 2:]) / 2.

            # Find bounding boxes whose centers are in the crop
            centers_in_crop = (bb_centers[:, 0] > left) * (bb_centers[:, 0] < right) * (bb_centers[:, 1] > top) * (
                    bb_centers[:, 1] < bottom)

            # If not a single bounding box has its center in the crop, try again
            if not centers_in_crop.any():
                continue

            # Discard bounding boxes that don't meet this criterion
            new_boxes = boxes[centers_in_crop, :]
            new_labels = labels[centers_in_crop]
            new_difficulties = difficulties[centers_in_crop]

            # Calculate bounding boxes' new coordinates in the crop
            new_boxes[:, :2] = torch.max(new_boxes[:, :2], crop[:2])
            new_boxes[:, :2] -= crop[:2]
            new_boxes[:, 2:] = torch.min(new_boxes[:, 2:], crop[2:])
            new_boxes[:, 2:] -= crop[:2]

            return new_image, new_boxes, new_labels, new_difficulties

def resize(image, boxes, dims=(300, 300), return_percent_coords=True):
    # Resize image
    new_image = FT.resize(image, dims)

    # Resize bounding boxes
    old_dims = torch.FloatTensor([image.width, image.height, image.width, image.height]).unsqueeze(0)
    new_boxes = boxes / old_dims  # percent coordinates

    if not return_percent_coords:
        new_dims = torch.FloatTensor([dims[1], dims[0], dims[1], dims[0]]).unsqueeze(0)
        new_boxes = new_boxes * new_dims

    return new_image, new_boxes

def flip(image, boxes):
    # Flip image
    new_image = FT.hflip(image)

    # Flip boxes
    new_boxes = boxes
    new_boxes[:, 0] = image.width - boxes[:, 0] - 1
    new_boxes[:, 2] = image.width - boxes[:, 2] - 1
    new_boxes = new_boxes[:, [2, 1, 0, 3]]

    return new_image, new_boxes

class AverageMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

def clip_gradient(optimizer, grad_clip):
    for group in optimizer.param_groups:
        for param in group['params']:
            if param.grad is not None:
                param.grad.data.clamp_(-grad_clip, grad_clip)

def save_checkpoint(epoch, model, optimizer):
    state = {'epoch': epoch,
             'model': model,
             'optimizer': optimizer}
    
    if epoch%500 != 0:
      filename = '/content/drive/My Drive/Colab Notebooks/SSD300/repo/' + checkpoint_name # Ensure filename is right 
    else:
      filename = '/content/drive/My Drive/Colab Notebooks/SSD300/repo/model-backup/' + checkpoint_name + '(E' + epoch.__str__() + ')'
    
    torch.save(state, filename)

def calculate_mAP(det_boxes, det_labels, det_scores, true_boxes, true_labels, true_difficulties):	
    assert len(det_boxes) == len(det_labels) == len(det_scores) == len(true_boxes) == len(	
        true_labels) == len(true_difficulties)	
    n_classes = len(label_map)	

    true_images = list()	
    for i in range(len(true_labels)):	
        true_images.extend([i] * true_labels[i].size(0))	
    true_images = torch.LongTensor(true_images).to(device)	
    true_boxes = torch.cat(true_boxes, dim=0)	
    true_labels = torch.cat(true_labels, dim=0)	
    true_difficulties = torch.cat(true_difficulties, dim=0)	

    assert true_images.size(0) == true_boxes.size(0) == true_labels.size(0)	

    det_images = list()	
    for i in range(len(det_labels)):	
        det_images.extend([i] * det_labels[i].size(0))	
    det_images = torch.LongTensor(det_images).to(device)	
    det_boxes = torch.cat(det_boxes, dim=0)	
    det_labels = torch.cat(det_labels, dim=0)	
    det_scores = torch.cat(det_scores, dim=0)	

    plotConfMatrix(det_labels, true_labels)
    assert det_images.size(0) == det_boxes.size(0) == det_labels.size(0) == det_scores.size(0)	

    # Calculate APs for each class (except background)	
    average_precisions = torch.zeros((n_classes - 1), dtype=torch.float)	
    for c in range(1, n_classes):	
        # Extract only objects with this class	
        true_class_images = true_images[true_labels == c]	
        true_class_boxes = true_boxes[true_labels == c]	
        true_class_difficulties = true_difficulties[true_labels == c]	
        n_easy_class_objects = (1 - true_class_difficulties).sum().item()	

        true_class_boxes_detected = torch.zeros((true_class_difficulties.size(0)), dtype=torch.uint8).to(device)	

        # Extract only detections with this class	
        det_class_images = det_images[det_labels == c]	
        det_class_boxes = det_boxes[det_labels == c]	
        det_class_scores = det_scores[det_labels == c]	
        n_class_detections = det_class_boxes.size(0)	
        if n_class_detections == 0:	
            continue	

        # Sort detections in decreasing order of confidence/scores	
        det_class_scores, sort_ind = torch.sort(det_class_scores, dim=0, descending=True)	
        det_class_images = det_class_images[sort_ind]	
        det_class_boxes = det_class_boxes[sort_ind]	

        # In the order of decreasing scores, check if true or false positive	
        true_positives = torch.zeros((n_class_detections), dtype=torch.float).to(device)	
        false_positives = torch.zeros((n_class_detections), dtype=torch.float).to(device)	

        for d in range(n_class_detections):	
            this_detection_box = det_class_boxes[d].unsqueeze(0)	
            this_image = det_class_images[d]	

            # Find objects in the same image with this class, their difficulties, and whether they have been detected before	
            object_boxes = true_class_boxes[true_class_images == this_image]	
            object_difficulties = true_class_difficulties[true_class_images == this_image]	

            # If no such object in this image, then the detection is a false positive	
            if object_boxes.size(0) == 0:	
                false_positives[d] = 1	
                continue	

            # Find maximum overlap of this detection with objects in this image of this class	
            overlaps = find_jaccard_overlap(this_detection_box, object_boxes)	
            max_overlap, ind = torch.max(overlaps.squeeze(0), dim=0)	

            original_ind = torch.LongTensor(range(true_class_boxes.size(0)))[true_class_images == this_image][ind]	

            # If the maximum overlap is greater than the threshold of 0.5, it's a match	
            if max_overlap.item() > 0.5:	
                # If the object it matched with is 'difficult', ignore it	
                if object_difficulties[ind] == 0:	
                    # If this object has already not been detected, it's a true positive	
                    if true_class_boxes_detected[original_ind] == 0:	
                        true_positives[d] = 1	
                        true_class_boxes_detected[original_ind] = 1  # this object has now been detected/accounted for	
                    # Otherwise, it's a false positive (since this object is already accounted for)	
                    else:	
                        false_positives[d] = 1	
            # Otherwise, the detection occurs in a different location than the actual object, and is a false positive	
            else:	
                false_positives[d] = 1	

        # Compute cumulative precision and recall at each detection in the order of decreasing scores	
        cumul_true_positives = torch.cumsum(true_positives, dim=0)	
        cumul_false_positives = torch.cumsum(false_positives, dim=0)	
        cumul_precision = cumul_true_positives / (cumul_true_positives + cumul_false_positives + 1e-10)	
        cumul_recall = cumul_true_positives / n_easy_class_objects	

        # Find the mean of the maximum of the precisions corresponding to recalls above the threshold 't'	
        recall_thresholds = torch.arange(start=0, end=1.1, step=.1).tolist()	
        precisions = torch.zeros((len(recall_thresholds)), dtype=torch.float).to(device)	
        for i, t in enumerate(recall_thresholds):	
            recalls_above_t = cumul_recall >= t	
            if recalls_above_t.any():	
                precisions[i] = cumul_precision[recalls_above_t].max()	
            else:	
                precisions[i] = 0.	
        average_precisions[c - 1] = precisions.mean()	

    # Calculate Mean Average Precision (mAP)	
    mean_average_precision = average_precisions.mean().item()	

    # Keep class-wise average precisions in a dictionary	
    average_precisions = {rev_label_map[c + 1]: v for c, v in enumerate(average_precisions.tolist())}	

    return average_precisions, mean_average_precision 	

def plotConfMatrix(det_labels, true_labels):
    voc_labels = ['with_mask', 'with_glasses', 'with_mask_and_glasses', 'with_face_shield' ,'clean']
    # detMapped = np.concatenate(det_labels, axis=0)
    # trueMapped = np.concatenate(true_labels, axis=0)
    
    # print('detMapped', detMapped)
    # print('trueMapped', trueMapped)

    cn_matrix = confusion_matrix(
        y_true=true_labels,
        y_pred=det_labels,
        # labels=voc_labels,
        normalize="true",
    )

    ConfusionMatrixDisplay(cn_matrix).plot(
        include_values=False, xticks_rotation="vertical"
    )
    plt.title("RTD")
    plt.tight_layout()
    plt.show()

def adjust_learning_rate(optimizer, scale):
    """
    Scale learning rate by a specified factor.
    :param optimizer: optimizer whose learning rate must be shrunk.
    :param scale: factor to multiply learning rate with.
    """
    for param_group in optimizer.param_groups:
        param_group['lr'] = param_group['lr'] * scale
    print("DECAYING learning rate.\n The new LR is %f\n" % (optimizer.param_groups[1]['lr'],))
 