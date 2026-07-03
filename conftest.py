import sys
import os

# Garante que a pasta raiz do projeto está no sys.path,
# permitindo que os testes importem 'from src.xxx import ...'
sys.path.insert(0, os.path.dirname(__file__))
