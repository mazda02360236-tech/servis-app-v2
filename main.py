def setup_cyrillic_font():
    """Пошук та реєстрація шрифту DejaVuSans для PDF."""
    font_names = ["DejaVuSans.ttf", os.path.join(os.path.dirname(sys.executable), "DejaVuSans.ttf")]
    
    if hasattr(sys, '_MEIPASS'):
        font_names.append(os.path.join(sys._MEIPASS, "DejaVuSans.ttf"))

    for font_path in font_names:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path))
            return 'DejaVuSans'

    # Якщо файл не знайдено локально, завантажуємо з мережі
    try:
        font_path = "DejaVuSans.ttf"
        url = "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf"
        urllib.request.urlretrieve(url, font_path)
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path))
            return 'DejaVuSans'
    except Exception:
        pass

    return 'Helvetica'
