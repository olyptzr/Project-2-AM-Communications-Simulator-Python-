# Project 2: AM Communications Simulator (Python)
Developed a Python application with a Tkinter-based GUI for simulating Amplitude Modulation (AM) and demodulation. Used NumPy for signal processing calculations and Matplotlib for real-time visualization of information and carrier signals in the time domain.

## Key Features
* **Interactive GUI:** Developed using **Tkinter** to allow users to dynamically adjust signal parameters such as Message/Carrier Amplitudes ($A_m, A_c$) and Frequencies ($f_m, f_c$).
* **Real-time Visualization:** Integrated **Matplotlib** to generate four synchronized subplots:
    1.  **Message Signal:** The original information wave.
    2.  **Carrier Signal:** The high-frequency wave used for transmission.
    3.  **AM Signal:** The resulting modulated wave.
    4.  **Demodulated Signal:** The recovered envelope of the original message.
* **Dynamic Sampling:** Implemented an adaptive sampling rate to ensure high-fidelity signal rendering across a wide range of carrier frequencies.
* **Input Validation:** Robust error handling using `try-except` blocks and pop-up alerts (`messagebox`) to prevent invalid data entry and non-physical values.

## Mathematical Implementation
The simulator uses **NumPy** for high-performance vectorized calculations based on standard communication formulas:
* **Modulation Index ($m$):** $m = \frac{A_m}{A_c}$
* **AM Waveform ($s(t)$):** $s(t) = A_c [1 + m \cdot \cos(2\pi f_m t)] \cdot \cos(2\pi f_c t)$
* **Envelope Detection:** Modeled using the absolute value of the analytical signal to simulate recovery.



## Technologies Used
* **Python 3.x**
* **NumPy:** Vectorized mathematical operations.
* **Matplotlib:** Time-domain signal plotting.
* **Tkinter:** Graphical User Interface (GUI) development.

## How to Run
To run the simulator locally, first ensure you have the required libraries installed:

```bash
pip install numpy matplotlib
```

Then, execute the main script:

```bash
PythonProject_AM_Simulator.py
```
