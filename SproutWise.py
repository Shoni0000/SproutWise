import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

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

        self.curiosities_text = tk.Text(content_frame, wrap="word", bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.curiosities_text.grid(row=1, column=0, pady=5, sticky="nsew")
        self.curiosities_text.insert(tk.END, "\n".join(curiozitati))
        self.curiosities_text.config(state=tk.DISABLED)

        # Random Button for Curiosities
        random_button = tk.Button(content_frame, text="Random Curiosity", command=self.show_random_curiosity, font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff")
        random_button.grid(row=2, column=0, pady=5)

        # Configure grid to make the text widget expand
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Buttons Section
        buttons_frame = tk.Frame(content_frame, bg="#f0f8ff")
        buttons_frame.grid(row=3, column=0, pady=10)

        add_button = tk.Button(buttons_frame, text="Add Plant", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.add_plant)
        add_button.grid(row=0, column=0, padx=5)

        view_button = tk.Button(buttons_frame, text="View Plants", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.view_plants)
        view_button.grid(row=0, column=1, padx=5)

        delete_button = tk.Button(buttons_frame, text="Delete All", font=("Helvetica", 12), bg="#ff4d4d", fg="#ffffff", command=self.delete_all_plants)
        delete_button.grid(row=0, column=2, padx=5)

        exit_button = tk.Button(buttons_frame, text="Exit", font=("Helvetica", 12), bg="#2e8b57", fg="#ffffff", command=self.root.quit)
        exit_button.grid(row=0, column=3, padx=5)

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

        # Scrollbar for viewing plants
        view_frame = tk.Frame(view_window)
        view_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(view_frame)
        scrollbar = ttk.Scrollbar(view_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Retrieve plant list from the database
        self.cursor.execute('SELECT id, name, type FROM plants')
        plants = self.cursor.fetchall()

        for plant in plants:
            plant_label = tk.Label(scrollable_frame, text=f"Name: {plant[1]}, Type: {plant[2]}")
            plant_label.pack(pady=5)
            
            # Add right-click delete option for each plant
            plant_label.bind("<Button-3>", lambda e, plant_id=plant[0]: self.delete_plant(plant_id, plant_label))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def delete_plant(self, plant_id, plant_label):
        # Function to delete a specific plant
        if messagebox.askyesno("Delete Plant", "Are you sure you want to delete this plant?"):
            self.cursor.execute('DELETE FROM plants WHERE id = ?', (plant_id,))
            self.conn.commit()
            plant_label.destroy()  # Remove the label from the view
            messagebox.showinfo("Deleted", "The plant has been deleted.")

    def delete_all_plants(self):
        # Confirm delete action
        if messagebox.askyesno("Delete All", "Are you sure you want to delete all plant records?"):
            self.cursor.execute('DELETE FROM plants')
            self.conn.commit()
            messagebox.showinfo("Deleted", "All plant records have been deleted.")

    def show_random_curiosity(self):
        # Display a random curiosity
        random_fact = random.choice(curiozitati)
        self.curiosities_text.config(state=tk.NORMAL)
        self.curiosities_text.delete(1.0, tk.END)
        self.curiosities_text.insert(tk.END, random_fact)
        self.curiosities_text.config(state=tk.DISABLED)

    def incarca_plante(self):
        # Function to load plants (if needed for other functionalities)
        pass

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicatieGradina(root)
    root.mainloop()
