### Video and Audio Translation with Lip Syncing

The aim of this project is to recieve a video, translate the audio to the desired language and sync the lips of the person talking in the video.

The dataset that will be used for this project is the following:
>**AV Speech Dataset:**
https://looking-to-listen.github.io/avspeech/download.html 


It will use 4 different models in order to achieve the final result. These are:
1. Whisper/Faster Whisper[https://github.com/openai/whisper] (Speech to text) Whisper an ASR model.
2. CoquiTTS (Text to speech) CoquiTTS[https://github.com/coqui-ai/TTS/tree/dev] is a model that uses speaker embeddings to clone the voice of the speaker itself and generate an audio based on a text provided.
3. Wav2Lip (Lip Syncing) Wav2Lip[https://github.com/Rudrabha/Wav2Lip] is a model that given a video of a person speaking and an audio, the lips of the speaker will be synchronized to the audio provided.
4. TBD (Superresolution) Repo: GFPGAN[https://github.com/TencentARC/GFPGAN] is a model for image super resolution, we intend to divide the video in frames apply GFPGAN in each one of the frames and later join them back together to have the final high resolution lip synced video.