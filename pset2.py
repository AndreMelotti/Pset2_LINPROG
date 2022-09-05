#!/usr/bin/env python3

# ATENÇÃO: NENHUM IMPORT ADICIONAL É PERMITIDO!
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage

def gerarkernel(raio):                                              # Gera um kernel aleatorio
    kernel = [[0 for t in range(raio)] for t in range(raio)]        # Cria um kernel com um raio especifico e o completa com 0
    for i in range(raio):
        for j in range(raio):
            kernel[i][j] = 1 / (raio * raio)                        # Faz com que o kernel se torne com base no raio
    return kernel


class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):                                      # Nessa função ele pega o valor no ponto espescifico (EX: na "casa" 3 o valor do pixel é 0).
        if x < 0:                                                   # Os "if else" servem como tratamento de erro.
            x = 0                                                   # Eles fazem com que se tiver uma coordenada negativa ou maior que o liimite ela fique enquadrada
        elif x >= self.largura:                                     # no padrão preestabelecido, sendo reformulada.
            x = self.largura - 1
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1
        return self.pixels[(x + y * self.largura)]                  # Retorna o valor do pixel e avança uma "casa".

    def set_pixel(self, x, y, c):                                   # Faz com que o valor do pixel se torne "c".
        self.pixels[(x + y * self.largura)] = c

    def aplicar_por_pixel(self, filtro):                            # Função que muda os valores dos Pixels.
        resultado = Imagem.new(self.largura, self.altura)
        for x in range(resultado.largura):                          # Looping duplo que faz com que repita até acabar a imagem.
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)                          # Atribui a variavel cor o valor do pixel(sua cor).
                nova_cor = filtro(cor)                              # Atribui a variavel nova_cor o parametro que será usado com base na cor dada.
                resultado.set_pixel(x, y, nova_cor)                 # Muda a cor antiga para a redefinida agora.
        return resultado

    def lerkernel(self, k):                                         # Função feita para o programa ler o kernel pixel por pixel
        centro = len(k)//2                                          # Essa variavel "centro" faz com que pegue o centro do kernel (só funciona pois o kernel
        novaimagem = Imagem.new(self.largura, self.altura)          # é impar, ex: 3x3; 5x5 ...)
        for x in range(novaimagem.largura):
            for y in range(novaimagem.altura):
                nova_cor = 0
                for r in range(len(k)):
                    for j in range(len(k)):
                        nova_cor = nova_cor + (self.get_pixel((x - centro + j), (y - centro + r)) * k[r][j])
                novaimagem.set_pixel(x, y, nova_cor)

        return novaimagem

    def lerkernelborrado(self, k):                                  # Função feita para o programa ler o kernel
        centro = len(k)//2                                          #
        novaimagem = Imagem.new(self.largura, self.altura)          #
        for x in range(novaimagem.largura):
            for y in range(novaimagem.altura):
                nova_cor = 0
                for r in range(len(k)):
                    for j in range(len(k)):
                        nova_cor = nova_cor + (self.get_pixel((x - centro + j), (y - centro + r)) * k[r][j])
                novaimagem.set_pixel(x, y, nova_cor)
        novaimagem.corrigir()
        return novaimagem

    def corrigir(self):                                             # Função criada para  arredondar os numeros para inteiros
        for x in range(self.largura):                               # igual pedido na parte 5.1 do pdf do pset2
            for y in range(self.altura):                            # Se o pixel tiver o valor menor que 0, ele vai virar 0
                pixel = self.get_pixel(x, y)                        # e caso ele seja maior do que 255 ele se torna 255.
                if pixel < 0:                                       # Por umltimo ele é transformado em inteiro e arredondado.
                    pixel = 0
                elif pixel > 255:
                    pixel = 255
                pixel = int(round(pixel))
                self.set_pixel(x, y, pixel)

    def invertido(self):                                            # Filtro que inverte a imagem passando um parametro pré estabelecido.
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def borrado(self, raio):                                        # Filtro que borra a imagem passando por algumas funções
        kernel = gerarkernel(raio)
        return self.lerkernelborrado(kernel)

    def focado(self, raio):
        imagemborrada = self.borrado(raio)
        novaimagem = Imagem.new(self.largura, self.altura)
        for x in range(self.largura):
            for y in range(self.altura):
                conta = round(2 * self.get_pixel(x, y) - imagemborrada.get_pixel(x, y))
                novaimagem.set_pixel(x, y, conta)
        novaimagem.corrigir()
        return novaimagem

    def bordas(self):
        novaimagem = Imagem.new(self.largura, self.altura)
        kernel1 = self.lerkernel([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])
        kernel2 = self.lerkernel([[-1, -2, -1],
                                [0,   0,  0],
                                [1,   2,  1]])
        for x in range(self.largura):
            for y in range(self.altura):
                novaimagem.set_pixel(x, y, round(math.sqrt((kernel1.get_pixel(x, y)**2) + kernel2.get_pixel(x, y)**2)))

        novaimagem.corrigir()
        return novaimagem

    # Abaixo deste ponto estão utilitários para carregar, salvar,
    # mostrar e testar imagens.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, arquivo):
        """
        Carrega uma imagem a partir de um arquivo e retorna uma instância
        da classe representando essa imagem. Também realiza a conversão
        para escala de cinza.

        Modo de usar:
           i = Imagem.carregar('imagens_teste/gato.png')
        """
        with open(arquivo, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, largura, altura):
        """
        Cria uma nova imagem em branco (tudo 0) para uma dada largura e altura.

        Modo de uso:
            i = Imagem.new(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, arquivo, modo='PNG'):
        """
        Salva uma dada imagem no disco ou para um objeto semelhante a um
        arquivo. Se "arquivo" é dado como uma string, o tipo de arquivo
        será inferido do próprio nome. Se "arquivo" for dado como um
        objeto semelhante a um arquivo, o tipo de arquivo será determinaddo
        pelo parâmetro "modo".
        """
        out = PILImage.new(mode='L', size=(self.largura, self.altura))
        out.putdata(self.pixels)
        if isinstance(arquivo, str):
            out.save(arquivo)
        else:
            out.save(arquivo, modo)
        out.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo
        a imagem como um GIF. É um utilitário para fazer a função
        mostrar ficar mais limpa.
        """
        buff = BytesIO()
        self.salvar(buff, modo='GIF')
        return base64.b64encode(buff.getvalue())

    def mostrar(self):
        """
        Mostra a imagem em uma janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se o Tk não está inicializado de forma apropriada, não faz nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evendo de redimensionamento (causando um loop infinito). Veja
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.altura,
                                width=self.largura, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        def on_resize(event):
            # Realiza o redimensionamento da imagem quando a janela é redimensionada.
            # O procedimento é:
            #  * Converter para uma imagem PIL
            #  * Redimensionar essa imagem
            #  * Obter o GIF codificado em base64 a partir da imagem redimensionada
            #  * Colocar essa imagem em um label tkinter
            #  * Mostrar essa imagem no canvas
            new_img = PILImage.new(mode='L', size=(self.largura, self.altura))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        # Finalmente, vincular essa função para que ela seja chamada
        # quando a janela for redimensionada.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()

    def reafter():
        tcl.after(500, reafter)

    tcl.after(500, reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco somente será rodado quando você, explicitamente,
    #  rodar seu script, e não quando os testes forem executados. Este é um
    #  bom lugar para gerar imagens, etc.
    pass


    # Questão 6
    # t = Imagem.carregar('imagens_teste/obra.png')
    # tk = t.bordas()
    # tk.salvar('imagem_salva/obraBordas.png')
    # tk.mostrar()
    # t.mostrar()



    # Questão 5.2
    # t = Imagem.carregar('imagens_teste/python.png')
    # tk = t.focado(11)
    # tk.salvar('imagem_salva/pythonNitido.png')
    # tk.mostrar()
    # t.mostrar()



    # Questão 05.1
    # t = Imagem.carregar('imagens_teste/gato.png')
    # tk = t.borrado(5)
    # tk.salvar('imagem_salva/gatoborrado.png')
    # tk.mostrar()
    # t.mostrar()


    #  Questão 04
    # kernel =   [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [1, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # t = Imagem.carregar('imagens_teste/porco.png')
    # tk = t.lerkernel(kernel)
    # tk.mostrar()
    # tk.salvar('imagem_salva/porcoSalvo.png')
    # t.mostrar()


    # Questão 02 do pset2
    # t = Imagem.carregar('imagens_teste/peixe.png')                # Carrega a imagem "peixe.png"
    # peixeInvertido = t.invertido()                                # Utiliza o inverter imagem pra inverter a imagem
    # peixeInvertido.salvar('imagem_salva/peixeInvertido.PNG')     # Salva a imagem na pasta "imagens_teste"


    # O código a seguir fará com que as janelas em Imagem.show
    # sejam mostradas de modo apropriado, se estivermos rodando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
