import os, shutil, zipfile, json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights
import gradio as gr
import matplotlib.pyplot as plt

def SkinDiagnosis(img_path, model1_path, model2_path, model3_path, label_decode_path, disease_step_path):
  #Read Images
  test_transforms = T.Compose([
    T.Resize((128, 128)),
  ])
  img = plt.imread(img_path)
  img = test_transforms(torch.tensor(img, dtype=torch.float32).permute(2,0,1)).unsqueeze(dim=0)
  
  # Setup device
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
  
  # Setup disease step
  with open(disease_step_path, 'r') as f:
    disease_step = json.load(f)
  
  disease_to_link = {disease['name'] : disease['link'] for disease in disease_step}
  disease_to_step = {disease['name'] : disease['step'] for disease in disease_step}  
  
  # Setup label decode
  with open(label_decode_path, 'r') as f:
    labels = f.read().splitlines()
  label_decode = dict()
  for label in labels:
    code, disease = label.split(':')
    label_decode[int(code)] = disease
  num_class = len(label_decode)
  
  # Setup model1
  class IsSkin(nn.Module):
    def __init__(self):
      super().__init__()
      self.resnet =  resnet50(weights="ResNet50_Weights.IMAGENET1K_V1")
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
  model1 = IsSkin().to(device)
  model1.load_state_dict(torch.load(model1_path, map_location=torch.device(device)))
  
  # Setup model2
  class IsHealthySkin(nn.Module):
    def __init__(self):
      super().__init__()
      self.resnet =  resnet50(weights="ResNet50_Weights.IMAGENET1K_V1").to(device)
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

  model2 = IsHealthySkin().to(device)
  model2.load_state_dict(torch.load(model2_path, map_location=torch.device(device)))
  
  # Setup model3
  class SkinDiseaseModel(nn.Module):
    def __init__(self):
      super().__init__()
      self.densenet =  nn.Sequential(
          torch.hub.load('pytorch/vision:v0.10.0', 'densenet121', pretrained=True),
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
          nn.Linear(50, num_class),
          nn.Softmax()
      )

    def __call__(self, x):
      x = self.densenet(x)
      x = self.linear(x)
      return x
  model3 = SkinDiseaseModel().to(device)
  model3.load_state_dict(torch.load(model3_path, map_location=torch.device(device)))
  
  # Diagnosis
  isskin = model1(img).argmax().item()
  if isskin == 1 : return 'notskin', 'Kosong', 'Kosong'
  ishealthy = model2(img).argmax().item()
  if ishealthy == 0 : return 'healthy', 'Kosong', 'Kosong'
  disease = model3(img).argmax().item()

  return label_decode[disease], disease_to_link[label_decode[disease]], disease_to_step[label_decode[disease]]