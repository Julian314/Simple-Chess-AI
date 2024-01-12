from NeuralNets import NeuralNetwork, NeuralNetwork_OG, NeuralNetwork_corrected
import torch
from helpers import int_to_binary_10, int_to_binary_44, int_to_binary_6, int_to_binary_64, en_passant, get_stockfish_eval, pawn, rook, bishop_knight, queen
import chess

model5 = NeuralNetwork_corrected(769, [770,512,256,128,64,32,16,1])
model5.load_state_dict(torch.load("ShessGPT_2(3).pth", map_location = torch.device('cpu')))

fen = "8/2p5/p7/P6p/2p4k/2P5/KP4b1/8 w - - 0 44"
board = chess.Board(fen)
moves = list(board.legal_moves)
evals = {}

def best_move(board, is_turn):
    '''RETURNS THE BEST MOVE FOR EITHER BLACK OR WHITE, DEPENDING ON 'IS_TURN' '''
    evals = {}
    moves = list(board.legal_moves)
    for move in moves:
        board.push(move)
        bin_string=int_to_binary_64(int(board.pieces(chess.PAWN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KING, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.PAWN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KING, chess.BLACK)))+str(int(board.turn))+str(int(board.has_kingside_castling_rights(chess.WHITE)))+str(int(board.has_queenside_castling_rights(chess.WHITE)))+str(int(board.has_kingside_castling_rights(chess.BLACK)))+str(int(board.has_queenside_castling_rights(chess.BLACK)))+en_passant(board)+int_to_binary_6(board.halfmove_clock)+int_to_binary_10(board.fullmove_number)
        binary = bytes(int(bin_string[i:i+8],2) for i in range(0,len(bin_string),8))
        bin_string = ''.join(format(byte,'08b')for byte in binary)
        bins = bin_string[:769]
        points_white = pawn(bin_string[:64]) + rook(bin_string[64:128]) + bishop_knight(bin_string[128:256]) + queen(bin_string[256:320])
        points_black = pawn(bin_string[384:448]) + rook(bin_string[448:512]) + bishop_knight(bin_string[512:640]) + queen(bin_string[640:704])
        points = torch.tensor([points_white - points_black])
        bins_ = torch.tensor([float(digit) for digit in bins])
        bins_tensor = torch.cat((bins_, points))
        evals[move] = model5(bins_tensor).item()
        board.pop()
        if is_turn:
            mini = max(list(evals.values()))
        else:
            mini = min(list(evals.values()))
        #print(evals)
    for key in evals:
        if evals.get(key) == mini:
            return (key, evals.get(key))

for move in moves:
    board.push(move)
    black_hole, wert = best_move(board, False)
    evals[move] = wert
    board.pop()
mini = max(evals.values())
for key in evals:
    if evals.get(key) == mini:
        print(key, evals.get(key))
        break 