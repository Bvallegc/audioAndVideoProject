import gradio as gr
from translator import Translator  # Assuming you have a Translator class for translation
import os
import traceback

a = os.path.join(os.path.dirname(__file__), "pancho.mp4")
b = os.path.join(os.path.dirname(__file__), "castillo_short.mp4")
c = os.path.join(os.path.dirname(__file__), "beltransitoIngles.mp4")

output_example_a = os.path.join(os.path.dirname(__file__), "pancho_frances.mp4")
output_example_b = os.path.join(os.path.dirname(__file__), "castillo_ingles.mp4")
output_example_c = os.path.join(os.path.dirname(__file__), "beltransitoAleman.mp4")

def translate_video(language, video):
    try:
        print(f"Type of language: {type(language)}")
        print(f"Value of language: {language}")

        video_path = '/private/var/folders/ng/n9ng0wy92t90_49j662nh02c0000gn/T/gradio/f8645bed8e121ce9cb616e0aeb318bbcef2a2429/pancho.mp4'
        video_path2 = '/private/var/folders/ng/n9ng0wy92t90_49j662nh02c0000gn/T/gradio/937f952e2e1a50bf99d727ee085bee7eb38bba40/castillo_short.mp4'
        video_path3 = '/private/var/folders/ng/n9ng0wy92t90_49j662nh02c0000gn/T/gradio/3a5c43134f4ee5b85fc49ab35f72c8aed0c5f60b/beltransitoIngles.mp4'

        if video == video_path:
            print("Returning output_example_a")
            return output_example_a
        elif video == video_path2:
            print("Returning output_example_b")
            return output_example_b
        elif video == video_path3:
            print("Returning output_example_c")
            return output_example_c
        else:
            print("video is equal to", video)
            print("Returning translated_video_path")
            translator = Translator(language)  # Corrected usage of Translator
            translated_video_path = translator.translate(video)

            return translated_video_path
        
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return None

iface = gr.Interface(
    fn=translate_video, 
    inputs=[gr.Dropdown(choices=['english', 'spanish', 'french', 'german'], label="Language"), gr.Video()],
    examples=[
        ['french', a],
        ['english', b],
        ['german', c],
    ],
    outputs=gr.Video(),
)


iface.launch()
