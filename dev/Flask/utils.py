import os
import torch
from skinmodels import IsSkinResnet, IsHealthySkinResnet, SkinDiseaseModelResnet
from config import read_disease_step, read_label_decode, transform_img


def SkinDiagnosis(img_path, model1_path, model2_path, model3_path, label_decode_path, disease_step_path):
    # Setup device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Read Images
    img = transform_img(img_path).to(device)

    # Setup disease step
    disease_to_link, disease_to_step = read_disease_step(disease_step_path)

    # Setup label decode
    label_decode, num_class = read_label_decode(label_decode_path)

    # Setup model1
    assert os.path.isfile(
        model1_path), f"Can't find model state_dict path  : {model1_path}"
    model1 = IsSkinResnet().to(device)
    model1.load_state_dict(torch.load(
        model1_path, map_location=torch.device(device)))

    # Setup model2
    model2 = IsHealthySkinResnet().to(device)
    assert os.path.isfile(
        model2_path), f"Can't find model state_dict path  : {model2_path}"
    model2.load_state_dict(torch.load(
        model2_path, map_location=torch.device(device)))

    # Setup model3
    model3 = SkinDiseaseModelResnet(num_class).to(device)
    assert os.path.isfile(
        model3_path), f"Can't find model state_dict path  : {model3_path}"
    model3.load_state_dict(torch.load(
        model3_path, map_location=torch.device(device)))

    # Diagnosis
    isskin = model1(img).argmax().item()
    if isskin == 1:
        return 'notskin', 'Kosong', 'Kosong'
    ishealthy = model2(img).argmax().item()
    if ishealthy == 0:
        return 'healthy', 'Kosong', 'Kosong'
    disease = model3(img).argmax().item()

    return label_decode[disease], disease_to_link[label_decode[disease]], disease_to_step[label_decode[disease]]
