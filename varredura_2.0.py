from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
#from functools import partial
import os.path

#cores
LightSkyBlue = '#87CEFA'
SkyBlue = '#87CEEB'
SteelBlue = '#4682B4'
LightSlateGray = '#778899'
WhiteSmoke = '#F5F5F5'
PaleGoldenrod = '#EEE8AA'
#fontes
FONTE_VERDANA_BOLD = ('Verdana', 20, 'bold')
FONTE_PAPYRUS_BOLD = ('Verdana',  13, 'bold')
FONTE_VERDANA_NORMAL_PEQUENA = ('Verdana', 13)
#configs

config_label = {'font': FONTE_VERDANA_BOLD,  'fg': WhiteSmoke, 'bg': LightSkyBlue}
config_entry = {'font': FONTE_PAPYRUS_BOLD,  'fg': LightSlateGray, 'relief': FLAT}
config_bt = {'font': FONTE_PAPYRUS_BOLD, 'bg':  'white', 'fg': LightSkyBlue,
                    'cursor': 'hand2', 'bd': 1, 'relief': SOLID}

class Buscador(object):
    def __init__(self):
        self.janela = Tk()
        self.janela.title('Buscador')
        self.janela['bg'] = LightSkyBlue
        self.janela.wm_iconbitmap('imagens/lupa.ico')
        self.janela.resizable(False, False)
        self.criar_tela_inicial()
        self.trancado = False
        self.janela.mainloop()


    def criar_tela_inicial(self):
        self.frame_inicial = Frame(self.janela, bg=LightSkyBlue, bd=10)
        self.frame_inicial.pack(fill=BOTH)
        
        self.label_url = Label(self.frame_inicial, text='URL ', **config_label)
        self.label_url.grid(row=1, column=1)

        self.entrada_url = Entry(self.frame_inicial, **config_entry)
        self.entrada_url.grid(row=1, column=2)
        #self.entrada_url.bind("<Key>", self.iniciar)
        self.entrada_url.bind("<Return>", self.iniciar)
        self.entrada_url.focus_set()
        self.entrada_url.insert(0, 'cole a url aqui')


    def teste_key(self, evento):
        print(f"tecla pressionada {evento.keycode}")

    def iniciar(self, evento):
       if len(self.entrada_url.get()) > 0 and self.entrada_url.get() != 'cole a url aqui':
           self.frame_inicial.pack_forget()
           self.cria_tela_menu()
       else:
           messagebox.showerror('erro', 'Por favor cole a URL')


           
        
    def cria_tela_menu(self):
        self.frame_busca = Frame(self.janela, bg=LightSkyBlue, bd=10)
        self.frame_busca.pack(fill=BOTH)
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.menubar = Menu(self.frame_busca)
        self.menubar.add_command(label="Salvar", command=self.salvar)
        self.menubar.add_command(label="Voltar", command=self.voltar)
        self.menubar.add_command(label="Limpar", command=self.limpar)
        self.menubar.add_command(label="Formatar", command=self.formatar)
        self.janela.config(menu=self.menubar)
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.label_tag = Label(self.frame_busca, text='Selecione    ', **config_label)
        self.label_tag.grid(row=1, column=1, sticky=E)

        self.entrada_tag = Entry(self.frame_busca, **config_entry)
        self.entrada_tag.grid(row=1, column=2, sticky=W)
        self.entrada_tag.focus_set()

     
        cadeado = PhotoImage(file="imagens/cadeadoAberto.png")
        self.label_cadeado = Label(self.frame_busca, cursor='hand2', image=cadeado, bg=LightSkyBlue)
        self.label_cadeado.imagem = cadeado
        self.label_cadeado.grid(row=1, column=1, sticky=W)

         #-----------------------------------------------------------------------------------------------------------------------------------------------
        delete = PhotoImage(file="imagens/delete1.png")
        self.bt_delete = Label(self.frame_busca, cursor='hand2', image=delete, bg=LightSkyBlue)
        self.bt_delete.imagem = delete
        self.bt_delete.grid(row=1, column=1, sticky=E)
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.scroll = Scrollbar(self.frame_busca)
        self.scroll.grid(row=4, column=3, rowspan=2, sticky=N+S)
        
        self.text_conteudo = Text(self.frame_busca, wrap=WORD, yscrollcommand=self.scroll.set,
                                  bg='white', state=NORMAL, font=FONTE_VERDANA_NORMAL_PEQUENA)
        self.text_conteudo.grid(row=4, column=1, columnspan=2, sticky=W+E)
        self.scroll.config(command=self.text_conteudo.yview)

        self.chamar_eventos()

    def buscar(self, evento):
        if len(self.entrada_tag.get()) > 0:
            try:
                html = urlopen(self.entrada_url.get())
                bs = BeautifulSoup(html, 'html.parser')
                conteudos = bs.select(self.entrada_tag.get())

                if len(conteudos) > 0:
                    for i in range(len(conteudos)):
                        self.text_conteudo.insert(END, conteudos[i].get_text()
                                                  + '\n')
                else:
                    messagebox.showwarning('aviso', 'Seleção incorreta')

            except HTTPError as e:
                messagebox.showerror('erro', f'erro HTTP')
            except URLError as e:
                messagebox.showerror('erro', 'URL errada!')
            except:
                messagebox.showerror('erro', 'Por favor verifique a URL')
                

    
    def chamar_eventos(self):
        self.entrada_tag.bind("<Return>", self.buscar)
        self.bt_delete.bind('<Button-1>', self.limpar_entry)
        self.label_cadeado.bind('<Button-1>', self.trancar_destrancar)
        self.bt_delete.bind('<Enter>', self.trocar_img_enter)
        self.bt_delete.bind('<Leave>', self.trocar_img_leave)

    def configure_bt(self, bt, bg, fg, evento):
        bt.configure(bg=bg, fg=fg, font=FONTE_PAPYRUS_BOLD)

    def salvar(self):
        if not os.path.isfile('dados.text'):
            texto = self.text_conteudo.get(1.0, END)
            arquivo = open('dados.text', 'w', encoding='utf8')
            arquivo.write(texto)
            arquivo.close()
        elif os.path.isfile('dados.text'):
            texto = self.text_conteudo.get(1.0, END)
            arquivo = open('dados.text', 'r', encoding='utf8')#somente leitura
            conteudo = arquivo.readlines()
            conteudo.append(texto)

            arquivo = open('dados.text', 'w', encoding='utf8')#escrita
            arquivo.writelines(conteudo)
            arquivo.close()
            

    def voltar(self):
        self.frame_busca.pack_forget()
        self.frame_inicial.pack(fill=BOTH)
        self.janela.config(menu="")

    def limpar(self):
        self.text_conteudo.delete(1.0, END)

    def limpar_entry(self, evento):
        self.entrada_tag.delete(0, END)

    def trocar_img_enter(self, evento):
        delete = PhotoImage(file="imagens/delete2.png")
        self.bt_delete['image'] = delete
        self.bt_delete.imagem = delete
        
    def trocar_img_leave(self, evento):
        delete = PhotoImage(file="imagens/delete1.png")
        self.bt_delete['image'] = delete
        self.bt_delete.imagem = delete

    def trancar_destrancar(self, evento):
        if self.trancado:
            cadeado = PhotoImage(file="imagens/cadeadoAberto.png")
            self.text_conteudo['state'] = NORMAL
            self.trancado = False
        else:
            cadeado = PhotoImage(file="imagens/cadeadoFechado.png")
            self.text_conteudo['state'] = DISABLED
            self.trancado = True
            
        self.label_cadeado['image'] = cadeado
        self.label_cadeado.imagem = cadeado

    def formatar(self):
        texto = self.text_conteudo.get(1.0, END)
        text = texto.split()
        texto_formatado = ' '.join(text)
        self.limpar()
        self.text_conteudo.insert(END,  texto_formatado)

if __name__ == '__main__':
    buscador = Buscador()
