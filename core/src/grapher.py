import os
import matplotlib.pyplot as plt
import numpy as np
from .. definitions import LOG_PATH

def main():
    log = open(LOG_PATH, 'r') 
    logLines = log.readlines()
    epochs = getEpochs(logLines)
    loss = getLoss(logLines)

    plot(epochs, loss)

def plot(epochs, loss):
    N = len(epochs)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(np.arange(0, N), loss, label="loss")
    plt.title("Training Loss")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss")
    plt.legend(loc="lower left")
    plt.savefig("plot")

def getEpochs(logLines):
    epochs = []

    for line in logLines:
        epoch = line.split('Epoch: [')[1].split('/')[0]
        epochs.append(epoch)

    for i in range(len(epochs) - 1):
        if (i != 0) & (epochs[i] == '0'):
            epochs.pop(i)

    return epochs

def getLoss(logLines):
    losses = []

    for line in logLines:
        loss = line.split('Loss ')[1].split(' (')[0]
        losses.append(loss)

    return [float(loss) for loss in losses]
