import gradio as gr
from translator import Translator

import traceback

def translate_video(language, video):
    try:
        print(f"Type of language: {type(language)}")
        print(f"Value of language: {language}")
        language_codes = {'english': 'en', 'spanish': 'es', 'french': 'fr', 'german': 'de'}
        language_code = language_codes.get(language, 'en')  # Default to 'en' if language is not found

        translator = Translator(language)
        translator.translate(video.name)
        return 'results/output.mp4'
    except Exception as e:
        print("Exception occurred:", e)
        traceback.print_exc()
        return None

iface = gr.Interface(
    fn=translate_video, 
    inputs=[gr.Dropdown(choices=['english', 'spanish', 'french', 'german'], label="Language"), "file"], 
    outputs="video",
)

iface.launch()