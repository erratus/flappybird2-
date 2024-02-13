import tkinter as tk
from main import main as run_game

class FlappyBirdApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flappy Bird")
        self.master.geometry("400x600")

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        self.start_button.pack_forget()  # Remove the start button from the window
        self.play_again_button = tk.Button(self.master, text="Play Again", command=self.play_again)
        self.exit_button = tk.Button(self.master, text="Exit Game", command=self.exit_game)
        run_game()  # Run the Flappy Bird game

    def play_again(self):
        self.play_again_button.pack_forget()
        self.exit_button.pack_forget()
        run_game()  # Run the Flappy Bird game

    def exit_game(self):
        self.master.destroy()  # Close the Tkinter window

def main():
    root = tk.Tk()
    app = FlappyBirdApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
