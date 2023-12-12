import librosa
import torch
import os
import cv2
import subprocess
import moviepy.editor as mp
import soundfile as sf
from moviepy.editor import VideoFileClip
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from TTS.api import TTS
from TTS.tts.utils.managers import EmbeddingManager
from scipy.spatial.distance import cosine

class Translator:
    '''
    Class for translating videos to different languages
    '''
    def __init__(self, language='english'):
        '''
        Initializes the translator with the specified language

        Parameters:
            language (str): The language to translate to. Defaults to 'english'
        '''
        self.language = language
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        model_path = '/Users/franciscomagot/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2'
        config_path = '/Users/franciscomagot/Library/Application Support/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json'

        # if os.path.exists(model_path) and os.path.exists(config_path):
        #     self.tts = TTS(model_path=model_path, config_path=config_path, progress_bar=False).to(self.device)
        # else:
        #     self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(self.device)
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(self.device)


        self.processor = WhisperProcessor.from_pretrained("openai/whisper-large")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")

        self.audio_path = 'temp/audio.wav'

    def set_language(self, language):
        '''
        Sets the language for the translator

        Parameters:
            language (str): The language to translate to
        '''
        self.language = language

    def get_tts_language_code(self):
        '''
        Returns the language code for the TTS model
        '''
        if self.language == 'english':
            return 'en'
        elif self.language == 'spanish':
            return 'es'
        elif self.language == 'french':
            return 'fr'
        elif self.language == 'german':
            return 'de' 

    def get_video_resolution(self, video_path):
        '''
        Function to get the resolution of a video

        Parameters:
            video_path (str): The path to the video to get the resolution of
        '''
        
        video = cv2.VideoCapture(video_path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return (width, height)

    def validate_video(self, video_path):
        '''
        Function to validate video
        '''
        video_duration = mp.VideoFileClip(video_path).duration
        if video_duration > 60:
            print("WARNING: Video duration exceeds 60 seconds. Please use a shorter video.")
            raise SystemExit(0)


        video_resolution = self.get_video_resolution(video_path)
        print(f"Video resolution: {video_resolution}")
        if video_resolution[0] >= 1920 or video_resolution[1] >= 1080:
            print("Resizing video to 720p...")

            new_width = int(720 * video_resolution[0] / video_resolution[1])

            new_width += new_width % 2

            os.system(f"ffmpeg -i {video_path} -vf scale={new_width}:720 temp/resized_video.mp4")
            
            #self.resize_video(video_path)
            
            print("Video resized to 720p")
            return True
        else:
            print("No resizing needed")
            return False

    def extract_audio_from_video(self, video_path):
        '''
        Extracts audio from video and saves it to temp/audio.wav

        Parameters:
            video_path (str): The path to the video to extract audio from.
        '''
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(self.audio_path, codec='pcm_s16le')  # Save as WAV

    def wav_to_txt(self):
        '''
        Generates text from audio using whisper-large
        '''
        self.model.config.forced_decoder_ids = self.processor.get_decoder_prompt_ids(language=self.language, task='transcribe')

        audio, sr = librosa.load(self.audio_path, sr=16000)
        input_features = self.processor(audio, sampling_rate=sr, return_tensors="pt").input_features

        # generate token ids
        predicted_ids = self.model.generate(input_features)

        txt = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
        return txt[0]
    
    def generate_audio(self, text):
        '''
        Generates audio from text using TTS
        '''

        lang = self.get_tts_language_code()
        
        self.tts.tts_with_vc_to_file(text=text, language=lang, speaker_wav = self.audio_path, file_path = 'results/output.wav')

    def lipsync(self, video_path='input_video.mp4'):
        '''
        Lipsyncs audio to video

        Parameters:
            video_path (str): The path to the video to lipsync. Defaults to 'input_video.mp4'
        '''
        output_file_path = 'results/output.mp4'

        pad_top =  0
        pad_bottom = 10
        pad_left =  0
        pad_right =  0
        rescaleFactor = 1
        nosmooth = True

        use_hd_model = False
        checkpoint_path = 'checkpoints/wav2lip.pth' if not use_hd_model else 'checkpoints/wav2lip_gan.pth'


        # Call the Wav2Lip inference file to sync original video with generated audio
        command = f"python3 Wav2Lip2/inference.py --checkpoint_path {checkpoint_path} --face {video_path} --audio 'results/output.wav' --pads {pad_top} {pad_bottom} {pad_left} {pad_right} --resize_factor {rescaleFactor}"

        subprocess.call(command, shell=True)

    def translate(self, video_path='input_video.mp4'):
        '''
        Generates lipsynced video

        Parameters:
            video_path (str): The path to the video to translate. Defaults to 'input_video.mp4'
        '''
        resized = self.validate_video(video_path=video_path) # Check if the video is 720p resolution
        path = "temp/resized_video.mp4" if resized else video_path # Use resized video path if needed

        self.extract_audio_from_video(video_path=path) # Extract audio from original video
        translated_text = self.wav_to_txt() # Generate translated text from original audio
        self.generate_audio(text=translated_text) # Generate audio with voice cloning from translated text and speaker audio
        self.lipsync(video_path=path) # Lipsync generated audio with original video

    def calculate_metrics(self):
        coqui_manager = EmbeddingManager(encoder_config_path='config_se.json', encoder_model_path='model_se.pth.tar')

        og_embeddings = coqui_manager.compute_embedding_from_clip('temp/audio.wav')
        vc_embeddings = coqui_manager.compute_embedding_from_clip('results/output.wav')

        # calculate cosine similarity
        similarity = 1 - cosine(og_embeddings, vc_embeddings)
        return similarity