# -*- coding: utf-8 -*-

from PDFFinder import PDFFinder
from PDFTextReplacer import PDFTextReplacer

import tkinter as tk
from tkinter import filedialog, messagebox
import os

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Substituidor de textos de PDF")
        self.master.configure(padx=16, pady=16)

        self.dir_label = tk.Label(master, text="Diretório:")
        self.dir_label.grid(row=0, column=0, sticky=tk.W)
        
        self.dir_entry = tk.Entry(master, width=50)
        self.dir_entry.grid(row=1, column=0, sticky=tk.W)
        self.browse_button = tk.Button(master, text="Selecionar", command=self.browse_directory)
        self.browse_button.grid(row=1, column=1)
        self.browse_button.configure(padx=10)
        
        self.target_text_label = tk.Label(master, text="Textos a serem substituídos: (separar por linha)")
        self.target_text_label.grid(row=2, column=0, sticky=tk.W)
        
        self.target_text = tk.Text(master, height=15, width=80)
        self.target_text.grid(row=3, columnspan=3)
        
        self.replacement_text_label = tk.Label(master, text="Texto a ser inserido: (vazio para apenas remover)")
        self.replacement_text_label.grid(row=4, column=0, sticky=tk.W)
        
        self.replacement_text = tk.Entry(master, width=50)
        self.replacement_text.grid(row=5, column=0, sticky=tk.W)
        
        
        self.submit_button = tk.Button(master, text="Substituir", command=self.submit_form)
        self.submit_button.grid(row=6, columnspan=3, pady=10)
        self.submit_button.configure(padx=10)
        
        self.log_label = tk.Label(master, text="Logs:")
        self.log_label.grid(row=7, column=0, sticky=tk.W)
        

        self.log_text = tk.Text(master, height=10, width=80)
        self.log_text.grid(row=8, columnspan=3)
        
    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(tk.END, directory)
        
    def insert_log(self, log):
         self.log_text.insert(tk.END, f"[LOG] {log} \n")
         self.log_text.see(tk.END)
         self.master.update_idletasks()

    def submit_form(self):
        directory = self.dir_entry.get()

        if not directory:
            self.insert_log("Por favor, selecione um diretório.")
            return
        
        if not os.path.exists(directory):
            self.insert_log( "Diretório não encontrado.")
            return 
        try:
            target_text =  self.target_text.get("1.0", "end-1c").strip()
            
            if len(target_text) < 1:
                raise Exception("Texto a ser substituído não foi informado")
            
            target_texts = target_text.split("\n")
        
            finder = PDFFinder(directory, log_function=self.insert_log)
            pdf_list = finder.run()
            self.insert_log(f"entradas: {target_texts}")
            
            if (len(pdf_list) < 1):
                raise Exception("Nenhum PDF encontrado")

            replacer = PDFTextReplacer(pdf_list=pdf_list, target_text=target_texts, replacement_text=self.replacement_text.get(), log_function=self.insert_log)
            replacer.run()
            self.log_text.insert(tk.END, "Ação concluída com sucesso!\n")
            messagebox.showinfo("Sucesso", "Ação concluída com sucesso!")
        
        except Exception as e:
            self.insert_log(f"Erro: {str(e)}\n")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

