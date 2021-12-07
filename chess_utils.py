def parse_moves(game_str: str):
    # Parses moves from a str representing a chess game.
    # Example game_str: "1.c4 g6 2.d4 Bg7 3.e4 d6 4.Nc3 c5 5.dxc5 Bxc3+ 6.bxc3 dxc5 7.Bd3 Nc6 8.f4 Qa5 9.Ne2 Be6 10.f5 O-O-O 11.fxe6 Ne5 12.exf7 Nf6 13.O-O Nxd3 14.Bh6 Ne5 15.Qb3 Nxf7" 
    tokens = game_str.split()
    moves = []
    for t in tokens:
        period_index = t.find(".")
        moves.append(t[period_index+1:])
    return moves