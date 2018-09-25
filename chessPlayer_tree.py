class queue:
    def __init__(self):
        self.list = []

    def enqueue (self,val):
        self.list = self.list + [val]
        #print "enqueue" + str(self.list)

    def dequeue(self):
        if len(self.list) > 0:
            tmp = self.list[0]
            self.list = self.list[1:len(self.list)]
            #print 'dequeue' + str(self.list)
            return tmp
        else:
            return -1

    def pop (self):
        if len(self.list) > 0:
            tmp = self.list[len(self.list)-1]
            self.list = self.list[0:len(self.list)-1]
            return tmp
        else:
            return -1

    def empty (self):
        if self.list == []:
            return True
        else:
            return False

    def length_check(self):
        if len(self.list) > 1:
            return True
        else:
            return False

class tree:

    def __init__(self,board):
        self.store = [board,[]]

    def AddSucc(self, adder):
        self.store[1] = self.store[1] + [adder, []]

    def gen_tree(self, player):
        parent_tree = tree(self.store[0])
        moves = GetMoves(self.store[0], player)

        for i in moves:
            temp = list(self.store[0])
            temp[i[1]] = temp[i[0]]
            temp[i[0]] = 0
            temp_tree = tree(temp)
            if player == 10:
                enemy = 20
            else:
                enemy = 10
            m2 = GetMoves(temp, enemy)
            for j in m2:
                t2 = list(temp)
                t2[j[1]] = t2[j[0]]
                t2[j[0]] = 0
                t2_tree = tree(t2)
                temp_tree.AddSucc(t2_tree)

                m3 = GetMoves(t2, player)
                for j in m3:
                   t3 = list(t2)
                   t3[j[1]] = t3[j[0]]
                   t3[j[0]] = 0
                   t3_tree = tree(t3)
		   t2_tree.AddSucc(t3_tree)
                temp_tree.AddSucc(t2_tree)
            parent_tree.AddSucc(temp_tree)

        return parent_tree


    def Get_LevelOrder(self):
        storage = []
        Q = queue()
        Q.enqueue(self.store)

        while (Q.empty() == False):
            node = Q.dequeue()
            storage = storage + [node[0]]
            for i in range (0,len(node[1]),1):
                if isinstance(node[1][i], tree):
                    Q.enqueue(node[1][i].store)
        return storage

    def miniMax(self,depth,maximizingPlayer, player):
        temp = self.store
        return minimax(temp, depth, maximizingPlayer, player)


def minimax(temp, depth, maximizingPlayer, player):
    if player == 10:
        enemy = 20
    else:
        enemy = 10

    if depth == 1:
        move = ScoreMove(temp[0], player) 
        return move

    if maximizingPlayer == True:
        bestValue = -9999
        for i in temp[1]:
            if isinstance(i, tree):
                v = i.miniMax(depth-1, True, enemy)
                bestValue = max(bestValue,v)
        return bestValue
    else:
        bestValue = 9999
        for i in temp[1]:
            if isinstance(i,tree):
                 v = i.miniMax(depth-1,True, player)
                 bestValue = min(bestValue,v)
        return bestValue

def isEmptyPos(board, pos):
        if board[pos] == 0:
                return True

        else:
                return False

def isOpponentPos(board, player, pos):
        if player == 10:
                if board[pos] in [20,21,22,23,24,25]:
                        return True

                else:
                        return False
        else:
                if IsOnBoard(pos):
                        if board[pos] in [10,11,12,13,14,15]:
                                return True
                        else:
                                return False

def getPiece(name):
   if name=="pawn":
      return 0
   elif name=="knight":
      return 1
   elif name=="bishop":
      return 2
   elif name=="rook":
      return 3
   elif name=="queen":
      return 4
   elif name=="king":
      return 5
   else:
      return -1

def genBoard():
   r=[0]*64
   White=10
   Black=20
   for i in [ White, Black ]:
      if i==White:
         factor=+1
         shift=0
      else:
         factor=-1
         shift=63

      r[shift+factor*7] = r[shift+factor*0] = i+getPiece("rook")
      r[shift+factor*6] = r[shift+factor*1] = i+getPiece("knight")
      r[shift+factor*5] = r[shift+factor*2] = i+getPiece("bishop")
      if i==White:
         r[shift+factor*4] = i+getPiece("queen") # queen is on its own color square
         r[shift+factor*3] = i+getPiece("king")
      else:
         r[shift+factor*3] = i+getPiece("queen") # queen is on its own color square
         r[shift+factor*4] = i+getPiece("king")

      for j in range(0,8):
         r[shift+factor*(j+8)] = i+getPiece("pawn")

   return r

def printBoard(board):
   accum="---- BLACK SIDE ----\n"
   max=63
   for j in range(0,8,1):
      for i in range(max-j*8,max-j*8-8,-1):
         accum=accum+'{0: <5}'.format(board[i])
      accum=accum+"\n"
   accum=accum+"---- WHITE SIDE ----"
   return accum

def GetPlayerPositions(board, player):
	if player not in [10,20]:
		return []
	else:
		pieces = []
		PlayerPositions = []
		for i in range(0,6):
			pieces = pieces + [player + i]
		#print pieces
		for i in range(0,64):
			if board[i] in pieces:
				PlayerPositions = PlayerPositions + [i]		
		#print PlayerPositions	
		return PlayerPositions

def IsOnBoard(pos):
   if (pos >= 0) and (pos <= 63):
      return True
   else:
      return False

def isOpponent(board,player,position):
    if position < 0 or position > 63:
        return False 
    if player == 10:
        if (board[position] - 20) in [0,1,2,3,4,5]:
            return True
    if player == 20:
        if (board[position] - 10) in [0,1,2,3,4,5]:
            return True
    else:
        return False     

def LegalHelp(board,position):
    rightEdge = [7,15,23,31,39,47,55,63]
    leftEdge = [0,8,16,24,32,40,48,56]
    topEdge = [56,57,58,59,60,61,62,63]
    botEdge = [0,1,2,3,4,5,6,7]
    legal = [] 
    moves = []
    if board[position] == 0:
        return False
    piece = board[position]
    empty = []
    for i in range(0,64,1):
        if board[i] == 0:
            empty += [i]        
    
    #Pawn_Pieces         
    if piece == 10:
        left = position + 7
        right = position + 9
        if position not in leftEdge:
	        if isOpponent(board,10,left):
	            legal += [left]
        
        if position not in rightEdge:
		if isOpponent(board,10,right):
	            legal += [right]
            
        if (position+8) in empty:
            legal += [position+8]
        
    if piece == 20:
        left = position - 7
        right = position - 9
        if position not in leftEdge:
		if isOpponent(board,20,left):
        	    legal += [left]
        
        if position not in rightEdge:
		if isOpponent(board,20,right):
        	    legal += [right]

        if (position-8) in empty:
            legal += [position-8]
            
    #King_Pieces 
    if piece == 15 or piece == 25:
        player = 10
        if piece == 25:
            player = 20
            
        forward = position + 8
        backward = position - 8
        right = position + 1
        left = position - 1 
        forward_right = position + 9
        forward_left = position + 7
        backward_right = position - 7
        backward_left = position - 9
        
        if position == 7:
            moves += [forward]
            moves += [left]
            moves += [forward_left]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal 
        
        if position == 63:
            moves += [backward]
            moves += [left]
            moves += [backward_left]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
        
        if position == 0:
            moves += [right, forward, forward_right]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
            
        if position == 56:
            moves += [backward, right, backward_right]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
            
        if position in leftEdge:
            moves += [forward, forward_right, right, backward_right, backward]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
            
        if position in rightEdge:
            moves += [forward, forward_left, left, backward_left, backward]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
            
        if position in topEdge:
            moves += [left, backward_left,backward, backward_right, right]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
            
        if position in botEdge:
            moves += [left, forward_left, forward, forward_right,right]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal
        
        else:
            for i in [1,8,7,9]:
                moves += [position+i]
                moves += [position-i]
            for i in moves:
                if isOpponent(board,player,i):
                    legal += [i]
                if i in empty:
                    legal += [i]
            return legal 
    
    #Knight
    if piece == 11 or piece == 21:
        player = 10
        if piece == 21:
            player = 20
            
        forward = [position + 16,True]
        backward = [position - 16,True]
        right = [position + 2,True]
        left = [position - 2,True] 
        
        if (right[0]-1) in rightEdge:
            right[1] = False
        if (left[0]+1) in leftEdge:
            left[1] = False
        if forward[0] > 63:
            forward[1] = False
        if backward[0] < 0:
            backward[1] = False
        
        for i in [left,right]:
            if i[1] == True:
                if (i[0]+8) in empty or isOpponent(board,player,i[0]+8):
                    legal += [i[0]+8]
                if (i[0]-8) in empty or isOpponent(board,player,i[0]-8):
                    legal += [i[0]-8]
                    
        for j in [forward,backward]:
            if j[1] == True:
                if (j[0]+1) in empty or isOpponent(board,player,j[0]+1):
                    if j[0] not in rightEdge:
                        legal += [j[0]+1]
    
                if (j[0]-1) in empty or isOpponent(board,player,j[0]-1):
                    if j[0] not in leftEdge:
                        legal += [j[0]-1]

    #Rook
    if piece == 13 or piece == 23:
        player = 10
        if piece == 23:
            player = 20
            
        forward = position + 8
        backward = position - 8
        right = position + 1
        left = position - 1 
        
        while forward in empty or isOpponent(board,player,forward):
            if isOpponent(board,player,forward):
                legal += [forward]
                break
            legal += [forward] 
            forward += 8
        
        while backward in empty or isOpponent(board,player,backward):
            if isOpponent(board,player,backward):
                legal += [backward]
                break
            legal += [backward]
            backward -= 8
        
        while right in empty or isOpponent(board,player,right):
            if position in rightEdge:
                break

            if isOpponent(board,player,right):
                legal += [right]
                break
            legal += [right]
            
            if right in rightEdge:
                break
            right += 1
            
        while left in empty or isOpponent(board,player,left):
            if position in leftEdge:
                break
            if isOpponent(board,player,left):
                legal += [left]
                break
            legal += [left] 
            
            if left in leftEdge:
                break
            left = left - 1

    #Bishop 
    if piece == 12 or piece == 22:
        player = 10
        if piece == 22:
            player = 20
            
        forward_right = position + 9
        forward_left = position +7
        backward_right = position -7 
        backward_left = position - 9
        
        
        while forward_right in empty or isOpponent(board,player,forward_right):
            if position in rightEdge:
                break
            if isOpponent(board,player,forward_right):
                legal += [forward_right]
                break
            legal += [forward_right] 
            if forward_right in rightEdge:
                break
            forward_right += 9
        
        while forward_left in empty or isOpponent(board,player,forward_left):
            if position in leftEdge:
                break
            if isOpponent(board,player,forward_left):
                legal += [forward_left]
                break
            legal += [forward_left] 
            if forward_left in leftEdge:
                break
            forward_left += 7
        
        while backward_right in empty or isOpponent(board,player,backward_right):
            if position in rightEdge:
                break
            if isOpponent(board,player,backward_right):
                legal += [backward_right]
                break
            legal += [backward_right] 
            if backward_right in rightEdge:
                break
            backward_right -= 7
        
        while backward_left in empty or isOpponent(board,player,backward_left):
            if position in leftEdge:
                break
            if isOpponent(board,player,backward_left):
                legal += [backward_left]
                break
            legal += [backward_left] 
            if backward_left in leftEdge:
                break
            backward_left -= 9
            
    #Queen
    if piece == 14 or piece == 24:
        player = 10
        if piece == 24:
            player = 20
            
        forward_right = position + 9
        forward_left = position +7
        backward_right = position -7 
        backward_left = position - 9
        forward = position + 8
        backward = position - 8
        right = position + 1
        left = position - 1
        
        while forward in empty or isOpponent(board,player,forward):
            if isOpponent(board,player,forward):
                legal += [forward]
                break
            legal += [forward] 
            forward += 8
        
        while backward in empty or isOpponent(board,player,backward):
            if isOpponent(board,player,backward):
                legal += [backward]
                break
            legal += [backward]
            backward -= 8
        
        while right in empty or isOpponent(board,player,right):
            if position in rightEdge:
                break

            if isOpponent(board,player,right):
                legal += [right]
                break
            legal += [right]
            
            if right in rightEdge:
                break
            right += 1
            
        while left in empty or isOpponent(board,player,left):
            if position in leftEdge:
                break
            if isOpponent(board,player,left):
                legal += [left]
                break
            legal += [left] 
            
            if left in leftEdge:
                break
            left = left - 1
        
        while forward_right in empty or isOpponent(board,player,forward_right):
            if position in rightEdge:
                break
            if isOpponent(board,player,forward_right):
                legal += [forward_right]
                break
            legal += [forward_right] 
            if forward_right in rightEdge:
                break
            forward_right += 9
        
        while forward_left in empty or isOpponent(board,player,forward_left):
            if position in leftEdge:
                break
            if isOpponent(board,player,forward_left):
                legal += [forward_left]
                break
            legal += [forward_left] 
            if forward_left in leftEdge:
                break
            forward_left += 7
        
        while backward_right in empty or isOpponent(board,player,backward_right):
            if position in rightEdge:
                break
            if isOpponent(board,player,backward_right):
                legal += [backward_right]
                break
            legal += [backward_right] 
            if backward_right in rightEdge:
                break
            backward_right -= 7
        
        while backward_left in empty or isOpponent(board,player,backward_left):
            if position in leftEdge:
                break
            if isOpponent(board,player,backward_left):
                legal += [backward_left]
                break
            legal += [backward_left] 
            if backward_left in leftEdge:
                break
            backward_left -= 9
            
    return legal

def IsPositionUnderThreat(board,position,player):
    if position < 0 or position > 63:
        return False 
    OppPos = []
    tmp = []
    
    for i in range (0,64,1):
        if isOpponentPos(board,player,i):
            OppPos += [i]
    for j in OppPos:
        tmp += LegalHelp(board,j)
    if position in tmp:
	return True 
    else:
        return False 

def Check(board,player):
    king_pos = -1
    for i in GetPlayerPositions(board,player):
        if board[i] - player == 5:
            king_pos = i 
    	
    if king_pos in range(0,64):
        if IsPositionUnderThreat(board,king_pos,player):
           return True 
        else:
           return False 
	
def GetPieceLegalMoves(board, position):
    legal = []
    check = False 
    piece = board[position]
    if piece - 20 in [0, 1, 2, 3, 4, 5]:
        player = 20
    if piece - 10 in [0,1,2,3,4,5]:
        player = 10 
    if Check(board,player):
        check = True 
    if not check:
	return LegalHelp(board, position)

    if check:
        for i in LegalHelp(board,position):
	    tmp = list(board)
            tmp[i] = tmp[position]
            tmp[position] = 0 
            if not Check(tmp,player):
		legal += [i]
        return legal 

def GetMoves(board, player):
	accum = []
	pos_list = GetPlayerPositions(board, player)
	tmp = []

	for i in pos_list:
		tmp = GetPieceLegalMoves(board, i)
		for j in tmp:
			accum = accum + [[i, j]]

	return accum

def ScoreMove(board, player):
		white_list = [10,11,12,13,14,15]
		black_list = [20, 21, 22, 23, 24, 25]
		score_list = [10, 30,30, 50, 90, 900]
		score = 0
		for i in range(0,64):
			if player == 10:
				for j in [0,1,2,3,4,5]:
					if board[i] == white_list[j]:
						score = score + score_list[j]
					if board[i] == black_list[j]:
						score = score - score_list[j]
			else:
				for j in [0,1,2,3,4,5]:
                                        if board[i] == white_list[j]:
                                                score = score - score_list[j]
                                        if board[i] == black_list[j]:
                                                score = score + score_list[j]

		return float(score)

def ScoreCandidateMove(board, move, player):
	temp = list(board)
	start = move[0]
	fin = move[1]
	temp[fin] = temp[start]
	temp[start] = 0
	piece = temp[fin]
	piece_score = ScoreMove(temp, player)

	return piece_score

def GetCandidateMoves(board, player):
	moves = GetMoves(board, player)
	accum = []
	score = 0.0

 	for i in moves:
		score = ScoreCandidateMove(board, i, player);
		accum = accum + [[i,score]]

	return accum


