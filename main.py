import sys
import os
import sqlite3
import urllib.request
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QDateEdit, QComboBox
)
from PyQt6.QtCore import QDate

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def setup_cyrillic_font():
    """Завантажує шрифт Roboto з Google Fonts для підтримки кирилиці."""
    font_path = "Roboto-Regular.ttf"
    
    if not os.path.exists(font_path):
        try:
            # Пряме посилання на шрифт з Google Fonts
            url = "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf"
            urllib.request.urlretrieve(url, font_path)
        except Exception:
            pass

    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Roboto', font_path))
        return 'Roboto'
    
    return 'Helvetica'
