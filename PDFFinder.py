import os

class PDFFinder:
    def __init__(self, path, log_function = print) -> None:
        self.path = path
        
        self.log_function = log_function
        
    def run(self):
        if not os.path.exists(self.path):
            self.log_function("Diretório não existe!")
            return
        
        return self.list_pdfs_recursively()
            
    def list_pdfs_recursively(self):
        pdfs = []
        for root, dirs, files in os.walk(self.path):
            self.log_function(f"Examinando diretório: {root}")
            for file in files:
                fullpath = os.path.join(root, file)
                if fullpath.endswith(".pdf"):
                    pdfs.append(fullpath)
        
        self.log_function(f"PDFs encontrados: {len(pdfs)}")                    
        return pdfs
            