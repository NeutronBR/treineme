import hashlib
import string
import random


def chave_aleatoria(tamanho=5):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for x in range(tamanho))


def gerar_hash_chave(sal, tamanho_aleatorio_str=5):
    str_aleatoria = chave_aleatoria(tamanho_aleatorio_str)
    texto = str_aleatoria + sal
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()
