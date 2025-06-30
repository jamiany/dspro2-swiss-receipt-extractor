import gradio as gr
import torch
from PIL import Image

from donut import DonutModel

def demo_process(input_img):
    input_img = Image.fromarray(input_img)
    output = pretrained_model.inference(image=input_img, prompt="<s_synthetic_data2>")["predictions"][0]
    return output


if __name__ == "__main__":

    pretrained_model = DonutModel.from_pretrained("result/train_cord/test_experiment")

    if torch.cuda.is_available():
        pretrained_model.half()
        device = torch.device("cuda")
        pretrained_model.to(device)

    pretrained_model.eval()

    demo = gr.Interface(
        fn=demo_process,
        inputs="image",
        outputs="json",
        title=f"DSPRO2 - Swiss Receipt Extraction",
    )
    demo.launch(share=True)
