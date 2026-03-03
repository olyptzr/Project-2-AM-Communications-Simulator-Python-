import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # I'm adding this so if the user enters wrong values, it displays an error message in a window and not just in the console

# --- Creating the generate_and_plot function ---
# Initially, I create a function that will perform the plots when I press the Generate & Plot button of the window
def generate_and_plot():
    try:    # I use try-except to check user input values (must be numbers and not symbols or strings)
        # 1. Get values from entries
        Am = float(entry_am.get())
        fm = float(entry_fm.get())
        Ac = float(entry_ac.get())
        fc = float(entry_fc.get())

        # Check for Ac = 0
        if Ac == 0:
            messagebox.showerror("Error", "The carrier amplitude (Ac) cannot be 0.", parent=root)
            return

        # Check for negative values
        if Am < 0 or fm < 0 or Ac < 0 or fc < 0:
            messagebox.showerror("Value Error", "Amplitude and Frequency values must be positive numbers.", parent=root)
            return

        # Optional check: Must be fc >> fm
        if fc <= fm:
            messagebox.showwarning("Warning!",
                                   "For proper AM modulation, the carrier frequency (fc) must be significantly higher than the message frequency (fm).", parent=root)
            # I do not return, I just warn and continue

        # 2. Create time axis t (from 0 to 0.02 sec)
        t_limit = 0.02
        total_points = int(max(1000, fc * t_limit * 100))       # Sampling adjustment (100 points per period) for smooth visualization for any time_limit and fc,
                                                                # with a minimum limit (1000) for smooth visualization at low frequencies

        t = np.linspace(0, t_limit, total_points)

        # 3. Signal calculation
        # Message Signal
        # m(t) = Am * cos(2*pi*fm*t)
        message_signal = Am * np.cos(2*np.pi*fm*t)

        # Carrier Signal
        # c(t) = Ac * cos(2*pi*fc*t)
        carrier_signal = Ac * np.cos(2*np.pi*fc*t)

        # Modulation index
        m = Am / Ac

        # AM Signal
        # s(t) = Ac * (1 + m * cos(2*pi*fm*t)) * cos(2*pi*fc*t)
        am_signal = Ac * (1 + m * np.cos(2*np.pi*fm*t)) * np.cos(2*np.pi*fc*t)

        # Demodulated Signal (Envelope)
        # E(t) = Ac * |1 + m * cos(2pi*fm*t)|
        demodulated_signal = Ac * np.abs(1 + m * np.cos(2*np.pi*fm*t))

        # 4. Plotting diagrams
        # Clear previous graphs to avoid graph overlap
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()

        # Plot 1: Message Signal
        ax1.plot(t, message_signal, color='blue')
        ax1.set_title('Message Signal', fontsize=10)
        ax1.grid(True)
        ax1.set_ylabel('Amplitude')     # I add names to the axes, although they were omitted in the instructions
        ax1.set_xlim(0, t_limit)       # Because I want the graphs to start exactly at the beginning of the axis (0) and end exactly at the end (0.02)
        ax1.set_ylim(-np.ceil(Am), np.ceil(Am))         # Scaling to have integer Y-axis limits

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
        ax4.set_xlim(0, t_limit)       # I leave autoscaling for the Y-axis limits for optimal signal focus because
                                       # unlike previous signals, the envelope is not symmetric around 0 (it has a positive offset).
        # Update canvas
        fig.tight_layout()      # Automatically calculates distances between graphs so they don't overlap and look clear.
        canvas.draw()       # Tells Matplotlib to take the new plots from memory and display them on the canvas


    except ValueError:
        # In case the user provides invalid entries (strings, symbols)
        messagebox.showerror("Error",
                             "Please enter valid numbers (use a dot for decimals).", parent=root)


# --- GUI Setup (Tkinter) ---

root = tk.Tk()
root.title("Amplitude Modulation (AM) Demo")
root.geometry("800x700")

# Frame for inputs (top part)
input_frame = ttk.Frame(root)
input_frame.pack()      # .pack() -> places the element automatically at the top of the available space and centers it horizontally

# Input: Message Amplitude (Am)
ttk.Label(input_frame, text="Message Amplitude (Am):").grid(row=0, column=0)
entry_am = ttk.Entry(input_frame)
entry_am.insert(0, "0.5")  # Default value from image
entry_am.grid(row=1, column=0)

# Input: Message Frequency (fm)
ttk.Label(input_frame, text="Message Frequency (fm) [Hz]:").grid(row=2, column=0)
entry_fm = ttk.Entry(input_frame)
entry_fm.insert(0, "200")  # Default value from image
entry_fm.grid(row=3, column=0)

# Input: Carrier Amplitude (Ac)
ttk.Label(input_frame, text="Carrier Amplitude (Ac):").grid(row=4, column=0)
entry_ac = ttk.Entry(input_frame)
entry_ac.insert(0, "1")  # Default value from image
entry_ac.grid(row=5, column=0)

# Input: Carrier Frequency (fc)
ttk.Label(input_frame, text="Carrier Frequency (fc) [Hz]:").grid(row=6, column=0)
entry_fc = ttk.Entry(input_frame)
entry_fc.insert(0, "1000")  # Default value from image
entry_fc.grid(row=7, column=0)

# Generate & Plot Button
plot_button = ttk.Button(input_frame, text="Generate & Plot", command=generate_and_plot)    # I create a button in the input_frame and link it to the generate_and_plot function
plot_button.grid(row=8, column=0, pady=(20, 10))


# --- Display Graphs in GUI (Matplotlib -> Tkinter)

# Create Figure with 4 subplots (4 rows, 1 column)
# Create subplots outside the function for optimal performance.
# If done inside, it would create the axis structure from scratch every time,
# instead of simply updating data in already existing subplots.
fig = plt.figure()
ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
ax4 = fig.add_subplot(4, 1, 4)

# Integrate the graph into the Tkinter window
canvas_frame = ttk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True)        # I want the graphs to fit if I resize the window, so I use .pack(fill=tk.BOTH, expand=True)

canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)     # I convert the Matplotlib canvas object into a widget for Tkinter to display it

# Initial call to display graphs with default values upon opening
generate_and_plot()

# --- Start program ---
root.mainloop()