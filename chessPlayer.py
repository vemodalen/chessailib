import time
from random import randint
from chessPlayer_tree import *

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
    for i in GetPlayerPositions(board,player):
        if board[i] - player == 5:
            king_pos = i 
    	
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

def chessPlayer(board,player):
    status = True
    if len(board) != 64 or player not in [10,20]:
        status = False 
        return [status,[],[],None]
    else:
	    evaltr = tree(board)
	    to_test = evaltr.gen_tree(player)
	    evalTree = to_test.Get_LevelOrder()
    
	    candidateMoves = GetCandidateMoves(board, player)
	    score = to_test.miniMax(3, True,player)
	    print candidateMoves, score
	    move_list = []
	    for i in candidateMoves:
	        if i[1] == score:
	            move_list += [i[0]]
	    print move_list, len(move_list)
	    move = move_list[randint(0, len(move_list)-1)]        
    
    return [status,move,candidateMoves,evalTree]

