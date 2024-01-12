import chess.pgn
from stockfish import Stockfish
import csv
import torch
import torch.nn as nn
from helpers import int_to_binary_10, int_to_binary_44, int_to_binary_6, int_to_binary_64, en_passant, get_stockfish_eval, pawn, rook, bishop_knight, queen
from NeuralNets import NeuralNetwork, NeuralNetwork_OG, NeuralNetwork_corrected

stockfish = Stockfish(path="/home/arbeite/stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads":4})
pgn = open('lichess_db_standard_rated_2013-03.pgn')

model4 = NeuralNetwork_OG()
model5 = NeuralNetwork_corrected(769, [769,512,256,128,64,32,16,1])
model6 = NeuralNetwork_corrected(769,[769,512,256,128,64,32,16,1])

model4.load_state_dict(torch.load("chess_eval_model_jschopp_og.pth", map_location = torch.device('cpu')))
model5.load_state_dict(torch.load("ShessGPT_1.pth", map_location = torch.device('cpu')))
model6.load_state_dict(torch.load("ShessGPT_2(3).pth", map_location = torch.device('cpu')))

with open('evaluations.csv', 'w', newline = '') as csvfile:
    fieldnames = ['Stockfish', 'ShessGPT_1', 'ShessGPT_2', 'ShessGPT_3']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(100):
        game = chess.pgn.read_game(pgn)
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            binary=int_to_binary_64(int(board.pieces(chess.PAWN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KING, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.PAWN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KING, chess.BLACK)))+str(int(board.turn))+str(int(board.has_kingside_castling_rights(chess.WHITE)))+str(int(board.has_queenside_castling_rights(chess.WHITE)))+str(int(board.has_kingside_castling_rights(chess.BLACK)))+str(int(board.has_queenside_castling_rights(chess.BLACK)))+en_passant(board)+int_to_binary_6(board.halfmove_clock)+int_to_binary_10(board.fullmove_number)
            binary = bytes(int(binary[i:i+8],2) for i in range(0,len(binary),8))
            bin_string = ''.join(format(byte,'08b')for byte in binary)

            bins = bin_string[:768]
            points_white = pawn(bin_string[:64]) + rook(bin_string[64:128]) + bishop_knight(bin_string[128:256]) + queen(bin_string[256:320])
            points_black = pawn(bin_string[384:448]) + rook(bin_string[448:512]) + bishop_knight(bin_string[512:640]) + queen(bin_string[640:704])
            points = torch.tensor([points_white - points_black])
            bins_ = torch.tensor([float(digit) for digit in bins])
            bins_tensor = torch.cat((bins_, points))
        
            bin_tensor = torch.tensor([float(digit) for digit in bin_string])
            eval_stock = get_stockfish_eval(stockfish, board)

            writer.writerow({'Stockfish': eval_stock,'ShessGPT_1':model4(bin_tensor).item(), 'ShessGPT_2': model5(bins_tensor).item(), 'ShessGPT_3': model6(bins_tensor).item()})
        
