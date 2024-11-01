import tkinter as tk
from tkinter import messagebox, simpledialog
from ttkbootstrap import Style
import ttkbootstrap as ttk
from datetime import datetime
import sqlite3
import openai
import requests
import random



# Cheile API (înlocuiește cu cheile tale reale)
openai.api_key = "CHEIA TA OPENAI"
CHEIE_API_METEO = "CHEIA TA METEO"
URL_METEO = "https://api.openweathermap.org/data/2.5/weather"

# Configurarea bazei de date
conn = sqlite3.connect("gradina.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS plante (
    id INTEGER PRIMARY KEY,
    nume TEXT,
    specie TEXT,
    locatie TEXT,
    data_plantare TEXT,
    instructiuni_ingrijire TEXT,
    program_udare TEXT,
    program_fertilizare TEXT,
    observatii TEXT,
    inregistrari_crestere TEXT
)
''')
conn.commit()

# Listă de curiozități, se pot adăuga in continuare
curiozitati = [
"Bananele sunt tehnic boabe, dar căpșunile nu sunt.",

"Roșiile au fost cândva temute în Europa și erau numite „mere otrăvitoare”.",

"Merele plutesc în apă deoarece sunt compuse din 25% aer.",

"Arahidele nu sunt nuci; sunt legume, asemenea fasolei.",

"Morcovii erau inițial violet, și nu portocalii.",

"Broccoli este o plantă creată de om și nu există în sălbăticie.",

"O singură rodie poate conține peste 1.000 de semințe!",

"Lămâile conțin mai mult zahăr decât căpșunile.",

"Cartofii au fost prima legumă crescută în spațiu.",

"Florile-soarelui pot conține până la 2.000 de semințe.",

"O orhidee poate trăi mai mult de 100 de ani în condiții ideale.",

"Bambusul poate crește până la 91 cm într-o singură zi, fiind cea mai rapidă plantă de pe Pământ.",

"Pepenii verzi conțin peste 90% apă, fiind o sursă excelentă de hidratare.",

"Arborele de cauciuc „Hevea brasiliensis” este sursa principală de latex natural.",

"Cafeaua este realizată din semințele unei bace – bobul de cafea.",

"Arborele de sequoia este unul dintre cei mai înalți arbori din lume, ajungând la 115 metri.",

"O singură plantă de orez poate produce până la 100.000 de boabe de orez.",

"Floarea cadavrului (Amorphophallus titanum) este una dintre cele mai mari și mai urât mirositoare flori din lume.",

"O nucă de cocos este un fruct, o sămânță și o nucă, toate în același timp.",

"Vanilia provine dintr-un tip de orhidee și este unul dintre cele mai scumpe condimente din lume.",

"Smochinele nu sunt polenizate de albine, ci de viespi mici, care pătrund în interiorul fructului.",

"Fructele de avocado nu se coc pe copac, ci încep să se coacă abia după ce sunt culese.",

"În Japonia, există pepeni în formă de cub, crescuți în containere speciale pentru a ocupa mai puțin spațiu.",

"Planta de aloe vera poate supraviețui fără apă săptămâni întregi datorită capacității sale de a stoca apă în frunze.",

"Plantele carnivore, cum ar fi capcana pentru muște Venus, trăiesc în soluri sărace în nutrienți și își prind prada pentru a obține minerale suplimentare.",

"Lemnul de balsa este unul dintre cele mai ușoare materiale naturale, fiind folosit frecvent în construcția modelelor de avioane.",

"Cactusul Saguaro poate stoca până la 200 de litri de apă în timpul ploilor.",

"Arborele de cacao produce aproximativ 2.500 de semințe de cacao în fiecare an.",

"Bambusul produce mai mult oxigen decât orice altă plantă de pe planetă.",

"Arborele de măslin poate trăi peste 1.500 de ani, iar unii măslini din Mediterană au această vârstă.",

"Ciupercile sunt mai apropiate genetic de animale decât de plante.",

"Majoritatea plantelor eliberează oxigen în timpul zilei și absorb dioxid de carbon, dar cactușii fac asta noaptea pentru a economisi apă.",

"Există o specie de palmier, Corypha umbraculifera, care înflorește o singură dată după aproximativ 80 de ani și apoi moare.",

"Arborele de Baobab poate stoca până la 120.000 de litri de apă în trunchiul său pentru a supraviețui secetelor.",

"Arborii de cafea pot trăi între 60 și 70 de ani și necesită aproximativ 2-3 ani pentru a începe să producă boabe.",

"Ghimbirul nu este o rădăcină, ci o tulpină subterană, numită rizom.",

"Portocalele nu sunt întotdeauna portocalii – în regiunile tropicale, rămân verzi chiar și când sunt coapte.",

"Avocado este considerat unul dintre cele mai nutritive fructe, conținând peste 20 de vitamine și minerale.",

"Trifoiul cu patru foi este considerat a aduce noroc deoarece este rar – apare o dată la aproximativ 5.000 de trifoi cu trei foi.",

"Floarea de lotus este cunoscută pentru capacitatea sa de a rămâne curată în apă tulbure, datorită frunzelor sale hidrofobe.",

"Avocado este toxic pentru multe animale: Spre deosebire de oameni, avocado este periculos pentru animalele de companie, cum ar fi câinii și pisicile, din cauza substanței numite persin."
]

class AplicatieGradina:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicație Avansată pentru Grădinărit")
        self.root.configure(bg="#f0f8ff")  # Culoare de fundal personalizată
        self.setup_ui()
        self.incarca_plante()

    def setup_ui(self):
        # Fonturi și stil
        font_poppins = ("Poppins", 10)
        self.root.option_add("*Font", font_poppins)

        # Creare Tab-uri
        caiet = ttk.Notebook(self.root)
        caiet.pack(expand=True, fill='both')

        # Tab-uri
        self.cadru_principal = ttk.Frame(caiet)
        self.cadru_meteo = ttk.Frame(caiet)
        self.cadru_crestere = ttk.Frame(caiet)
        self.cadru_chat = ttk.Frame(caiet)
        self.cadru_curiozitati = ttk.Frame(caiet)
        
        caiet.add(self.cadru_principal, text="Gestionare Plante")
        caiet.add(self.cadru_meteo, text="Vremea")
        caiet.add(self.cadru_crestere, text="Monitorizare Creștere")
        caiet.add(self.cadru_chat, text="Sfaturi pentru Grădinărit")
        caiet.add(self.cadru_curiozitati, text="Curiozități")

        # Elemente cadru principal (Gestionare Plante)
        self.setup_cadru_principal()
        # Elemente cadru meteo
        self.setup_cadru_meteo()
        # Elemente cadru monitorizare creștere
        self.setup_cadru_crestere()
        # Elemente cadru chat
        self.setup_cadru_chat()
        # Elemente cadru curiozități
        self.setup_cadru_curiozitati()

    def setup_cadru_principal(self):
        # Introducere detalii plante
        ttk.Label(self.cadru_principal, text="Nume Plantă:", bootstyle="info").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nume = ttk.Entry(self.cadru_principal, width=30)
        self.entry_nume.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(self.cadru_principal, text="Specie:", bootstyle="info").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_specie = ttk.Entry(self.cadru_principal, width=30)
        self.entry_specie.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.cadru_principal, text="Locație:", bootstyle="info").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_locatie = ttk.Entry(self.cadru_principal, width=30)
        self.entry_locatie.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.cadru_principal, text="Program Udare:", bootstyle="info").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_program_udare = ttk.Entry(self.cadru_principal, width=30)
        self.entry_program_udare.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.cadru_principal, text="Program Fertilizare:", bootstyle="info").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_program_fertilizare = ttk.Entry(self.cadru_principal, width=30)
        self.entry_program_fertilizare.grid(row=4, column=1, padx=10, pady=5)

        buton_adauga = ttk.Button(self.cadru_principal, text="Adaugă Plantă", command=self.adauga_planta, bootstyle="success")
        buton_adauga.grid(row=5, column=0, columnspan=2, pady=10)

        # Afișare listă plante
        self.lista_plante = tk.Listbox(self.cadru_principal, width=50, height=15)
        self.lista_plante.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.lista_plante.bind("<<ListboxSelect>>", self.afiseaza_detalii_planta)

    def setup_cadru_meteo(self):
        # Afișarea vremii pe baza locației plantei
        self.afisare_meteo = tk.Text(self.cadru_meteo, width=60, height=20)
        self.afisare_meteo.pack(pady=10)

    def setup_cadru_crestere(self):
        # Zonă de desen pentru monitorizarea creșterii
        self.canvas_crestere = tk.Canvas(self.cadru_crestere, width=500, height=400)
        self.canvas_crestere.pack()

    def setup_cadru_chat(self):
        # Casetă de chat pentru a solicita sfaturi de grădinărit
        self.entry_chat = tk.Entry(self.cadru_chat, width=50)
        self.entry_chat.pack(pady=5)
        self.buton_chat = ttk.Button(self.cadru_chat, text="Solicită Sfaturi", command=self.cere_openai, bootstyle="primary")
        self.buton_chat.pack(pady=5)

        # Afișare răspunsuri OpenAI
        self.afisare_chat = tk.Text(self.cadru_chat, width=60, height=20)
        self.afisare_chat.pack(pady=10)

    def setup_cadru_curiozitati(self):
        # Afișare curiozități
        self.eticheta_curiozitate = ttk.Label(self.cadru_curiozitati, text="Știați că?", bootstyle="info")
        self.eticheta_curiozitate.pack(pady=10)

        self.text_curiozitate = tk.Text(self.cadru_curiozitati, width=60, height=10)
        self.text_curiozitate.pack(pady=5)
        self.afiseaza_curiozitate()

        # Buton pentru a afișa o nouă curiozitate
        self.buton_curiozitate = ttk.Button(self.cadru_curiozitati, text="Afișează o altă Curiozitate", command=self.afiseaza_curiozitate, bootstyle="primary")
        self.buton_curiozitate.pack(pady=5)

    def afiseaza_curiozitate(self):
        self.text_curiozitate.delete(1.0, tk.END)
        curiozitate = random.choice(curiozitati)
        self.text_curiozitate.insert(tk.END, curiozitate)

    def incarca_plante(self):
        cursor.execute("SELECT nume FROM plante")
        plante = cursor.fetchall()
        self.lista_plante.delete(0, tk.END)
        for planta in plante:
            self.lista_plante.insert(tk.END, planta[0])

    def adauga_planta(self):
        nume = self.entry_nume.get()
        specie = self.entry_specie.get()
        locatie = self.entry_locatie.get()
        data_plantare = datetime.now().strftime("%Y-%m-%d")
        program_udare = self.entry_program_udare.get()
        program_fertilizare = self.entry_program_fertilizare.get()

        if not (nume and specie and locatie and program_udare and program_fertilizare):
            messagebox.showwarning("Avertisment", "Toate câmpurile trebuie completate!")
            return

        cursor.execute('''
            INSERT INTO plante (nume, specie, locatie, data_plantare, program_udare, program_fertilizare)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nume, specie, locatie, data_plantare, program_udare, program_fertilizare))
        conn.commit()

        self.incarca_plante()
        messagebox.showinfo("Succes", f"{nume} a fost adăugată în grădină.")

    def afiseaza_detalii_planta(self, event):
        index_selectat = self.lista_plante.curselection()
        if not index_selectat:
            return

        nume_planta = self.lista_plante.get(index_selectat[0])
        cursor.execute("SELECT * FROM plante WHERE nume=?", (nume_planta,))
        date_planta = cursor.fetchone()

        detalii = (f"Nume: {date_planta[1]}\nSpecie: {date_planta[2]}\nLocație: {date_planta[3]}\n"
                   f"Data Plantare: {date_planta[4]}\nProgram Udare: {date_planta[6]}\nProgram Fertilizare: {date_planta[7]}")
        messagebox.showinfo("Detalii Plantă", detalii)

    def cere_openai(self):
        intrebare = self.entry_chat.get()
        raspuns = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Oferă sfaturi de grădinărit pentru: {intrebare}",
            max_tokens=100
        )
        raspuns_text = raspuns.choices[0].text.strip()
        self.afisare_chat.insert(tk.END, f"Î: {intrebare}\nR: {raspuns_text}\n\n")
        self.entry_chat.delete(0, tk.END)

# Bucla principală a aplicației Tkinter
root = ttk.Window(themename="morph")  # Inițializare fereastră ttkbootstrap pentru stil personalizat
app = AplicatieGradina(root)
root.mainloop()
