import pygame
import socket

pygame.init()

win = pygame.display.set_mode((200, 200))
pygame.display.set_caption("First Game")

posx = 50
posy = 50
width = 40
height = 40
vel = 5

run = True

host = "127.0.0.1"
port = 12345

name = "noname"
user_id = 0
is_live = 1
cli_datas = []


def send_pos():
    global name, posx, posy, user_id, cli_datas
    s = socket.socket()
    try:
        s.connect((host, port))

        send_text = (
            name
            + ":"
            + str(posx)
            + ":"
            + str(posy)
            + ":"
            + str(is_live)
            + ":"
            + str(user_id)
        )

        s.sendall(send_text.encode("utf-8"))

        yanit = s.recv(1024).decode("utf-8")

        if user_id == 0:
            spl = yanit.split(":")
            user_id = int(spl[-1])
            print(str(user_id))
        else:
            cli_datas = yanit.split(";")
        print(yanit)
        s.close()
    except socket.error as msg:
        print("[Server aktif değil.] Mesaj:", msg)


send_pos()

while run:
    pygame.time.delay(100)
    send_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        posx -= vel

    if keys[pygame.K_RIGHT]:
        posx += vel

    if keys[pygame.K_UP]:
        posy -= vel

    if keys[pygame.K_DOWN]:
        posy += vel

    win.fill((255, 255, 255))  # Fills the screen with black
    if is_live == 1:
        pygame.draw.rect(win, (255, 239, 3), (posx, posy, width, height))
    else:
        break

    if cli_datas != []:
        print(str(cli_datas))
        for i in cli_datas:
            if i != "0":
                spl = i.split(":")
                if int(spl[-1]) != user_id:
                    if int(spl[-2]) != 0:
                        pygame.draw.rect(
                            win, (255, 0, 0), (int(spl[1]), int(spl[2]), width, height)
                        )

    pygame.display.update()

pygame.quit()
