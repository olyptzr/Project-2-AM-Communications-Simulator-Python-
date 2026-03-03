import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Βάζω και αυτό ώστε αν βάλει ο χρήστης λάθος τιμές, να εμφανίσει μήνυμα σφάλματος σε παράθυρο και όχι μόνο στο console

# --- Δημιουργία συνάρτησης generate_and_plot ---
# Αρχικά δημιουργώ συνάρτηση που θα πραγματοποιεί τα plots όταν πατάω το κουμπί Generate&plot του παραθύρου
def generate_and_plot():
    try:    # χρησιμοποιώ try-except για έλεγχο των τιμών που δίνει ο χρήστης (να είναι αριθμοί και όχι σύμβολα ή strings)
        # 1. Λήψη τιμών από τα entries
        Am = float(entry_am.get())
        fm = float(entry_fm.get())
        Ac = float(entry_ac.get())
        fc = float(entry_fc.get())

        # Έλεγχος για Ac = 0
        if Ac == 0:
            messagebox.showerror("Σφάλμα", "Το πλάτος του φέροντος (Ac) δεν μπορεί να είναι 0.", parent=root)
            return

        # Έλεγχος για αρνητικές τιμές
        if Am<0 or fm<0 or Ac<0 or fc<0:
            messagebox.showerror("Σφάλμα Τιμών", "Οι τιμές για Πλάτος και Συχνότητα πρέπει να είναι θετικοί αριθμοί.", parent=root)
            return

        # Προαιρετικός έλεγχος: Πρέπει fc>>fm
        if fc<=fm:
            messagebox.showwarning("Προειδοποίηση!",
                                   "Για σωστή διαμόρφωση ΑΜ, η συχνότητα του φέροντος (fc) πρέπει να είναι αρκετά μεγαλύτερη από τη συχνότητα του σήματος (fm).", parent=root)
            # Δεν κάνω return, απλά προειδοποιώ και συνεχίζω

        # 2. Δημιουργία άξονα χρόνου t (από 0 έως 0.02 sec)
        t_limit = 0.02
        total_points = int(max(1000, fc * t_limit * 100))       # Προσαρμογή δειγματοληψίας (100 σημεία ανά περίοδο) για λεία απεικόνιση για οποιοδήποτε time_limit και fc,
                                                                # με ελάχιστο όριο (1000) για λεία απεικόνιση στις χαμηλές συχνότητες

        t = np.linspace(0, t_limit, total_points)

        # 3. Υπολογισμός σημάτων
        # Σήμα πληροφορίας (Message Signal)
        # m(t) = Am * cos(2*pi*fm*t)
        message_signal = Am * np.cos(2*np.pi*fm*t)

        # Φέρον σήμα (Carrier Signal)
        # c(t) = Ac * cos(2*pi*fc*t)
        carrier_signal = Ac * np.cos(2*np.pi*fc*t)

        # Δείκτης διαμόρφωσης
        m = Am / Ac

        # Σήμα AM
        # s(t) = Ac * (1 + m * cos(2*pi*fm*t)) * cos(2*pi*fc*t)
        am_signal = Ac * (1 + m * np.cos(2*np.pi*fm*t)) * np.cos(2*np.pi*fc*t)

        # Αποδιαμορφωμένο σήμα (Περιβάλλουσα)
        # E(t) = Ac * |1 + μ * cos(2π*fm*t)|
        demodulated_signal = Ac * np.abs(1 + m * np.cos(2*np.pi*fm*t))

        # 4. Σχεδίαση των διαγραμμάτων
        # Καθαρισμός προηγούμενων γραφημάτων για να μην υπάρχει graph overlap
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        # Plot 1: Message Signal
        ax1.plot(t, message_signal, color='blue')
        ax1.set_title('Message Signal', fontsize=10)
        ax1.grid(True)
        ax1.set_ylabel('Amplitude')     # Βάζω ονόματα στους άξονες, αν και στην εκφώνηση παραλείπονταν
        ax1.set_xlim(0, t_limit)       # Γιατί θέλω να τα γραφήματα να ξεκινούν ακριβώς από την αρχή του άξονα (0) και τελειώνουν ακριβώς στο τέλος (0.2)
        ax1.set_ylim(-np.ceil(Am), np.ceil(Am))         # Κάνω scaling για να έχω ακέραια τα όρια του άξονα Υ


        # Plot 2: Carrier Signal
        ax2.plot(t, carrier_signal, color='purple')
        ax2.set_title('Carrier Signal', fontsize=10)
        ax2.grid(True)
        ax2.set_ylabel('Amplitude')
        ax2.set_xlim(0, t_limit)
        ax2.set_ylim(-np.ceil(Ac), np.ceil(Ac))

        # Plot 3: AM Signal
        ax3.plot(t, am_signal, color='red')
        ax3.set_title('AM Signal', fontsize=10)
        ax3.grid(True)
        ax3.set_ylabel('Amplitude')
        ax3.set_xlim(0, t_limit)
        ax3.set_ylim(-np.ceil(Ac + Am), np.ceil(Ac + Am))

        # Plot 4: Demodulated Signal (Envelope)
        ax4.plot(t, demodulated_signal, color='green')
        ax4.set_title('Demodulated Signal (Envelope)', fontsize=10)
        ax4.grid(True)
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Amplitude')
        ax4.set_xlim(0, t_limit)       # Αφήνω autoscaling για τα όρια του y άξονα για βέλτιστη εστίαση στο σήμα γιατί σε
                                    # αντίθεση με τα προηγούμενα σήματα η περιβάλλουσα δεν είναι συμμετρική γύρω από το 0 (έχει θετική μετατόπιση).
        # Ενημέρωση του canvas
        fig.tight_layout()      # υπολογίζει αυτόματα τις αποστάσεις μεταξύ των γραφημάτων ώστε να μην επικαλύπτονται και να φαίνονται όλα καθαρά.
        canvas.draw()       # λέει στο Matplotlib να πάρει τα νέα plots από τη μνήμη και να τα εμφανίσει στο canvas


    except ValueError:
        # Σε περίπτωση που ο χρήστης δώσει invalid entries (strings, σύμβολα)
        messagebox.showerror("Σφάλμα",
                             "Παρακαλώ εισάγετε έγκυρους αριθμούς (χρησιμοποιήστε τελεία για δεκαδικούς).", parent=root)


# --- Ρύθμιση του GUI (Tkinter) ---

root = tk.Tk()
root.title("Amplitude Modulation (AM) Demo")
root.geometry("800x700")

# Frame για τα inputs (πάνω μέρος)
input_frame = ttk.Frame(root)
input_frame.pack()      # .pack() -> τοποθετεί το στοιχείο αυτόματα στο πάνω μέρος του διαθέσιμου χώρου και το κεντράρει οριζόντια

# Input: Message Amplitude (Am)
ttk.Label(input_frame, text="Message Amplitude (Am):").grid(row=0, column=0)
entry_am = ttk.Entry(input_frame)
entry_am.insert(0, "0.5")  # Default τιμή από την εικόνα
entry_am.grid(row=1, column=0)

# Input: Message Frequency (fm)
ttk.Label(input_frame, text="Message Frequency (fm) [Hz]:").grid(row=2, column=0)
entry_fm = ttk.Entry(input_frame)
entry_fm.insert(0, "200")  # Default τιμή από την εικόνα
entry_fm.grid(row=3, column=0)

# Input: Carrier Amplitude (Ac)
ttk.Label(input_frame, text="Carrier Amplitude (Ac):").grid(row=4, column=0)
entry_ac = ttk.Entry(input_frame)
entry_ac.insert(0, "1")  # Default τιμή από την εικόνα
entry_ac.grid(row=5, column=0)

# Input: Carrier Frequency (fc)
ttk.Label(input_frame, text="Carrier Frequency (fc) [Hz]:").grid(row=6, column=0)
entry_fc = ttk.Entry(input_frame)
entry_fc.insert(0, "1000")  # Default τιμή από την εικόνα
entry_fc.grid(row=7, column=0)

# Κουμπί Generate & Plot
plot_button = ttk.Button(input_frame, text="Generate & Plot", command=generate_and_plot)    # δημιουργώ κουμπί στο input_frame και το συνδέω με τη συνάρτηση generat_and_plot
plot_button.grid(row=8, column=0, pady=(20, 10))


# --- Εμφάνιση Γραφημάτων στο GUI (Matplotlib -> Tkinter)

# Δημιουργία Figure με 4 subplots (4 γραμμές, 1 στήλη)
# Δημιουργία των subplots εκτός της συνάρτησης για βέλτιστη απόδοση.
# Αν γινόταν μέσα, θα δημιουργούσε τη δομή των αξόνων κάθε φορά από την αρχή,
# αντί απλά να ανανεώνει τα δεδομένα στα ήδη υπάρχοντα subplots.
fig = plt.figure()
ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
ax4 = fig.add_subplot(4, 1, 4)

# Ενσωμάτωση του γραφήματος στο Tkinter παράθυρο
canvas_frame = ttk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)        # Θέλω να κάνουν fit τα γραφήματα αν μεγαλώσω το παράθυρο, για αυτό κάνω τώρα .pack(fill=tk.BOTH, expand=True)

canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)     # Μετατρέπω το canvas που είναι αντικείμενο της Matplotlib σε widget για να το εμφανίσει το tkinter

# Αρχική κλήση για να εμφανιστούν τα γραφήματα με τις default τιμές με το άνοιγμα
generate_and_plot()

# --- Εκκίνηση προγράμματος ---
root.mainloop()