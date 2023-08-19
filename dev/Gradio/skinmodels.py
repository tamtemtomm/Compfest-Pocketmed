import torch
import torch.nn as nn
from torchvision.models import resnet50
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class IsSkinResnet(nn.Module):
    def __init__(self):
        super().__init__()
        self.resnet = resnet50(
            weights="ResNet50_Weights.IMAGENET1K_V1").to(device)
        self.linear = nn.Sequential(
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.Linear(500, 2),
            nn.Softmax()
        )

    def __call__(self, x):
        x = self.resnet(x)
        x = self.linear(x)
        return x


class IsHealthySkinResnet(nn.Module):
    def __init__(self):
        super().__init__()

        self.resnet = resnet50(
            weights="ResNet50_Weights.IMAGENET1K_V1").to(device)
        self.linear = nn.Sequential(
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(500),
            nn.Linear(500, 250),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(250),
            nn.Linear(250, 2),
            nn.Softmax()
        )

    def __call__(self, x):
        x = self.resnet(x)
        x = self.linear(x)
        return x

# @title <p> Resnet alternative
class LinearBlock(nn.Module):
  def __init__(self, in_channel, out_channel, dropout = 0.2):
    super().__init__()
    self.linear = nn.Sequential(
        nn.Linear(in_channel, out_channel),
        nn.ReLU(),
        nn.Dropout(dropout),
        nn.LayerNorm(out_channel)
    )
  def __call__(self, x):
    return self.linear(x)

class SkinDiseaseModelResnet(nn.Module):
  def __init__(self, num_class):
    super().__init__()
    self.num_class = num_class
    self.resnet =  resnet50(weights="ResNet50_Weights.IMAGENET1K_V1")
    self.linearblock = nn.Sequential(
        LinearBlock(1000, 750),
        LinearBlock(750, 500),
        LinearBlock(500, 250),
        LinearBlock(250, 125),
        LinearBlock(125, 62),
        nn.Linear(62, num_class),
        nn.Softmax()
    )

  def __call__(self, x):
    x = self.resnet(x)
    x = self.linearblock(x)
    return x