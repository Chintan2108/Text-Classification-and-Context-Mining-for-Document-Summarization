import PyPDF2

tfile = open('proposal.pdf', 'rb')
proposal = PyPDF2.PdfFileReader(tfile)

for pageno in range(proposal.numPages):
    page = proposal.getPage(pageno)
    print(pageno+1)
    print(page.extractText())