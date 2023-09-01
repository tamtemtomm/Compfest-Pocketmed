import os
import torch
from skinmodels import IsSkinResnet, IsHealthySkinResnet, SkinDiseaseModelResnet
from config import read_disease_step, read_label_decode, transform_img
from config_path import SKINMODEL1_PATH, SKINMODEL2_PATH, SKINMODEL3_PATH, SKINDISEASE_STEP_PATH, SKINLABEL_DECODE_PATH

def diagnosis(img):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    img = transform_img(img).to(device=device)
    
    # Setup disease step
    disease_to_link, disease_to_step = read_disease_step(SKINDISEASE_STEP_PATH)
    
    # Setup label decode
    label_decode, num_class = read_label_decode(SKINLABEL_DECODE_PATH)
    
    # Setup model1
    assert os.path.isfile(
        SKINMODEL1_PATH), f"Can't find model state_dict path  : {SKINMODEL1_PATH}"
    model1 = IsSkinResnet().to(device)
    model1.load_state_dict(torch.load(
        SKINMODEL1_PATH, map_location=torch.device(device)))
    
    # Setup model2
    model2 = IsHealthySkinResnet().to(device)
    assert os.path.isfile(
        SKINMODEL2_PATH), f"Can't find model state_dict path  : {SKINMODEL2_PATH}"
    model2.load_state_dict(torch.load(
        SKINMODEL2_PATH, map_location=torch.device(device)))

    # Setup model3
    model3 = SkinDiseaseModelResnet(num_class).to(device)
    assert os.path.isfile(
        SKINMODEL3_PATH), f"Can't find model state_dict path  : {SKINMODEL3_PATH}"
    model3.load_state_dict(torch.load(
        SKINMODEL3_PATH, map_location=torch.device(device)))
    
    # Diagnosis
    isskin = model1(img).argmax().item()
    if isskin == 1:
        return 'notskin', 'Kosong', 'Kosong'
    ishealthy = model2(img).argmax().item()
    if ishealthy == 0:
        return 'healthy', 'Kosong', 'Kosong'
    disease = model3(img).argmax().item()

    return label_decode[disease], disease_to_link[label_decode[disease]], disease_to_step[label_decode[disease]]
