def int_to_binary_64(num):
    binary_string = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
    binary_string = binary_string.zfill(64)  # Zero-fill to ensure a length of 64 bits
    return binary_string

def int_to_binary_44(num):
    binary_string = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
    binary_string = binary_string.zfill(4)  # Zero-fill to ensure a length of 64 bits
    return binary_string

def int_to_binary_6(num):
    binary_string = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
    binary_string = binary_string.zfill(6)  # Zero-fill to ensure a length of 64 bits
    return binary_string

def int_to_binary_10(num):
    binary_string = bin(num)[2:]  # Convert to binary and remove the '0b' prefix
    binary_string = binary_string.zfill(10)  # Zero-fill to ensure a length of 64 bits
    return binary_string

def en_passant(board):
    if board.ep_square == None:
        return int_to_binary_10(65)
    return int_to_binary_10(int(board.ep_square))

def get_stockfish_eval(stockfish, board):
            stockfish.set_fen_position(board.fen())
            eval_stock = stockfish.get_evaluation()
            if eval_stock['type'] == 'mate':
                if eval_stock['value'] > 0:
                    return max(20, (100 - eval_stock['value'] * 5))
                elif eval_stock['value'] == 0:
                    if board.turn:
                        return -100
                    else:
                        return 100
                elif eval_stock['value'] < 0:
                    return min(-20, -100 - eval_stock['value'] * 5)
            else:
                if eval_stock['value'] > 0:
                    return min(20, eval_stock['value']/100)
                else:
                    return max(-20, eval_stock['value']/100)

def rook(strng):
  zaehler = 0
  for i in range(64):
    if strng[i] == '1':
      zaehler += 1
  return zaehler * 5

def bishop_knight(strng):
  zaehler = 0
  for i in range(128):
    if strng[i] == '1':
      zaehler += 1
  return 3 * zaehler

def queen(strng):
  zaehler = 0
  for i in range(64):
    if strng[i] == '1':
      zaehler += 1
  return 9 * zaehler

def pawn(strng):
  zaehler = 0
  for i in range(64):
    if strng[i] == '1':
      zaehler += 1
  return zaehler