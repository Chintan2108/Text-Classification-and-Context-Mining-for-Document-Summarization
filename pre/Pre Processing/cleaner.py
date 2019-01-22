import xlrd

#def clean(response):


data = xlrd.open_workbook("Responses_All About the RMP2031.xlsx","rb")
sheets = data.sheet_names()
file=open("scraped.txt","w")
for sheet_name in sheets:
    sh = data.sheet_by_name(sheet_name)
    i=0
    for rownum in range(sh.nrows):
        row_val = sh.row_values(rownum)
        if row_val[3]:
            #cleaned = clean(row_val[3])
            file.write(str(i)+ '-' + row_val[3]+'\n')
            i+=1

