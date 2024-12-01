import os
from gtts import gTTS

# Defina o caminho completo para o arquivo MP3
diretorio = 'media/descriptions/'
nome_arquivo = 'descricao.mp3'
caminho_completo = os.path.join(diretorio, nome_arquivo)

# Verifique se o diretório existe, se não, crie-o
if not os.path.exists(diretorio):
    os.makedirs(diretorio)

# Crie o arquivo de áudio usando gTTS
tts = gTTS('Sua descrição aqui', lang='pt')
tts.save(caminho_completo)

# Agora o arquivo será salvo corretamente no diretório 'media/descriptions'
