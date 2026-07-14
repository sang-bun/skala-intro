import pygame
import random
import sys
import os

# 게임 화면 설정
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDE_WIDTH = 200

SCREEN_WIDTH = BOARD_WIDTH * BLOCK_SIZE + SIDE_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE

FPS = 60


# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (100, 100, 100)

COLORS = [
    (0, 255, 255),    # I 블록
    (0, 0, 255),      # J 블록
    (255, 165, 0),    # L 블록
    (255, 255, 0),    # O 블록
    (0, 255, 0),      # S 블록
    (128, 0, 128),    # T 블록
    (255, 0, 0),      # Z 블록
]


# 테트리스 블록 모양
# 1은 블록이 존재하는 위치를 의미한다.
SHAPES = [
    # I 블록
    [
        [1, 1, 1, 1]
    ],

    # J 블록
    [
        [1, 0, 0],
        [1, 1, 1]
    ],

    # L 블록
    [
        [0, 0, 1],
        [1, 1, 1]
    ],

    # O 블록
    [
        [1, 1],
        [1, 1]
    ],

    # S 블록
    [
        [0, 1, 1],
        [1, 1, 0]
    ],

    # T 블록
    [
        [0, 1, 0],
        [1, 1, 1]
    ],

    # Z 블록
    [
        [1, 1, 0],
        [0, 1, 1]
    ]
]


class Block:
    """떨어지는 테트리스 블록을 나타내는 클래스"""

    def __init__(self):
        # 블록 종류를 무작위로 선택한다.
        self.shape_index = random.randrange(len(SHAPES))
        self.shape = SHAPES[self.shape_index]
        self.color = COLORS[self.shape_index]

        # 블록을 게임판 위쪽 중앙에 배치한다.
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0


def create_board():
    """빈 게임판을 생성한다."""

    return [
        [None for _ in range(BOARD_WIDTH)]
        for _ in range(BOARD_HEIGHT)
    ]


def rotate_shape(shape):
    """블록 모양을 시계 방향으로 회전한다."""

    # 행과 열을 뒤집어 시계 방향으로 회전한다.
    return [list(row) for row in zip(*shape[::-1])]


def is_valid_position(board, block, move_x=0, move_y=0, new_shape=None):
    """블록을 이동하거나 회전할 수 있는지 검사한다."""

    # 회전된 모양이 전달되지 않으면 현재 모양을 사용한다.
    shape = new_shape if new_shape is not None else block.shape

    for row_index, row in enumerate(shape):
        for column_index, value in enumerate(row):

            # 블록이 없는 위치는 검사하지 않는다.
            if value == 0:
                continue

            new_x = block.x + column_index + move_x
            new_y = block.y + row_index + move_y

            # 게임판 좌우를 벗어났는지 검사한다.
            if new_x < 0 or new_x >= BOARD_WIDTH:
                return False

            # 게임판 아래를 벗어났는지 검사한다.
            if new_y >= BOARD_HEIGHT:
                return False

            # 게임판 내부에 이미 다른 블록이 있는지 검사한다.
            if new_y >= 0 and board[new_y][new_x] is not None:
                return False

    return True


def place_block(board, block):
    """떨어진 블록을 게임판에 고정한다."""

    for row_index, row in enumerate(block.shape):
        for column_index, value in enumerate(row):

            if value == 1:
                board_y = block.y + row_index
                board_x = block.x + column_index

                if 0 <= board_y < BOARD_HEIGHT:
                    board[board_y][board_x] = block.color


def clear_full_lines(board):
    """완성된 줄을 삭제하고 삭제된 줄의 수를 반환한다."""

    # 한 줄에 빈칸이 없는 줄만 찾는다.
    remaining_rows = [
        row for row in board
        if any(cell is None for cell in row)
    ]

    cleared_lines = BOARD_HEIGHT - len(remaining_rows)

    # 삭제된 줄 수만큼 빈 줄을 위쪽에 추가한다.
    for _ in range(cleared_lines):
        remaining_rows.insert(0, [None for _ in range(BOARD_WIDTH)])

    board[:] = remaining_rows

    return cleared_lines


def calculate_score(cleared_lines):
    """삭제한 줄 수에 따라 점수를 계산한다."""

    score_table = {
        1: 100,
        2: 300,
        3: 500,
        4: 800
    }

    return score_table.get(cleared_lines, 0)


def draw_board(screen, board):
    """게임판과 고정된 블록을 화면에 그린다."""

    for row in range(BOARD_HEIGHT):
        for column in range(BOARD_WIDTH):
            x = column * BLOCK_SIZE
            y = row * BLOCK_SIZE

            # 빈 칸의 배경을 그린다.
            pygame.draw.rect(
                screen,
                BLACK,
                (x, y, BLOCK_SIZE, BLOCK_SIZE)
            )

            # 고정된 블록이 있다면 블록을 그린다.
            if board[row][column] is not None:
                pygame.draw.rect(
                    screen,
                    board[row][column],
                    (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                )

            # 격자선을 그린다.
            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, BLOCK_SIZE, BLOCK_SIZE),
                1
            )


def draw_block(screen, block):
    """현재 떨어지고 있는 블록을 화면에 그린다."""

    for row_index, row in enumerate(block.shape):
        for column_index, value in enumerate(row):

            if value == 1:
                x = (block.x + column_index) * BLOCK_SIZE
                y = (block.y + row_index) * BLOCK_SIZE

                pygame.draw.rect(
                    screen,
                    block.color,
                    (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                )

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2),
                    1
                )


def draw_next_block(screen, next_block, small_font):
    """다음에 떨어질 블록을 화면 왼쪽 상단에 미리 표시한다."""

    # 미리보기 영역의 위치와 크기
    preview_x = 10
    preview_y = 10
    preview_width = 150
    preview_height = 130

    # 미리보기 영역의 반투명 배경
    preview_surface = pygame.Surface(
        (preview_width, preview_height),
        pygame.SRCALPHA
    )
    preview_surface.fill((0, 0, 0, 180))

    screen.blit(preview_surface, (preview_x, preview_y))

    # 미리보기 영역 테두리
    pygame.draw.rect(
        screen,
        WHITE,
        (preview_x, preview_y, preview_width, preview_height),
        2
    )

    # NEXT 문구 출력
    title = small_font.render("NEXT", True, WHITE)
    screen.blit(title, (preview_x + 50, preview_y + 10))

    # 다음 블록을 미리보기 영역 중앙에 배치한다.
    shape_width = len(next_block.shape[0]) * BLOCK_SIZE
    shape_height = len(next_block.shape) * BLOCK_SIZE

    start_x = preview_x + (preview_width - shape_width) // 2
    start_y = preview_y + 45 + (preview_height - 45 - shape_height) // 2

    # 다음 블록을 그린다.
    for row_index, row in enumerate(next_block.shape):
        for column_index, value in enumerate(row):

            if value == 1:
                x = start_x + column_index * BLOCK_SIZE
                y = start_y + row_index * BLOCK_SIZE

                pygame.draw.rect(
                    screen,
                    next_block.color,
                    (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                )

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2),
                    1
                )


def draw_information(screen, score, font, small_font):
    """점수와 조작 방법을 화면에 출력한다."""

    side_x = BOARD_WIDTH * BLOCK_SIZE

    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (side_x, 0, SIDE_WIDTH, SCREEN_HEIGHT)
    )

    title = font.render("TETRIS", True, WHITE)
    screen.blit(title, (side_x + 45, 30))

    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (side_x + 30, 100))

    controls = [
        "Left/Right: Move",
        "Up: Rotate",
        "Down: Move down",
        "Space: Drop",
        "ESC: Exit"
    ]

    y = 370

    for text in controls:
        control_text = small_font.render(text, True, LIGHT_GRAY)
        screen.blit(control_text, (side_x + 15, y))
        y += 35


def draw_game_over(screen, font, small_font):
    """게임 종료 문구를 화면에 출력한다."""

    overlay = pygame.Surface((BOARD_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))

    game_over_text = font.render("GAME OVER", True, WHITE)
    restart_text = small_font.render("Press R to restart", True, WHITE)

    game_over_rect = game_over_text.get_rect(
        center=(BOARD_WIDTH * BLOCK_SIZE // 2, SCREEN_HEIGHT // 2 - 30)
    )

    restart_rect = restart_text.get_rect(
        center=(BOARD_WIDTH * BLOCK_SIZE // 2, SCREEN_HEIGHT // 2 + 20)
    )

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)


def reset_game():
    """게임 상태를 처음 상태로 초기화한다."""

    board = create_board()
    current_block = Block()
    next_block = Block()
    score = 0
    game_over = False

    return board, current_block, next_block, score, game_over

def draw_score(screen, score, font):
    """획득한 점수를 화면 오른쪽 상단에 표시한다."""

    # 점수 문자열을 만든다.
    score_text = font.render(f"Score: {score}", True, WHITE)

    # 화면 오른쪽 상단에 배치한다.
    score_rect = score_text.get_rect()
    score_rect.topright = (SCREEN_WIDTH - 20, 20)

    # 점수를 화면에 출력한다.
    screen.blit(score_text, score_rect)

def play_background_music():
    """직접 만든 테트리스 배경 음악을 반복 재생한다."""

    try:
        # 현재 파이썬 파일이 위치한 폴더를 기준으로 음악 경로를 만든다.
        current_directory = os.path.dirname(os.path.abspath(__file__))
        music_path = os.path.join(current_directory, "tetris_bgm.wav")

        # 배경 음악 파일을 불러온다.
        pygame.mixer.music.load(music_path)

        # 배경 음악의 음량을 설정한다.
        pygame.mixer.music.set_volume(0.3)

        # -1은 배경 음악을 무한 반복한다는 의미이다.
        pygame.mixer.music.play(-1)

    except pygame.error as error:
        print("배경 음악을 재생할 수 없습니다.")
        print(error)


def main():
    """테트리스 게임의 메인 함수"""

    pygame.init()

    #게임이 진행되는 동안 배경 음악을 반복 재생한다.
    play_background_music()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")

    clock = pygame.time.Clock()


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 40)
    small_font = pygame.font.SysFont(None, 24)

    board, current_block, next_block, score, game_over = reset_game()

    # 블록이 자동으로 떨어지는 간격
    fall_interval = 500
    last_fall_time = pygame.time.get_ticks()

    running = True

    while running:
        clock.tick(FPS)

        current_time = pygame.time.get_ticks()

        # 키보드와 창 종료 이벤트를 처리한다.
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # ESC 키를 누르면 게임을 종료한다.
                if event.key == pygame.K_ESCAPE:
                    running = False

                # 게임 종료 상태에서 R 키를 누르면 다시 시작한다.
                if game_over:
                    if event.key == pygame.K_r:
                        board, current_block, next_block, score, game_over = reset_game()
                        last_fall_time = pygame.time.get_ticks()

                    continue

                # 왼쪽 화살표: 왼쪽으로 이동
                if event.key == pygame.K_LEFT:
                    if is_valid_position(board, current_block, move_x=-1):
                        current_block.x -= 1

                # 오른쪽 화살표: 오른쪽으로 이동
                elif event.key == pygame.K_RIGHT:
                    if is_valid_position(board, current_block, move_x=1):
                        current_block.x += 1

                # 아래 화살표: 한 칸 아래로 이동
                elif event.key == pygame.K_DOWN:
                    if is_valid_position(board, current_block, move_y=1):
                        current_block.y += 1

                # 위 화살표: 시계 방향으로 회전
                elif event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_block.shape)

                    if is_valid_position(
                        board,
                        current_block,
                        new_shape=rotated_shape
                    ):
                        current_block.shape = rotated_shape

                # 스페이스바: 블록을 바닥까지 즉시 떨어뜨린다.
                elif event.key == pygame.K_SPACE:
                    while is_valid_position(
                        board,
                        current_block,
                        move_y=1
                    ):
                        current_block.y += 1

                    # 즉시 고정되도록 자동 낙하 시간을 조정한다.
                    last_fall_time = 0

        # 일정 시간이 지나면 블록을 자동으로 아래로 이동한다.
        if not game_over and current_time - last_fall_time >= fall_interval:

            if is_valid_position(board, current_block, move_y=1):
                current_block.y += 1

            else:
                # 더 이상 내려갈 수 없으면 블록을 고정한다.
                place_block(board, current_block)

                # 완성된 줄을 삭제하고 점수를 증가시킨다.
                cleared_lines = clear_full_lines(board)
                score += calculate_score(cleared_lines)

                # 다음 블록을 현재 블록으로 변경한다.
                current_block = next_block
                next_block = Block()

                # 새 블록을 배치할 공간이 없으면 게임 종료
                if not is_valid_position(board, current_block):
                    game_over = True

            last_fall_time = current_time

        # 화면을 검은색으로 초기화한다.
        screen.fill(BLACK)

        # 게임 화면을 그린다.
        draw_board(screen, board)

        if not game_over:
            draw_block(screen, current_block)

        # 다음 블록 미리보기
        draw_next_block(screen, next_block, small_font)

        # 화면 오른쪽 상단에 점수 표시
        draw_score(screen, score, font)

        # 게임 오버 화면을 출력한다.
        if game_over:
            draw_game_over(screen, font, small_font)

        pygame.display.flip()

    # 배경 음악을 정지한다.
    pygame.mixer.music.stop()


    pygame.quit()
    sys.exit()


# 프로그램의 시작점
if __name__ == "__main__":
    main()