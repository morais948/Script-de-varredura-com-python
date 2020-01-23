from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from tkinter import *
from functools import partial
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
FONTE_PAPYRUS_BOLD = ('papyrus', 16, 'bold')
#configs

config_label = {'font': FONTE_VERDANA_BOLD,  'fg': WhiteSmoke, 'bg': LightSkyBlue, 'pady': 5}
config_entry = {'font': FONTE_PAPYRUS_BOLD,  'fg': LightSlateGray, 'relief': FLAT}
config_bt = {'font': FONTE_PAPYRUS_BOLD, 'bg':  'white', 'fg': LightSkyBlue,
                    'cursor': 'hand2', 'bd': 1, 'relief': SOLID}

class Buscador(object):
    def __init__(self):
        self.janela = Tk()
        self.janela.title('Buscador')
        self.janela['bg'] = LightSkyBlue
        self.janela.wm_iconbitmap('lupa.ico')
        self.janela.resizable(False, False)
        self.criar_tela_inicial()
        self.janela.mainloop()


    def criar_tela_inicial(self):
        self.frame_inicial = Frame(self.janela, bg=LightSkyBlue, bd=10)
        self.frame_inicial.pack(fill=BOTH)
        
        self.label_url = Label(self.frame_inicial, text='URL ', **config_label)
        self.label_url.grid(row=1, column=1)

        self.entrada_url = Entry(self.frame_inicial, **config_entry)
        self.entrada_url.grid(row=1, column=2)
        self.entrada_url.bind("<Key>", self.iniciar)
        self.entrada_url.focus_set()
        self.entrada_url.insert(0, 'cole a url aqui')

    def teste_key(self, evento):
        print(f"tecla pressionada {evento.keycode}")

    def iniciar(self, evento):
       if evento.keycode == 13 and len(self.entrada_url.get()) > 0 and self.entrada_url.get() != 'cole a url aqui':
           self.frame_inicial.pack_forget()
           self.cria_tela_menu()
           
        
    def cria_tela_menu(self):
        self.frame_busca = Frame(self.janela, bg=LightSkyBlue, bd=10)
        self.frame_busca.pack(fill=BOTH)
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.menubar = Menu(self.frame_busca)
        self.menubar.add_command(label="Salvar", command=self.salvar)
        self.menubar.add_command(label="Voltar", command=self.voltar)
        self.menubar.add_command(label="Limpar", command=self.limpar)
        self.janela.config(menu=self.menubar)
        
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.label_tag = Label(self.frame_busca, text='Selecione ', **config_label)
        self.label_tag.grid(row=1, column=1, sticky=E)

        self.entrada_tag = Entry(self.frame_busca, **config_entry)
        self.entrada_tag.grid(row=1, column=2, sticky=W)
        self.entrada_tag.focus_set()

        #em testes---------------
        cadeado = PhotoImage(file="cadeadoFechado.png")
        label_cadeado = Label(self.frame_busca, cursor='hand2', image=cadeado)
        label_cadeado.imagem = cadeado
        label_cadeado.grid(row=1, column=1, sticky=W)
        # em testes---------------

         #-----------------------------------------------------------------------------------------------------------------------------------------------
        delete = PhotoImage(file="delete1.png")
        self.bt_delete = Label(self.frame_busca, cursor='hand2', image=delete)
        self.bt_delete.imagem = delete
        self.bt_delete.grid(row=1, column=2, sticky=E)
        #-----------------------------------------------------------------------------------------------------------------------------------------------
        self.scroll = Scrollbar(self.frame_busca)
        self.scroll.grid(row=4, column=3, rowspan=2, sticky=N+S)
        
        self.text_conteudo = Text(self.frame_busca, wrap=WORD, yscrollcommand=self.scroll.set,
                                  bg=WhiteSmoke)
        self.text_conteudo.grid(row=4, column=1, columnspan=2, sticky=W+E)
        self.scroll.config(command=self.text_conteudo.yview)

        self.chamar_eventos()

    def buscar(self, evento):
        if len(self.entrada_tag.get()) > 0:
            try:
                html = urlopen(self.entrada_url.get())
            except HTTPError as e:
                print(e)
            except URLError as e:
                print('URL errada!')
                
            bs = BeautifulSoup(html, 'html.parser')
            #print(bs)
            conteudos = bs.select(self.entrada_tag.get())
            
            for i in range(len(conteudos)):   
                self.text_conteudo.insert(END,  conteudos[i].get_text() + '\n')
                self.text_conteudo['bg'] = WhiteSmoke          
    
    def chamar_eventos(self):
        self.entrada_tag.bind("<Return>", self.buscar)
        self.bt_delete.bind('<Button-1>', self.limpar_entry)
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
        delete = PhotoImage(file="delete2.png")
        self.bt_delete['image'] = delete
        self.bt_delete.imagem = delete
        
    def trocar_img_leave(self, evento):
        delete = PhotoImage(file="delete1.png")
        self.bt_delete['image'] = delete
        self.bt_delete.imagem = delete

                   
buscador = Buscador()

#trabalhar na funcionalidade do cadeado...

