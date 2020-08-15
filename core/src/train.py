import time
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
from commons.model import SSD300, MultiBoxLoss
from .datasets import PascalVOCDataset
from utils import *
from .. definitions import CHECKPOINT, KAGGLE_PATH

# Data parameters
data_folder = KAGGLE_PATH  # folder with images
keep_difficult = True

n_classes = len(label_map)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Learning parameters
checkpoint = CHECKPOINT  # path to model checkpoint, None if none
# checkpoint = None  CHECKPOINT # path to model checkpoint, None if nonek
batch_size = 8  # batch size
iterations = 120000 # 120000  # number of iterations to train
workers = 4  # number of workers for loading data in the DataLoader
print_freq = 200  # print training status every __ batches
lr = 1e-3  # learning rate
decay_lr_at = [80000, 100000]  # decay learning rate after these many iterations
decay_lr_to = 0.1  # decay learning rate to this fraction of the existing learning rate
momentum = 0.9  # momentum
weight_decay = 5e-4  # weight decay
grad_clip = None  # clip if gradients are exploding, which may happen at larger batch sizes (sometimes at 32) - you will recognize it by a sorting error in the MuliBox loss calculation

cudnn.benchmark = True

def main():
    global start_epoch, label_map, epoch, checkpoint, decay_lr_at
    
    print("Checkpoint: " + checkpoint.__str__())

    # Initialize model or load checkpoint
    if checkpoint is None:
        start_epoch = 0
        model = SSD300(n_classes=n_classes)
        biases = list()
        not_biases = list()
        for param_name, param in model.named_parameters():
            if param.requires_grad:
                if param_name.endswith('.bias'):
                    biases.append(param)
                else:
                    not_biases.append(param)
        optimizer = torch.optim.SGD(params=[{'params': biases, 'lr': 2 * lr}, {'params': not_biases}],
                                    lr=lr, momentum=momentum, weight_decay=weight_decay)

    else:
        checkpoint = torch.load(checkpoint)
        start_epoch = checkpoint['epoch'] + 1
        print('\nLoaded checkpoint from epoch %d.\n' % start_epoch)
        model = checkpoint['model']
        optimizer = checkpoint['optimizer']

    # Move to default device
    model = model.to(device)
    criterion = MultiBoxLoss(priors_cxcy=model.priors_cxcy).to(device)

    train_dataset = PascalVOCDataset(data_folder,
                                     split='train',
                                     keep_difficult=keep_difficult)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                                               collate_fn=train_dataset.collate_fn, num_workers=workers,
                                               pin_memory=True)

    epochs = iterations // (len(train_dataset) // 32)
    decay_lr_at = [it // (len(train_dataset) // 32) for it in decay_lr_at]
    print("Lenght decay_lr_at: " + decay_lr_at.__str__())

    # Epochs
    for epoch in range(start_epoch, epochs):
        print("Epoch: " + epoch.__str__())

        # Decay learning rate at particular epochs
        if epoch in decay_lr_at:
            adjust_learning_rate(optimizer, decay_lr_to)

        # Training for epoch
        train(train_loader=train_loader,
              model=model,
              criterion=criterion,
              optimizer=optimizer,
              epoch=epoch)

        print("Saving checkpoint for epoch: " + epoch.__str__())
        # Save checkpoint
        save_checkpoint(epoch, model, optimizer)

def train(train_loader, model, criterion, optimizer, epoch):
    model.train()  # training mode enables dropout

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    start = time.time()

    for i, (images, boxes, labels, _) in enumerate(train_loader):
        data_time.update(time.time() - start)

        # Move to default device
        images = images.to(device)
        boxes = [b.to(device) for b in boxes]
        labels = [l.to(device) for l in labels]

        predicted_locs, predicted_scores = model(images)

        loss = criterion(predicted_locs, predicted_scores, boxes, labels)

        # Backward prop.
        optimizer.zero_grad()
        loss.backward()

        # Clip gradients, if necessary
        if grad_clip is not None:
            clip_gradient(optimizer, grad_clip)

        # Update model
        optimizer.step()

        losses.update(loss.item(), images.size(0))
        batch_time.update(time.time() - start)

        start = time.time()

        # Print status
        if i % print_freq == 0:
            logMessage = (("[{0}] Epoch: [{1}/{2}]\t"
                "Batch Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t"
                "Data Time {data_time.val:.3f} ({data_time.avg:.3f})\t"
                "Loss {loss.val:.4f} ({loss.avg:.4f})\n").format(datetime.now(), epoch, epochs,
                                                        batch_time=batch_time,
                                                        data_time=data_time, loss=losses))
                          
            print(logMessage)
            
            with open('/content/drive/My Drive/Colab Notebooks/SSD300/repo/log.txt', 'a') as f:
              f.write(logMessage.__str__())

        # assert not np.any(np.isnan(losses.val)) # Add some validation for loss = nan 
    del predicted_locs, predicted_scores, images, boxes, labels

if __name__ == 'core.src.train':
    main()
