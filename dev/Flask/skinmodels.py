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


class SkinDiseaseModelResnet(nn.Module):
    def __init__(self, num_class):
        super().__init__()
        self.num_class = num_class
        self.densenet = nn.Sequential(
            torch.hub.load('pytorch/vision:v0.10.0',
                           'densenet121', pretrained=True),
        )
        self.linear = nn.Sequential(
            nn.Linear(1000, 500),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(500),
            nn.Linear(500, 250),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(250),
            nn.Linear(250, 125),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(125),
            nn.Linear(125, 50),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.LayerNorm(50),
            nn.Linear(50, self.num_class),
            nn.Softmax()
        )

    def __call__(self, x):
        x = self.densenet(x)
        x = self.linear(x)
        return x
