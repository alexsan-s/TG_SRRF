import dropbox
import cv2
dbx = dropbox.Dropbox("sl.Apg2xaL1ZZQ3VfTFnM2Reh8EbMuHhcgpuONV6CprCKbmm5J1dJew5oVGXc5kTbtD9ZD59WB6MZ7xNxei9S6PIMm0pP-Nf30y_Evi0E3EegA5Hxteu36YHEGbPPUMEUNWbYt2qH6m4-w")
dbx.users_get_current_account()

for entry in dbx.files_list_folder('').entries:
    if(entry.name == "viagens-internacionais.jpg"):
        print(entry.name)
        imagem = cv2.imread('https://www.dropbox.com/s/0t9um6mzry0y7o4/viagens-internacionais.jpg?dl=0')
        cv2.imshow("Teste", imagem)
        cv2.waitKey(1)


cv2.destroyAllWindows()