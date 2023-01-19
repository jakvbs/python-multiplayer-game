import pygame as pg

from canvas import Canvas
from constants import WIDTH, HEIGHT
from game import Game
from network import Network

canvas = Canvas(WIDTH, HEIGHT, "Client")


def redraw_window(canvas: Canvas, game: Game, player: int) -> None:
    canvas.draw_background()

    if not game.connected():
        canvas.draw_text("Waiting for player...", 40,
                         WIDTH // 2 - 150, HEIGHT // 2 - 50)
    else:
        for row in game.circles:
            for circle in row:
                circle.draw(canvas.screen)
        for line in game.lines:
            line.draw(canvas.screen)

        your_score = game.p1_score if player == 1 else game.p2_score
        opp_score = game.p2_score if player == 1 else game.p1_score
        canvas.draw_text(f"Your Score: {your_score}", 40, 100, 715)
        canvas.draw_text(
            f"Opponent's Score: {opp_score}", 40, 330, 715)

        if game.winner_or_draw:
            if game.winner_or_draw == player:
                canvas.draw_text("You Won!", 40, WIDTH // 2 - 150, 755)
            elif game.winner_or_draw == "DRAW":
                canvas.draw_text("Tie Game!", 40, WIDTH // 2 - 150, 755)
            else:
                canvas.draw_text("You Lost!", 40, WIDTH // 2 - 150, 755)

        if game.current_player != player and not game.winner_or_draw:
            canvas.draw_text("Opponent's Turn", 40, WIDTH // 2 - 150, 755)

    canvas.update()


def game_loop() -> None:
    run = True
    clock = pg.time.Clock()
    net = Network()
    player = net.get_player()
    print(f"You are player: {player}")

    while run:
        clock.tick(60)
        try:
            game: Game = net.send("get")
        except:
            print("Couldn't get game")
            break

        if game.winner_or_draw:
            redraw_window(canvas, game, player)
            pg.time.delay(500)
            try:
                game = net.send("reset")
            except:
                print("Couldn't get game")
                break

            pg.time.delay(5000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.MOUSEBUTTONDOWN and game.current_player == player:
                x, y = event.pos[0], event.pos[1]
                if game.check_valid_move(x, y) and game.connected():
                    net.send(f"{x},{y}")

        redraw_window(canvas, game, player)


def menu_screen() -> None:
    run = True
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        canvas.draw_background()
        canvas.draw_text("Click to Play!", 60, WIDTH //
                         2 - 150, HEIGHT // 2 - 50)
        canvas.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                run = False

    game_loop()


def main() -> None:
    while True:
        menu_screen()


if __name__ == "__main__":
    main()
