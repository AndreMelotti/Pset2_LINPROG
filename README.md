# Pset2 - Processamento de Imagem
Esse trabalho consiste em aprender a usar um kernel, e criar filtros de processamento de imagens utilizando python.
Feito por André Melotti.

## Questão 01:
O input recebido pelo programa foi (4, 1, [29, 89, 136, 200]), o Filtro de inversão faz com que seja pego os valores dos pixels sejam mudados pelo seu inverso (no caso
diminuindo o valor de 255, o máximo), tendo o onput final esperado sendo (4, 1, [226, 166, 119, 55]), Invertendo assim a tonalidade de preto, branco e cinza da imagem.

## Questão 02:
Consistia em iverte a imagem "peixe", o resultado foi:

![peixeInvertido](https://user-images.githubusercontent.com/103462954/188498171-c04fe7da-29eb-4006-8666-9669644f6254.PNG)

## Questão 03:
Fazendo a multiplicação pixel por pixel temos:
80 x 0,00 = 0

53 x -0,07 = -3,71

99 x 0,00 = 0

129 x -0,45 = -58,05

127 x 1,20 = 152,40

148 x -0,25 = -37

175 x 0,00 = 0

174 x -0,12 = -20,88

193 x 0,00 = 0

Fazendo a soma total dos resltados nós temos: **32,76**

## Questão 04:
Utilizando o Kernel passado no pdf do trabalho temos como resultado a imagem do "porco" dessa forma:

![porcoSalvo](https://user-images.githubusercontent.com/103462954/188499135-559b9543-fee8-426e-9085-f7f774061cff.png)

Nota-se que a imagem foi bem pouco deslocada para a diagonal inferior direita.

## Questão 05: 
Usando o filtro de "Borrado" na imagem do gato nós  temos:

![gatoborrado](https://user-images.githubusercontent.com/103462954/188499666-4d6da1f1-428a-48f8-ae65-372aefb9cc12.png)

Caso houvesse a necessidade de usar uma versão desfocada com um kernel de desfoque de 3 x 3, o cálculo seria:
kn_1 = [[0, 0, 0], [0, 2, 0], [0, 0, 0]]

operação (-)

kn_2 = [[1/9, 1/9, 1/9],
[1/9, 1/9, 1/9],
[1/9, 1/9, 1/9]]

Agora, subtraindo os pixels do kernel 1 (kn_1) pelos pixels do kernel 2 (kn_2) pelas suas respectivas posições, o resultado será

kn = [[-1/9, -1/9, -1/9],
[-1/9, 17/9, -1/9],
[-1/9, -1/9, -1/9]].
