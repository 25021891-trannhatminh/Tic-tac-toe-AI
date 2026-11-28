import random


def heuristic_rollout(game, state):
    """
    Rollout có luật ưu tiên:  Thắng ngay  ->  Chặn đối thủ thắng ngay  ->  Đi ngẫu nhiên.
    Trả về người thắng (1 / -1) hoặc None (hòa).

    Idea:
      * `win_potential_move[p]` = tập ô "win potential" của player.
      * Mỗi khi player đặt quân tại (row,col), check các ô local quanh nó bán kính win_length -> True = thêm vào win_potential_move[player].
      * Khi cần dùng, ô ứng viên được kiểm tra lại bằng game.wins_at (ô cũ đã bị chặn
        hoặc đã bị chiếm thì loại bỏ). Ô thắng chỉ có thể xuất hiện lại khi p đặt quân mới
        -> lúc đó đã được thêm lại, nên loại bỏ như vậy là an toàn.
      * Danh sách ô trống dùng swap-remove: lấy ngẫu nhiên và xóa đều O(1).
    """
    winner = game.get_winner(state)
    if winner is not None:
        return winner

    board_size, win_length = game.size, game.win_length
    directions = game.DIRECTIONS
    board = [list(row) for row in state[0]]
    player = state[1]                                  

    empties = [(row, col) for row in range(board_size) for col in range(board_size) if board[row][col] == 0]
    index = {cell: i for i, cell in enumerate(empties)}  # Map {(row,col) : index của empties}
    win_potential_move = {1: set(), -1: set()}                    # Vị trí dọa win của player 1 / -1

    def add_threats(row, col, player):
        """Sau khi player đánh (row,col): tìm ô dọa win ngay, local quanh (row,col) 1 khoảng win_length """
        for direct_row, direct_col in directions:
            for s in range(-(win_length - 1), 1):                 # Xác định đầu, cuối dãy dài win_length trong local của (row,col)
                row_first, col_first = row + s * direct_row, col + s * direct_col
                row_last, col_last = row_first + (win_length - 1) * direct_row, col_first + (win_length - 1) * direct_col
                if not (0 <= row_first < board_size and 0 <= col_first < board_size and 0 <= row_last < board_size and 0 <= col_last < board_size):
                    continue
                gap = None
                for i in range(win_length):                       # Scan lần lượt từng ô của dãy dài win_length
                    row_scan, col_scan = row_first + i * direct_row, col_first + i * direct_col
                    player_in_board = board[row_scan][col_scan]
                    if player_in_board == player:
                        continue
                    if player_in_board == 0 and gap is None:      # Gặp ô trống trong dãy win_length
                        gap = (row_scan, col_scan)
                        continue
                    gap = None                           # có quân đối thủ hoặc >= 2 ô trống
                    break
                if gap is not None:
                    win_potential_move[player].add(gap)

    def find_win(player):
        """Một ô mà player đi vào là thắng ngay, hoặc None."""
        cells = win_potential_move[player]
        while cells:
            cell = next(iter(cells))
            r, c = cell
            if board[r][c] == 0:
                board[r][c] = player
                ok = game.wins_at(board, r, c)
                board[r][c] = 0
                if ok:
                    return cell
            cells.discard(cell)
        return None

    # Add potential win từ các ô đã đánh
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != 0:
                add_threats(row, col, board[row][col])

    while empties:
        move = find_win(player)
        won = move is not None                           # đi vào ô này là thắng chắc
        if not won:
            move = find_win(-player)                     # chặn ô win của đối thủ
        if move is None:
            move = empties[random.randrange(len(empties))]  # chọn ngẫu nhiên

        # Xóa move khỏi empties với O(1)
        i = index.pop(move)         # i = index của move trong empties   O(1)
        last = empties.pop()        # xóa last_move bất kỳ trong empties O(1)
        if last != move:            
            empties[i] = last       # Swap last_move đó vào index của move
            index[last] = i         # -> xóa move trong empties O(1)

        row, col = move
        board[row][col] = player    # Lượt chơi của player
        if won or game.wins_at(board, row, col):
            return player
        add_threats(row, col, player)
        player = -player

    return None
