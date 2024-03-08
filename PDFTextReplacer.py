import os

from spire.pdf.common import *
from spire.pdf import *

class PDFTextReplacer:
    def __init__(self, target_text, pdf_list,replacement_text = "", output_folder = None,  log_function = print) -> None:
        self.target_text = target_text
        self.replacement_text = replacement_text
        self.pdf_list = pdf_list
        self.output_folder = output_folder
        
        self.log_function = log_function
        
    def replace_text_in_pdf(self, input_pdf_path):     
        
        
        try:
            doc = PdfDocument()
            doc.LoadFromFile(input_pdf_path)
            
            for i in range(doc.Pages.Count):
                page = doc.Pages[i]   
                self.log_function(f"Modificando página {i + 1} de {doc.Pages.Count}")
                replacer = PdfTextReplacer(page)
                
                for text in self.target_text:
                    replacer.ReplaceAllText(text, self.replacement_text)


            file_name, file_extension = os.path.splitext(os.path.basename(input_pdf_path))
            save_path = f"{self.output_folder}/{file_name}_modified.pdf" if self.output_folder is not None else input_pdf_path
            
            doc.SaveToFile(save_path)

            doc.Close()
        except:
            self.log_function(f"erro ao manipular: '{input_pdf_path}'")

        
    def run(self):
        if self.output_folder is not None and not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        for pdf_path in self.pdf_list:
            self.log_function(f"modificando: '{pdf_path}'")
            self.replace_text_in_pdf(input_pdf_path=pdf_path )