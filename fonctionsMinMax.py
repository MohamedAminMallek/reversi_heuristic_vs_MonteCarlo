#--- With alpha beta pruning
def negaMaxAlphaBeta(board,profondeur, alpha, beta):
    if (board.is_game_over()) or profondeur == 0:
        h = board.heuristique()
        
        return h
    liste = board.legal_moves()
    
    for i in liste:
        board.push(i)
        val =  - negaMaxAlphaBeta(board, profondeur - 1,-beta,-alpha)
        board.pop()
        if val>=alpha:
            alpha = val
            if alpha >= beta:
                return alpha
    return alpha

MEMORY = {}

def alphaBetaWithMemory(board,profondeur,alpha,beta):
    boardHash = str(board._board)
    if boardHash in MEMORY:
        pos = MEMORY[boardHash]

        if pos[0] >= beta:
            return pos[0]
        if pos[1] <= alpha:
            return pos[1]
        alpha = max(alpha, pos[0])
        beta = min(beta, pos[1])

    liste = board.legal_moves()
    if board.is_game_over() or profondeur == 0:
        h = board.heuristique()
        return h
    a = alpha
    bestMove = None
    current = float('-inf')
    for move in liste:
        board.push(move)
        score = - negaMaxAlphaBeta(board,profondeur-1,-beta,-a)
        
        board.pop()
        if score >= current:
            current = score
            bestMove = move
            if score >= a:
                a = score
                if score >= beta:
                    break

    pos = [float('-inf'),float('inf')]
    if current <= alpha:
        pos[1] = current
    if current > alpha and current < beta:
        pos = [current,current]
    if current >= beta:
        pos[0] = current

    MEMORY[boardHash] = pos
    return current, bestMove

def MTDF(board, profondeur = 4, init_g = 0):
    g = init_g
    upper = float('inf')
    lower = float('-inf')
    beta = 0
    bestMove = None
    while(1):
        if g == lower:
            beta = g +1
        else:
            beta = g
        g, bestMove = alphaBetaWithMemory(board, profondeur, beta-1, beta)
        if g < beta:
            upper = g
        else:
            lower = g

        if(upper == lower):
            break
    del MEMORY[str(board._board)]
    print("best move avec Valeur = ",g)
    return bestMove




#---- Without aplha beta pruning
def negaMaxStandard(board,profondeur):
    if len(board.legal_moves()) == 0 or profondeur == 0:
        h = board.heuristique()
        return h
    liste = board.legal_moves()
    best = float('-inf')
    for i in liste:
        boardCopied = board
        boardCopied.push(i)
        val =  - negaMaxStandard(boardCopied, profondeur - 1)
        boardCopied.pop()
        if val>= best:
            best = val
    return best
def negaStandard(board,profondeur):
    liste = board.legal_moves()
    best = float('-inf')
    bestMove = None
    for move in liste:
        board.push(move)
        val = negaMaxStandard(board,profondeur)
        print(val)
        if best<= val:
            bestMove = move
            best = val
        board.pop()
    return bestMove
