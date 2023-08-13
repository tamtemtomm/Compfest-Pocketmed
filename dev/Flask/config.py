import os
import torch
import json
import torchvision.transforms as T
import matplotlib.pyplot as plt


def read_disease_step(disease_step_path):
    assert os.path.isfile(
        disease_step_path), f"Can't find disease_step config : {disease_step_path}"
    with open(disease_step_path, 'r') as f:
        disease_step = json.load(f)

    disease_to_link = {disease['name']: disease['link']
                       for disease in disease_step}
    disease_to_step = {disease['name']: disease['step']
                       for disease in disease_step}

    return disease_to_link, disease_to_step


def read_label_decode(label_decode_path):
    assert os.path.isfile(
        label_decode_path), f"Can't find label_decode config : {label_decode_path}"
    with open(label_decode_path, 'r') as f:
        labels = f.read().splitlines()
    label_decode = dict()
    for label in labels:
        code, disease = label.split(':')
        label_decode[int(code)] = disease

    return label_decode, len(label_decode)


def transform_img(img_path):
    assert os.path.isfile(img_path), f"Can't find Image : {img_path}"
    test_transforms = T.Compose([
        T.Resize((128, 128)),
    ])
    img = plt.imread(img_path)

    img = test_transforms(torch.tensor(
        img, dtype=torch.float32).permute(2, 0, 1)).unsqueeze(dim=0)
    return img
