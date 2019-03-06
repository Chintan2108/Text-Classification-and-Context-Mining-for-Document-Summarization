from process_pdf import PdfConverter

FILEPATH = 'Civis_Bangalore Master Plan_Content.pdf'

if __name__ == "__main__":
    converter = PdfConverter(FILEPATH)

    # converter = PdfConverter(file_path=FILEPATH)
    # converted_text_str = converter.PDFToText()
    # text = converter.splitByPara(converted_text_str, FILEPATH)
    temp = open('Kitty.txt', 'r', encoding='utf-8')
    print(temp.readlines())