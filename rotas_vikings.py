import heapq
import sys

# Um valor muito grande para representar infinito
INFINITO = float('inf')

def ler_mapa(dados_mapa):
    """Lê os dados do mapa, extrai dimensões, o grid e a posição dos portos."""
    linhas_str = dados_mapa.strip().split('\n')
    
    # A primeira linha contém as dimensões
    try:
        linhas, colunas = map(int, linhas_str[0].split())
        grid_mapa = linhas_str[1:]
    except (ValueError, IndexError):
        print("Erro: Formato de entrada do mapa inválido.")
        return None, None, None, None

    if len(grid_mapa) != linhas:
        print(f"Aviso: O número de linhas no mapa ({len(grid_mapa)}) não corresponde ao especificado ({linhas}).")

    pos_portos = {}
    for r in range(len(grid_mapa)):
        for c in range(len(grid_mapa[r])):
            if '1' <= grid_mapa[r][c] <= '9':
                pos_portos[grid_mapa[r][c]] = (r, c)
    
    return linhas, colunas, grid_mapa, pos_portos

def dijkstra_modificado(grid, inicio, fim):
    """
    Executa o algoritmo de Dijkstra para encontrar o caminho de menor custo (combustível).
    O custo de movimento depende da mudança de direção.
    """
    linhas = len(grid)
    colunas = len(grid[0])
    
    # O estado na fila de prioridade é: (custo, linha, coluna, direcao_chegada)
    # direcao_chegada é uma tupla (dr, dc), ex: (-1, 0) para Norte.
    # (0, 0) indica o ponto de partida, sem direção anterior.
    fila_prio = [(0, inicio[0], inicio[1], (0, 0))]
    
    # distancias armazena o custo mínimo para chegar a um estado (linha, coluna, direcao)
    distancias = {}
    distancias[(inicio[0], inicio[1], (0, 0))] = 0

    # Movimentos possíveis: Norte, Sul, Leste, Oeste
    movimentos = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }

    while fila_prio:
        custo, r, c, dir_anterior = heapq.heappop(fila_prio)

        # Se já encontramos um caminho mais curto para este estado, ignoramos
        if custo > distancias.get((r, c, dir_anterior), INFINITO):
            continue

        # Se chegamos às coordenadas do destino, encontramos o caminho mais curto
        if (r, c) == fim:
            return custo

        # Explora os vizinhos
        for nova_dir_tupla in movimentos.values():
            dr, dc = nova_dir_tupla
            nr, nc = r + dr, c + dc

            # Verifica se o movimento é válido (dentro do mapa e não é um obstáculo)
            if 0 <= nr < linhas and 0 <= nc < colunas and grid[nr][nc] != '*':
                # Calcula o custo do movimento.
                # O primeiro movimento a partir do porto (sem direção anterior) custa 1.
                # Manter a direção custa 1.
                # Mudar de direção (curva) custa 3.
                if dir_anterior == (0, 0) or dir_anterior == nova_dir_tupla:
                    custo_movimento = 1
                else:
                    custo_movimento = 3
                
                novo_custo_total = custo + custo_movimento

                # Se encontrarmos um caminho mais barato para o estado (nr, nc, nova_dir_tupla)
                estado_vizinho = (nr, nc, nova_dir_tupla)
                if novo_custo_total < distancias.get(estado_vizinho, INFINITO):
                    distancias[estado_vizinho] = novo_custo_total
                    heapq.heappush(fila_prio, (novo_custo_total, nr, nc, nova_dir_tupla))
    
    # Se a fila esvaziar e não chegamos ao fim, o destino é inalcançável
    return INFINITO

def calcular_rota_viking(dados_mapa):
    """
    Lê os dados do mapa e calcula o combustível total para a viagem,
    passando pelos portos em ordem.
    """
    linhas, colunas, mapa, portos = ler_mapa(dados_mapa)

    if not all([linhas, colunas, mapa, portos]):
        return

    combustivel_total = 0
    porto_atual = '1'
    
    print(f"Iniciando a grande jornada Viking!\n")

    # Viagens de porto em porto (1 -> 2, 2 -> 3, ..., 8 -> 9)
    for i in range(2, 10):
        proximo_porto = str(i)
        
        if proximo_porto not in portos:
            print(f"AVISO: Porto {proximo_porto} não encontrado no mapa. Pulando para o próximo.")
            continue
        
        if porto_atual not in portos:
             print(f"AVISO: Não é possível partir do porto {porto_atual} pois ele não foi alcançado ou não existe. Pulando trecho.")
             continue

        print(f"Calculando rota do Porto {porto_atual} para o Porto {proximo_porto}...")
        
        pos_inicio = portos[porto_atual]
        pos_fim = portos[proximo_porto]

        custo_trecho = dijkstra_modificado(mapa, pos_inicio, pos_fim)

        if custo_trecho == INFINITO:
            print(f"ALERTA: Porto {proximo_porto} é inalcançável a partir do Porto {porto_atual}. A rota para ele será ignorada.")
        else:
            print(f"Combustível para o trecho: {custo_trecho} unidades.")
            combustivel_total += custo_trecho
            porto_atual = proximo_porto # Atualiza o porto de partida para o próximo trecho
        print("-" * 30)

    # Viagem de volta para casa (último porto visitado -> 1)
    if porto_atual == '1' and combustivel_total == 0:
         print("\nNenhuma viagem foi possível. Os Vikings permanecem em casa.")
         return

    print(f"Calculando rota de volta para casa: do Porto {porto_atual} ao Porto 1...")
    pos_inicio = portos[porto_atual]
    pos_fim = portos['1']
    
    custo_volta = dijkstra_modificado(mapa, pos_inicio, pos_fim)

    if custo_volta == INFINITO:
         print("ALERTA MÁXIMO: Não é possível retornar ao porto inicial! Os Vikings estão perdidos no mar!")
    else:
        print(f"Combustível para a volta: {custo_volta} unidades.")
        combustivel_total += custo_volta

    print("\n==============================================")
    print(f"Missão concluída! Combustível total necessário: {combustivel_total} unidades.")
    print("==============================================")


# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    try:
        dados_mapa = sys.stdin.read()
        calcular_rota_viking(dados_mapa)
    except Exception as e:
        print(f"Ocorreu um erro ao ler a entrada padrão: {e}")
