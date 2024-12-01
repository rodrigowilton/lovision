from django.db import models

class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagens/')
    descricao = models.TextField(blank=True)
    data_captura = models.DateTimeField(auto_now_add=True)
