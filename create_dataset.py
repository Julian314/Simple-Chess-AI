import chess.pgn
from stockfish import Stockfish
from insert_table import insert_table_shessgames
from create_connection import create_connection
from helpers import int_to_binary_10, int_to_binary_44, int_to_binary_6, int_to_binary_64, en_passant, get_stockfish_eval
import time

stockfish = Stockfish(path="/home/arbeite/stockfish/stockfish-ubuntu-x86-64-avx2", parameters={"Threads":4})
pgn = open('lichess_db_standard_rated_2013-04.pgn')

common_openings = []

with open('common_chess_positions.txt', 'r') as f:
    for line in f:
        common_openings.append(line[:len(line) - 1])

conn = create_connection("shess.db") #894828, 1247045, 1442902

count = 0

while True:
    game = chess.pgn.read_game(pgn)
    if game is not None:

        board = game.board()

        white_elo = game.headers["WhiteElo"]
        black_elo = game.headers["BlackElo"]
        if black_elo == '?':
            black_elo = 0
        if white_elo == '?':
            white_elo = 0

        for move in game.mainline_moves():

            board.push(move)
            #Set this number to how many positions you read from the pgn file, this allows to cancel the code and continue later
            if count >= 603577 and board.fen() not in common_openings:
                if count == 603577:
                    print("Success")

                eval = get_stockfish_eval(stockfish, board)
                binary=int_to_binary_64(int(board.pieces(chess.PAWN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.KING, chess.WHITE)))+int_to_binary_64(int(board.pieces(chess.PAWN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.ROOK, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KNIGHT, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.BISHOP, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.QUEEN, chess.BLACK)))+int_to_binary_64(int(board.pieces(chess.KING, chess.BLACK)))+str(int(board.turn))+str(int(board.has_kingside_castling_rights(chess.WHITE)))+str(int(board.has_queenside_castling_rights(chess.WHITE)))+str(int(board.has_kingside_castling_rights(chess.BLACK)))+str(int(board.has_queenside_castling_rights(chess.BLACK)))+en_passant(board)+int_to_binary_6(board.halfmove_clock)+int_to_binary_10(board.fullmove_number)
                binary = bytes(int(binary[i:i+8],2) for i in range(0,len(binary),8))
                insert_table_shessgames(conn,(board.fen(),binary,white_elo,black_elo,eval))
            count += 1
    else:
        break