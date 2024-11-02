import tkinter as tk
from tkinter import ttk
import sqlite3

# Listă de curiozități, se pot adăuga in continuare
curiozitati = [
    "Bananele sunt tehnic boabe, dar căpșunile nu sunt.",
    "Roșiile au fost cândva temute în Europa și erau numite „mere otrăvitoare”.",
    "Merele plutesc în apă deoarece sunt compuse din 25% aer.",
    # Add more curiosities as needed...
]

class AplicatieGradina:
    def __init__(self, root):
        self.root = root
        self.root.title("SproutWise")
        self.root.configure(bg="#f0f8ff")  # Culoare de fundal personalizată
        self.setup_ui()
        self.setup_database()
        self.incarca_plante()

    def setup_ui(self):
        # Fonturi și stil
        font_poppins = ("Poppins", 10)
        self.root.option_add("*Font", font_poppins)

        # Title Label
        title_label = tk.Label(self.root, text="SproutWise - Garden Management", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#2e8b57")
        title_label.pack(pady=10)

        # Frame for content
        content_frame = tk.Frame(self.root, bg="#f0f8ff")
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Curiosities Section
        curiosities_label = tk.Label(content_frame, text="Curiosities", font=("Helvetica", 14, "bold"), bg="#f0f8ff", fg="#2e8b57")
        curiosities_label.grid(row=0, column=0, sticky="w", pady=5)

        curiosities_text = tk.Text(content_frame, wrap="word", bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        curiosities_text.grid(row=1, column=0, pady=5, sticky="nsew")
        curiosities_text.insert(tk.END, "\n".join(curiozitati))
        curiosities_text.config(state=tk.DISABLED)

        # Configure grid to make the text widget expand
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Buttons Section
        buttons_frame = tk.Frame(content_frame, bg="#f0f8ff")
        buttons_frame.grid(row=2, column=0, pady=10)

        add_button = tk.Button(buttons_frame, text="Add Plant", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.add_plant)
        add_button.grid(row=0, column=0, padx=5)

        view_button = tk.Button(buttons_frame, text="View Plants", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.view_plants)
        view_button.grid(row=0, column=1, padx=5)

        exit_button = tk.Button(buttons_frame, text="Exit", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.root.quit)
        exit_button.grid(row=0, column=2, padx=5)

    def setup_database(self):
        # Setup the database
        self.conn = sqlite3.connect('plants.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_plant(self):
        # Function to add a plant
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Plant")
        add_window.geometry("300x200")
        
        tk.Label(add_window, text="Plant Name:").pack(pady=5)
        plant_name_entry = tk.Entry(add_window)
        plant_name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Plant Type:").pack(pady=5)
        plant_type_entry = tk.Entry(add_window)
        plant_type_entry.pack(pady=5)
        
        tk.Button(add_window, text="Add", command=lambda: self.save_plant(plant_name_entry.get(), plant_type_entry.get())).pack(pady=20)

    def save_plant(self, name, plant_type):
        # Save the plant details to the database
        self.cursor.execute('INSERT INTO plants (name, type) VALUES (?, ?)', (name, plant_type))
        self.conn.commit()
        print(f"Plant added: {name}, Type: {plant_type}")

    def view_plants(self):
        # Function to view plants
        view_window = tk.Toplevel(self.root)
        view_window.title("View Plants")
        view_window.geometry("400x300")
        
        # Retrieve plant list from the database
        self.cursor.execute('SELECT name, type FROM plants')
        plants = self.cursor.fetchall()
        
        for plant in plants:
            tk.Label(view_window, text=f"Name: {plant[0]}, Type: {plant[1]}").pack(pady=5)

    def incarca_plante(self):
        # Function to load plants
        pass

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieGradina(root)
    root.mainloop()
