import random
import customtkinter as ctk,customtkinter

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  

class Hangman(ctk.CTk):
    hangman_stages = [
        """
           ------
           |    |
           |
           |
           |
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------            
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------            
        """
    ]
    word_list = ['words']
        

    def __init__(self):    
        super().__init__()
        self.title('Hangman')
        self.center_window(600,580)
        self.iconbitmap('Icon Path') 
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Hangman", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Use random word", command=self.new_game)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Use own word", command=self.input_custom_word)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "115%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.scaling_optionemenu.set("100%")

        self.main_Frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_Frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.main_Frame.grid_columnconfigure(0, weight=1)
        self.main_Frame.grid_rowconfigure(6, weight=1)

        self.word_label = ctk.CTkLabel(self.main_Frame, text='Wort:')
        self.word_label.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.guess_input = ctk.CTkEntry(self.main_Frame)
        self.guess_input.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.guess_input.bind('<Return>', lambda event: self.make_guess())

        self.guess_button = ctk.CTkButton(self.main_Frame, text='Guess', command=self.make_guess)
        self.guess_button.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.tried_letters_label = ctk.CTkLabel(self.main_Frame, text='Already tried characters: ')
        self.tried_letters_label.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.hangman_image_label = ctk.CTkLabel(self.main_Frame, text='', font=('Courier', 12), justify='left')
        self.hangman_image_label.grid(row=4, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.attempts_label = ctk.CTkLabel(self.main_Frame, text='Remaining tries: 6')
        self.attempts_label.grid(row=5, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.message_label = ctk.CTkLabel(self.main_Frame, text='')
        self.message_label.grid(row=6, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.new_game()


    def change_appearance_mode_event(self, new_appearance_mode: str):       
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):               
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def center_window(self, width, height):             
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{x}+{y}')

    def new_game(self, custom_word=None):       
        self.guess_input.delete(0, 'end')
        if custom_word:
            self.word = custom_word.lower()
        else:
            self.word = random.choice(self.word_list)
        
        self.word_display = ['_'] * len(self.word)
        self.attempts = 6
        self.guessed_letters = set()
        
        self.update_display()
        self.update_hangman_image()
    
    def input_custom_word(self):        
        input_window = ctk.CTk()
        input_window.title('Choose own word')
        input_window.geometry('300x200')
        input_window.iconbitmap('Icon Path')

        input_window_width = 300
        input_window_height = 150
        screen_width = input_window.winfo_screenwidth()
        screen_height = input_window.winfo_screenheight()
        x = (screen_width // 2) - (input_window_width // 2)
        y = (screen_height // 2) - (input_window_height // 2)
        input_window.geometry(f'{input_window_width}x{input_window_height}+{x}+{y}')

        input_frame = ctk.CTkFrame(input_window)
        input_frame.pack(padx=20, pady=20)

        input_label = ctk.CTkLabel(input_frame, text='Type in word:')
        input_label.pack(pady=5)

        input_entry = ctk.CTkEntry(input_frame, placeholder_text="Your word", show="*")
        input_entry.pack(pady=5)
        input_entry.bind('<Return>', lambda event: submit_custom_word())

        def submit_custom_word():
            custom_word = input_entry.get().strip()
            if custom_word and not custom_word.isalpha():
                Error = ctk.CTk()
                Error.title('Error')
                Error.geometry('300x150')
                Error.iconbitmap('Icon Path')
                Error_width = 300
                Error_height = 150
                screen_width = Error.winfo_screenwidth()
                screen_height = Error.winfo_screenheight()
                x = (screen_width // 2) - (Error_width // 2)
                y = (screen_height // 2) - (Error_height // 2)
                Error.geometry(f'{Error_width}x{Error_height}+{x}+{y}')
                end_Frame= ctk.CTkFrame(Error)
                end_Frame.pack(padx=10, pady=10)
                end_label = ctk.CTkLabel(Error, text="\n Please only type in characters!")
                end_label.pack(side='top', pady=5)
                def play_again():
                    Error.destroy()
                    input_entry.delete(0, 'end')
                    input_window.focus_force()

                play_again_button = ctk.CTkButton(end_Frame, text='Okay', command=play_again)
                play_again_button.pack(side='bottom', padx=15, pady=15, )
                Error.mainloop()
            else:
                self.new_game(custom_word)
                input_window.destroy()

        submit_button = ctk.CTkButton(input_frame, text='Confirm', command=submit_custom_word)
        submit_button.pack(pady=5)
        input_window.mainloop()
    
    def update_display(self):           
        display_word = ' '.join(self.word_display)
        self.word_label.configure(text='Wort: ' + display_word)
        self.tried_letters_label.configure(text='Already tried characterts: ' + ', '.join(sorted(self.guessed_letters)))
        self.attempts_label.configure(text=f'Remaining tries: {self.attempts}')

    def update_hangman_image(self):         
        stage_index = 6 - self.attempts
        
        if stage_index >= 0 and stage_index < len(self.hangman_stages):
            self.hangman_image_label.configure(text=self.hangman_stages[stage_index])
        else:
            self.hangman_image_label.configure(text='')

    def make_guess(self):               
        self.message_label.configure(text='')
        guess = self.guess_input.get().strip().lower()
        
        if len(guess) != 1 or not guess.isalpha():
            self.message_label.configure(text='Type in a character!')
            self.guess_input.delete(0, 'end')
            return
        
        if guess in self.guessed_letters:
            self.message_label.configure(text='You already tried this character!')
            self.guess_input.delete(0, 'end')
            return

        self.guessed_letters.add(guess)
        
        if guess in self.word:
            for index, letter in enumerate(self.word):
                if letter == guess:
                    self.word_display[index] = guess
            self.word_display[0] = self.word_display[0].upper()
            self.update_display()
            if '_' not in self.word_display:
                self.show_end_game_message(f'You won! The word was: {self.word[0].upper()+self.word[1:len(self.word)]}')
        else:
            self.attempts -= 1
            self.update_display()
            self.update_hangman_image()
            if self.attempts == 0:
                self.show_end_game_message(f'You loose! The word was: {self.word[0].upper()+self.word[1:len(self.word)]}')
        self.guess_input.delete(0, 'end')

    def show_end_game_message(self, message):       
        end_window = ctk.CTk()
        end_window.title('End')
        end_window.geometry('300x150')
        end_window.iconbitmap('Icon Path')
        end_window_width = 300
        end_window_height = 150
        screen_width = end_window.winfo_screenwidth()
        screen_height = end_window.winfo_screenheight()
        x = (screen_width // 2) - (end_window_width // 2)
        y = (screen_height // 2) - (end_window_height // 2)
        end_window.geometry(f'{end_window_width}x{end_window_height}+{x}+{y}')
        end_Frame= ctk.CTkFrame(end_window)
        end_Frame.pack(padx=10, pady=10)
        end_label = ctk.CTkLabel(end_window, text=message+"\n Dou want to play another round?")
        end_label.pack(side='top', pady=5)

        def play_again():
            self.new_game()
            end_window.destroy()

        def quit_game():
            self.destroy()
            end_window.destroy()

        play_again_button = ctk.CTkButton(end_Frame, text='Yes', command=play_again)
        play_again_button.pack(side='left', padx=5, pady=5, )

        quit_button = ctk.CTkButton(end_Frame, text='No', command=quit_game)
        quit_button.pack(side='right', padx=5, pady=5,)

        end_window.mainloop()

     
if __name__ == '__main__':
    app = Hangman()
    app.mainloop()
