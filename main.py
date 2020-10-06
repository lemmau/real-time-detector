#BACK+CORE
# import sys
# sys.path.insert(0, 'commons')
# sys.path.insert(0, 'flask-back')
# from app import app, socketIo

# if __name__ == '__main__':
#     socketIo.run(app)

#GRAPHER
# import core.src.grapher as grapher

# if __name__ == "__main__":
#     grapher.main()

#CREATE DATA LISTS
# import core.src.create_data_lists as create_data_lists

#CALCULATE MAP
import core.src.modelEvaluation as modelEval

if __name__ == "__main__":
    modelEval.runMain()


# import torch
# import numpy as np
# from core.src.confusionMatrix import ConfusionMatrix

# conf_mat = ConfusionMatrix(num_classes = 5, CONF_THRESHOLD = 0.3, IOU_THRESHOLD = 0.5)

# preds = torch.tensor([0, 1, 2, 2, 1])
# true = torch.tensor([0, 1, 2, 3, 2])

# preds = [[0, 1, 2, 2, 1], [0, 1, 2, 2, 1]]
# true = [[0, 1, 2, 3, 2], [0, 1, 2, 2, 1]]

# preds = np.array([[0, 1, 2, 2, 1], [0, 1, 2, 2, 1]])
# true = np.array([[0, 1, 2, 2, 1], [0, 1, 2, 2, 1]])

# preds = np.array([0, 1, 2, 2, 1, 2], [0, 1, 2, 2, 1, 2])
# true = np.array([2, 1, 2, 2, 1], [2, 1, 2, 2, 1])

# preds = [[0, 1, 2, 2, 1, 2], [0, 1, 2, 2, 1, 2]]
# true = [[0, 1, 2, 2, 1, 2], [0, 1, 2, 2, 1, 2]]

# conf_mat.process_batch(preds, true)
# conf_mat.priprint_matrix()



# import torch
# from pytorch_lightning.metrics import ConfusionMatrix

# pred = torch.tensor([0, 1, 2, 2])
# target = torch.tensor([0, 1, 2, 2])
# metric = ConfusionMatrix()
# print(metric(pred, target))

# from sklearn.metrics import confusion_matrix

# y_true = [[2, 0, 2, 2, 0, 1], [2, 0, 2, 2, 0, 2]]
# y_pred = [[0, 0, 2, 2, 0, 2], [0, 0, 2, 2, 0, 1]]

# print(confusion_matrix(y_true, y_pred))


# import torch
# import matplotlib.pyplot as plt
# import numpy as np
# from sklearn.metrics import (
#     confusion_matrix,
#     ConfusionMatrixDisplay
# )

# voc_labels = ['with_mask', 'with_glasses', 'with_mask_and_glasses', 'with_face_shield' ,'clean']

# y_true = [torch.tensor([0, 3, 2, 2, 3]), torch.tensor([2, 2, 2, 2, 2])]
# y_pred = [torch.tensor([0, 3, 1, 1, 3]), torch.tensor([1, 1, 1, 1, 1])]

# print(np.concatenate(y_true, axis=0))

# cn_matrix = confusion_matrix(
#     y_true=np.concatenate(y_true, axis=0),
#     y_pred=np.concatenate(y_pred, axis=0),
#     # labels=voc_labels,
#     normalize="true",
# )

# ConfusionMatrixDisplay(cn_matrix).plot(
#     include_values=False, xticks_rotation="vertical"
# )
# plt.title("RTD")
# plt.tight_layout()
# plt.show()
