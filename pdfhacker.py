import PyPDF2, os
from sys import argv
import itertools as it

# Usage:
# d.py [brute | dict | pwd] [parameter] [file*]
#
# *file is optional. If not, all files from cwd will be taken.
# brute parameter - length of password
# dict parameter - name of dictionary file
# pwd parameter - password


def decrypt(typ, param, name):
    for n in name:
        pdf_file = open(n, 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        if typ == 'pwd': pdf_reader = pwd(pdf_reader, param)         
        if typ == 'dict': pdf_reader = crack(pdf_reader, param)
        if typ == 'brute': pdf_reader = brute(pdf_reader, param)
            
        if pdf_reader == None:
            print 'Failed decrypt: ' + n
            continue
        else:
            file_name = n[:-4]+"_decrypted.pdf"
            print 'Password cracked. Generating file ' + file_name + '..'
            
            pdf_dec_file = open(file_name, 'wb')
            pdf_writer = PyPDF2.PdfFileWriter()
            
            for page in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page))
            pdf_writer.write(pdf_dec_file)
            print 'Done.'
    return True


def pwd(pdf, pwd):
    if pdf.decrypt(pwd):
        return pdf
    else:
        return None
        
        


def crack(pdf, param):
    dictionary = open(param, 'r')
    
    while True:
        line = dictionary.readline()[:-1]
        if line == '': return None
        if pdf.decrypt(line): return pdf   


def brute(pdf, param):
    param = int(param)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    n = 15
    string = ''
    for i in it.product(chars, repeat=param):
        for j in i:
            string = string + j
        if pdf.decrypt(string): return pdf
        string = ''
    return None
    

if __name__ == '__main__':
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)
    if len(argv) == 3: decrypt(argv[1], argv[2], files)

    if len(argv) == 4: decrypt(argv[1], argv[2], [argv[3]])
    




