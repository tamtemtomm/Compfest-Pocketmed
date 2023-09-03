# Pocketmed
Pocketmed is a tool to check diseases from images. User can check skin and eye health by upload photo into the application

## How to Use?

1. You can use this [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16kHxAnUV35AvUCunFFaapUP9eNnCxCFk?usp=sharing) notebook to run the program remotely

2. Run the notebook <br> <br>
![alt text](https://github.com/tamtemtomm/Compfest-Pocketmed/assets/92860332/5198f69b-4257-44cb-82f9-40d7f4d10969)

3. Wait until the demo start <br> <br>
![alt text](https://github.com/tamtemtomm/Compfest-Pocketmed/assets/92860332/6bf525a3-9674-4350-9079-57a535e20601)

3. Have Fun!

4. You can also check our HuggingSpace space in this [link](https://xmaulana-compfest-pocketmed.hf.space/), so you dont have to run it by yourself in google colab or your personal computer.

## Installation and usage instructions (for contributors)

1. Clone this repository. You can copy this code to your terminal
   <br> <br>
   ```rb
    $ git clone https://github.com/tamtemtomm/Compfest-Pocketmed.git
    ```
2. Download the pretrained model and other config files in this [link](https://drive.google.com/uc?id=1wN0JJHgeMVTrYdptmz3GmGdsCEPDUtPK)
3. Move and unzip tools.zip file inside the ./dev folder
4. For gradio demo, executes this command:
   <br> <br>
   ```rb
    cd .\dev
    cd .\Gradio
    python app.py
    ```
5. For flask demo, executes this command:
   <br> <br>
   ```rb
    cd .\dev
    cd .\Flask
    python app.py
    ```
## Documentation
### Model Training Stage
Here we provide some link that explain about the training stage of the model.
<br>
| Colab | Model Training
| --- | --- |
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11l_fi84VTUVUMFqeUnmNlIW-gaLtOVdw?usp=sharing) | Skin Disease Classification
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1-QGQv_WJolS1b0PXUZ_67Bu4OIoedUGx?usp=sharing) | Healthy Skin Check
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1RXDiNII5EZNxybXcp_g0Lo9avBjgG0QQ?usp=sharing) | Skin Check

## Known issues (On Development!)
1. Flask UI still don't responsive with user's device
2. Chatbot system is not working
3. Model's accuracy still a bit bad

Thank you for coming in!
