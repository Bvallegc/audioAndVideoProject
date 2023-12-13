python3 -m venv venv
source venv/bin/activate

pip3 install TTS
pip3 install -r requirements.txt

brew install espeak

git clone https://github.com/panchomb/Wav2Lip.git

wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth' -O 'checkpoints/wav2lip.pth'
wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip_gan.pth' -O 'checkpoints/wav2lip_gan.pth'
wget https://github.com/coqui-ai/TTS/releases/download/speaker_encoder_model/config_se.json -O checkpoints/config_se.json
wget https://github.com/coqui-ai/TTS/releases/download/speaker_encoder_model/model_se.pth.tar -O checkpoints/model_se.pth.tar