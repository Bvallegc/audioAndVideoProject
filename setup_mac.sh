python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

brew install espeak

git clone https://github.com/Rudrabha/Wav2Lip.git

wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip.pth' -O 'checkpoints/wav2lip.pth'
wget 'https://github.com/justinjohn0306/Wav2Lip/releases/download/models/wav2lip_gan.pth' -O 'checkpoints/wav2lip_gan.pth'