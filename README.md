# Audio and Video Translator


## Overview

This project provides a tool for translating the audio in a video and generating a new video where the speaker appears to be speaking in the translated language. This is achieved using a combination of speech recognition, machine translation, voice cloning, and lip-syncing technologies.

It will use 4 different models in order to achieve the final result. These are:

1. [Whisper](https://github.com/openai/whisper): An ASR (Automatic Speech Recognition) model for speech to text conversion.

2. [CoquiTTS](https://github.com/coqui-ai/TTS/tree/dev): A text to speech model that uses speaker embeddings to clone the voice of the speaker itself and generate an audio based on a text provided.

3. [Wav2Lip](https://github.com/Rudrabha/Wav2Lip): A model that, given a video of a person speaking and an audio, synchronizes the lips of the speaker to the audio provided.

4. [GFPGAN](https://github.com/TencentARC/GFPGAN) (TODO) is a model for image super resolution. We intend to divide the video into frames, apply GFPGAN to each one, and later join them back together to have the final high-resolution lip-synced video.

The main component of this project is the `Translator` class in the [translator.py](translator.py) file. This class has two main methods:

1. `lipsync(video_path='input_video.mp4')`: This method syncs the audio to the video. It calls the Wav2Lip inference file to sync the original video with the generated audio. The `video_path` parameter specifies the path to the video to lipsync and defaults to 'input_video.mp4'.

2. `translate(video_path='input_video.mp4')`: This method generates a lip-synced video. It first validates the video to check if it's 720p resolution and resizes it if needed. Then, it uses the `lipsync` method to sync the translated audio with the video. The `video_path` parameter specifies the path to the video to translate and defaults to 'input_video.mp4'.

The resulting video is saved as 'results/output.mp4'. The speaker in the video appears to be speaking in the translated language, providing a seamless viewing experience for users who speak different languages.

The main component of this project is the `Translator` class in the [translator.py](translator.py) file. This class has two main methods:

1. `lipsync(video_path='input_video.mp4')`: This method syncs the audio to the video. It calls the Wav2Lip inference file to sync the original video with the generated audio. The `video_path` parameter specifies the path to the video to lipsync and defaults to 'input_video.mp4'.

2. `translate(video_path='input_video.mp4')`: This method generates a lip-synced video. It first validates the video to check if it's 720p resolution and resizes it if needed. Then, it uses the `lipsync` method to sync the translated audio with the video. The `video_path` parameter specifies the path to the video to translate and defaults to 'input_video.mp4'.

The resulting video is saved as 'results/output.mp4'. The speaker in the video appears to be speaking in the translated language, providing a seamless viewing experience for users who speak different languages.

## Set up

1. Install all dependencies from the [requirements.txt](requirements.txt) file.
    ```bash
    pip install -r requirements.txt
    ```
2. Install the 'espeak' package using apt-get or brew:
    - On Ubuntu or Debian-based systems, use:
        ```bash
        sudo apt-get install espeak
        ```
    - On macOS, use:
        ```bash
        brew install espeak
        ```
3. Clone the Wav2Lip repository:
   ```bash
   git clone https://github.com/Rudrabha/Wav2Lip.git
   ```

## Usage

To use the translator, follow these steps:

1. Import the `Translator` class from the [translator.py](translator.py) file.

    ```python
    from translator import Translator
    ```

2. Create an instance of the `Translator` class. Pass the language you want to translate to as the only parameter.

    ```python
    translator = Translator('spanish')  # Replace 'spanish' with your desired language
    ```

3. Call the `translate()` method on the `Translator` instance. This method will translate the video located at the path 'input_video.mp4' to the language specified when creating the `Translator` instance. By default, the video path is 'input_video.mp4', but you can pass a different path as a parameter if you want to translate a different video.

    ```python
    translator.translate('path_to_your_video.mp4')  # Replace with your video path if different from 'input_video.mp4'
    ```

This will translate the audio in the video to the specified language, generate new audio with voice cloning, and lipsync the new audio with the original video. The resulting video will be saved as 'results/result_voice.mp4'.