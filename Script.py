import os
import sqlite3 as sqlite
import smtplib
from PdfManipulation import *
from Database import *
from Email import *

if __name__ == '__main__':
    EMAIL_ADDRESS = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    conn = sqlite.connect("./Database/Mydatabase.db")
    create_database(conn)
    encrypt_database()
    cursor = conn.cursor()

    server = smtplib.SMTP_SSL('smtp.gmail.com')
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    index = 0
    if(os.stat("EmailStatus.txt").st_size != 0):
        file = open("EmailStatus.txt", "r")
        for line in file:
            pass
        index = int(line.split()[-1])
        file.close()

    #Compress the PDF 
    compress_pdf('./Pdf/Main.pdf')

    cursor.execute("SELECT Count(*) FROM ServingOfficers")
    length = cursor.fetchone()[0]

    if(index == length):
        #Clear text file
        open('EmailStatus.txt', 'w').close()
        index =0 

    cursor.execute("SELECT * FROM ServingOfficers")
    for row in cursor:
        sno = row[0]

        if(sno > index):
            #Fetch data from the database
            dob = row[1]
            dob = dob.split()[0]
            dob = dob.split('-')[::-1]
            dob = ''.join(dob)

            name = row[2]
            email = row[4]

            password = name[:4].upper() + dob

            # Annotate and Encrypt PDF
            create_annotation('Annotation.pdf', name)
            merge_annotation('./Pdf/Compressed_Main.pdf', 'Annotation.pdf')
            encrypt_pdf(None, password,'Watermarked_Compressed_Main.pdf', name + '.pdf')

            # Create and send email
            msg = create_msg(email, name+'.pdf')
            server.send_message(msg)

            # Save progress
            file = open("EmailStatus.txt", "a")
            file.write("Email sent to sno {num}\n".format(num=sno))
            file.close()

            #Remove files
            os.remove(name+'.pdf')
            os.remove('Watermarked_Compressed_Main.pdf')
            os.remove('Annotation.pdf')

    conn.commit()
    conn.close()

    os.remove("./Pdf/Compressed_Main.pdf")
    os.remove("./Database/Mydatabase.db")

    server.close()
