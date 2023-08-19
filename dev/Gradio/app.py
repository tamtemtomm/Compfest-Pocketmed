import gradio as gr
from utils import diagnosis

demo = gr.Interface(fn=diagnosis,
                    inputs=gr.Image(shape=(224, 224)),
                    outputs=[gr.Textbox(label="Disease"),
                             gr.Textbox(label="Link"),
                             gr.Textbox(label="Preventive Action")])

if __name__ == '__main__':
    demo.launch(share=True)