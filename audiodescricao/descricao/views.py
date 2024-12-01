from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
from gtts import gTTS
import os
from .models import Imagem
from .serializers import ImagemSerializer


# Restaura a função index
def index(request):
	return render(request, 'index.html')


class ImagemView(APIView):
	def post(self, request, *args, **kwargs):
		imagem = request.FILES.get('imagem')
		if imagem:
			# Salvar imagem no banco
			imagem_obj = Imagem(imagem=imagem)
			imagem_obj.save()
			
			# Processar imagem com OpenCV
			descricao = self.processar_imagem(imagem_obj.imagem.path)
			
			# Atualizar descrição
			imagem_obj.descricao = descricao
			imagem_obj.save()
			
			# Gerar o áudio da descrição
			self.gerar_audio(descricao)
			
			return Response({'descricao': descricao}, status=status.HTTP_200_OK)
		
		return Response({'error': 'Imagem não enviada'}, status=status.HTTP_400_BAD_REQUEST)
	
	def processar_imagem(self, imagem_path):
		# Ler a imagem com OpenCV
		img = cv2.imread(imagem_path)
		
		# Verificar se a imagem foi carregada corretamente
		if img is None:
			return "Erro ao carregar a imagem."
		
		# Convertendo para tons de cinza
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		# Inicializar detectores de características faciais
		face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
		smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
		
		# Detectar rostos
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
		total_faces = len(faces)
		
		# Detalhar as características faciais
		olhos_detectados = 0
		sorrisos_detectados = 0
		for (x, y, w, h) in faces:
			roi_gray = gray[y:y + h, x:x + w]
			
			# Detectar olhos e sorrisos em cada rosto
			eyes = eye_cascade.detectMultiScale(roi_gray)
			smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
			olhos_detectados += len(eyes)
			sorrisos_detectados += len(smiles)
		
		# Calcular dimensões da imagem
		altura, largura, _ = img.shape
		
		# Analisar cor predominante (média dos canais RGB)
		media_canais = img.mean(axis=(0, 1))
		cor_predominante = f"Azul={int(media_canais[0])}, Verde={int(media_canais[1])}, Vermelho={int(media_canais[2])}"
		
		# Construir descrição narrativa
		descricao = f"Esta é uma imagem de {largura} pixels de largura e {altura} pixels de altura. "
		
		if total_faces == 0:
			descricao += "Nenhum rosto foi detectado na imagem. "
		elif total_faces == 1:
			descricao += "Há um rosto visível na imagem. "
			if sorrisos_detectados > 0:
				descricao += "A pessoa parece estar sorrindo. "
			if olhos_detectados > 0:
				descricao += f"Os olhos estão claramente visíveis. "
		else:
			descricao += f"Há {total_faces} rostos visíveis na imagem. "
			descricao += f"Desses, {sorrisos_detectados} aparentam estar sorrindo. "
		
		descricao += f"A cor predominante na imagem é uma mistura de {cor_predominante}. "
		
		return descricao
	
	def gerar_audio(self, descricao):
		# Usar gTTS para gerar o áudio
		audio_path = os.path.join('media/descriptions', 'descricao.mp3')
		
		# Criar diretório, se necessário
		os.makedirs(os.path.dirname(audio_path), exist_ok=True)
		
		# Gerar o áudio
		tts = gTTS(descricao, lang='pt')
		tts.save(audio_path)
