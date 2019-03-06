from pdfminer.pdfpage import PDFPage
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
import sys
import os


class PdfConverter:
    '''
    Utility class
    '''

    def __init__(self, file_path):
        self.file_path = file_path

# convert pdf file to a string which has space among words
    def PDFToText(self):
        '''
        This function converts the PDF to text
        '''
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'  # 'utf16','utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(self.file_path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        print('PDF converted to text successfully.')

        return str

    def splitByPara(self, text_string, filename):
        '''
        This function grooms up the processed PDF and returns the paper as
        a list of its paragraphs
        '''
        #print("Paper Name: "+ filename)
        #print("-----------------------------------------------------------------------------------------------------")
        print('Processing ' + filename + '...')
        paragraphs = []
        blocks = text_string.split("\n\n")
        blocks_iter = iter(blocks)
        for l in blocks_iter:
            para = ''
            if len(l) > 200:
                l = l.replace("\n","")
                if l.endswith(tuple(['-', ','])):
                    if(l[-1] == '-'):
                        l = l[:-1]
                    flag = True
                    while(flag):
                        try:
                            next_l = next(blocks_iter)
                        except StopIteration:
                            flag = False
                        if len(next_l) > 200:
                            if next_l[0].islower() or next_l[0].isdigit():
                                flag = False
                                result_l = l + next_l
                                para += result_l
                else:
                    para += l

                if l.endswith(':'):
                        next_l = next(blocks_iter)
                        result_l = l + next_l
                        para += result_l
            paragraphs.append(para)
        
        paragraphs = list(filter(None, paragraphs))
        print('Processed successfully.')

        return paragraphs


def processPDF(path):
    '''
    This function starts a trail of tailing function calls to process and 
    convert the PDF files; arg(path) is the path of the folder containing the 
    PDF files
    This function returns a 2d list, the inner list being the list of paragraphs in 
    the paper and the outer list being the paper(s) itself
    '''
    papers = os.listdir(path)
    papers.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    papers_list = []
    for pdf_file in papers:
        pdfConverter = PdfConverter(file_path=path+pdf_file)
        coverted_text_str = pdfConverter.PDFToText()
        papers_list.append(pdfConverter.splitByPara(coverted_text_str, pdf_file))

    print('2d list populated successfully.')
    
    return papers_list