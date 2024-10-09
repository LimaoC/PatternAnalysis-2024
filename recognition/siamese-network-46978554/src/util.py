from pathlib import Path

import torch
import torch.nn.functional as F

# Dataset directory
# We use a downsized version of the ISIC 2020 dataset:
# https://www.kaggle.com/datasets/nischaydnk/isic-2020-jpg-256x256-resized/data
DATA_DIR = Path(__file__).parent.parent / "data"


def contrastive_loss(margin):
    """
    REF: https://www.sciencedirect.com/topics/computer-science/contrastive-loss
    """

    def f(x1, x2, y):
        dist = F.pairwise_distance(x1, x2)
        dist_sq = torch.pow(dist, 2)

        loss = (1 - y) * dist_sq + y * torch.pow(torch.clamp(margin - dist, min=0.0), 2)
        loss = torch.mean(loss / 2.0, dim=0)

        return loss

    return f


def contrastive_loss_threshold(margin):
    def f(x1, x2):
        dist = F.pairwise_distance(x1, x2)
        return (dist >= margin).float()

    return f


def plot_pca_embeddings(embeddings, targets):
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA

    pca = PCA(n_components=2)
    embeddings_pca = pca.fit_transform(embeddings)

    comp1 = embeddings_pca[:, 0]
    comp2 = embeddings_pca[:, 1]

    plt.scatter(comp1[targets == 0], comp2[targets == 0], label="benign")
    plt.scatter(comp1[targets == 1], comp2[targets == 1], label="malignant")
    plt.xlabel("PC Direction 1")
    plt.ylabel("PC Direction 2")
    plt.title("Model Embeddings (Test Set) in Principal Component Space")
    plt.legend()
    plt.show()
