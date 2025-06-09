Otimização de Rotas Viking - T2 Algoritmos e Estruturas de Dados II


Este projeto contém uma solução em Python para o problema de otimização de rotas de navegação, proposto no Trabalho 2 da disciplina de Algoritmos e Estruturas de Dados II. O objetivo é calcular o consumo mínimo de combustível para uma viagem viking que passa por uma série de portos numa ordem específica.

O Problema
Vikings modernos planeiam uma expedição partindo do porto 1, visitando todos os outros portos de 2 a 9 em sequência e, finalmente, retornando ao porto 1. O desafio reside em calcular o caminho de menor custo (combustível) dadas as seguintes condições:

Mapa: Um mapa em grelha onde . representa água navegável, * representa obstáculos intransponíveis e os dígitos de 1 a 9 marcam os portos.

Movimento: Os barcos movem-se apenas nas quatro direções cardeais (Norte, Sul, Leste, Oeste).

Custo de Combustível:

Mover-se em linha reta consome 1 unidade de combustível.

Mudar de direção (fazer uma curva) consome o triplo, ou seja, 3 unidades de combustível.

Portos Inacessíveis: Se um porto não puder ser alcançado a partir do porto anterior, ele deve ser ignorado, e a viagem continua para o próximo porto da sequência a partir do último porto visitado com sucesso.

A Solução
Para resolver este problema de caminho mínimo num grafo com pesos variáveis nas arestas (o custo depende do movimento anterior), a solução implementa uma versão modificada do Algoritmo de Dijkstra.

A principal adaptação está na definição do "estado" de cada nó na busca. Em vez de considerar apenas a posição (linha, coluna), o nosso estado precisa de incluir a direção a partir da qual chegámos à célula.

Estado no Dijkstra: (custo, linha, coluna, direcao_anterior)

Esta abordagem permite que o algoritmo distinga entre chegar a uma célula vindo do norte ou do leste, por exemplo, e aplique corretamente a penalidade de custo ao avaliar o próximo movimento. Se o próximo movimento mantiver a direcao_anterior, o custo é 1. Se for diferente, o custo é 3.

Estrutura do Código
O script está organizado em três funções principais:

ler_mapa(dados_mapa): Processa o mapa recebido como uma string, extrai as dimensões, a grelha e um dicionário com as coordenadas de cada porto.

dijkstra_modificado(grid, inicio, fim): O núcleo da solução. Executa o algoritmo de Dijkstra com a lógica de custo direcional para encontrar o caminho mais barato entre dois pontos.

calcular_rota_viking(dados_mapa): Orquestra a viagem completa. Itera sobre a sequência de portos (1->2, 2->3, ...), chama a função de Dijkstra para cada trecho, lida com portos inacessíveis e soma o custo total, incluindo a viagem de volta para casa.

Como Executar
O programa foi desenhado para ler os dados do mapa a partir da entrada padrão (stdin). Para executá-lo, utilize o redirecionamento de entrada no seu terminal.

Pré-requisitos:

Python 3 instalado.

Os ficheiros de mapa (mapa100.txt, mapa500.txt, etc.) no mesmo diretório que o script.

Comando de Execução:

python3 rotas_vikings.py < nome_do_ficheiro_do_mapa.txt

Exemplos:

# Para testar com o mapa de 100 colunas
python3 rotas_vikings.py < mapa100.txt

# Para testar com o mapa de 500 colunas
python3 rotas_vikings.py < mapa500.txt

Dependências
O código utiliza apenas bibliotecas padrão do Python:

heapq: Para a implementação eficiente da fila de prioridades (min-heap) no algoritmo de Dijkstra.

sys: Para ler da entrada padrão (sys.stdin).