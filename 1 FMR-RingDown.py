
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from tkinter import Tk, filedialog, simpledialog

# Create a Tkinter root window
root = Tk()
root.withdraw()  # Hide the root window

# Ask the user to input the field value and units
field_value = simpledialog.askstring("Input", "Enter the field value (e.g., 0.5):")
field_unit = simpledialog.askstring("Input", "Enter the field unit (e.g., T):")
if not field_value or not field_unit:
    print("Field value or unit not entered. Exiting...")
    exit()

# Combine field value and unit
field = f"{field_value}{field_unit}"

# Open a file dialog to select the file location
file_path = filedialog.askopenfilename(title="Select ODT File", filetypes=[("ODT files", "*.odt"), ("All files", "*.*")])
if not file_path:
    print("No file selected. Exiting...")
    exit()

# Load the ODT file into a pandas DataFrame
data = pd.read_csv(file_path, comment='#', sep=r'\s+', header=None)

# Define the column names based on the ODT file format
columns = [
    'Total_energy', 'Energy_calc_count', 'Max_dm_dt', 'dE_dt', 'Delta_E',
    'Exchange_Energy', 'Max_Spin_Ang', 'Stage_Max_Spin_Ang', 'Run_Max_Spin_Ang',
    'Demag_Energy', 'ZeemanStatic_Energy', 'Iteration', 'Stage_iteration', 'Stage',
    'mx', 'my', 'mz', 'Last_time_step', 'Simulation_time'
]
data.columns = columns

# Exclude the first and last data points
time = data['Simulation_time'].values[1:-1]
mx = data['mx'].values[1:-1]
my = data['my'].values[1:-1]
mz = data['mz'].values[1:-1]

# Remove the mean to focus on oscillations
mx_detrended = mx - np.mean(mx)
my_detrended = my - np.mean(my)
mz_detrended = mz - np.mean(mz)

# Perform FFT on the magnetization data
N = len(mx_detrended)
T = time[1] - time[0]  # Assuming uniform time steps

yf_mx = fft(mx_detrended)
yf_my = fft(my_detrended)
yf_mz = fft(mz_detrended)

xf = fftfreq(N, T)[:N//2]
xf_GHz = xf / 1e9  # Convert to GHz

# Compute power spectrum
power_spectrum_mx = 2.0 / N * np.abs(yf_mx[:N//2])
power_spectrum_my = 2.0 / N * np.abs(yf_my[:N//2])
power_spectrum_mz = 2.0 / N * np.abs(yf_mz[:N//2])

# Compute derivative of power spectrum with respect to frequency
derivative_spectrum_mx = np.gradient(power_spectrum_mx, xf_GHz)
derivative_spectrum_my = np.gradient(power_spectrum_my, xf_GHz)
derivative_spectrum_mz = np.gradient(power_spectrum_mz, xf_GHz)

# Save frequency spectrum and derivatives as CSV file
spectrum_data = pd.DataFrame({
    'Frequency (GHz)': xf_GHz,
    'Power Spectrum Mx': power_spectrum_mx,
    'Derivative Mx': derivative_spectrum_mx,
    'Power Spectrum My': power_spectrum_my,
    'Derivative My': derivative_spectrum_my,
    'Power Spectrum Mz': power_spectrum_mz,
    'Derivative Mz': derivative_spectrum_mz
})
spectrum_data.to_csv(f'frequency_spectrum_{field}_with_derivatives.csv', index=False)

# Restrict the x range to 200 GHz
x_max = 200  # GHz
xf_GHz = xf_GHz[xf_GHz <= x_max]
power_spectrum_mx = power_spectrum_mx[:len(xf_GHz)]
power_spectrum_my = power_spectrum_my[:len(xf_GHz)]
power_spectrum_mz = power_spectrum_mz[:len(xf_GHz)]

# Set the threshold as 10% of the maximum peak value
threshold_mx = 0.05 * np.max(power_spectrum_mx)
threshold_my = 0.05 * np.max(power_spectrum_my)
threshold_mz = 0.05* np.max(power_spectrum_mz)

# Find significant peaks in the power spectrum
peaks_mx, _ = find_peaks(power_spectrum_mx, height=threshold_mx)
peaks_my, _ = find_peaks(power_spectrum_my, height=threshold_my)
peaks_mz, _ = find_peaks(power_spectrum_mz, height=threshold_mz)

# Plot and save subplots for Mx
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Mx vs Simulation Time
axs[0].plot(time, mx_detrended, label='Mx')
axs[0].set_xlabel('Simulation Time (s)')
axs[0].set_ylabel('Magnetization Mx')
axs[0].set_title(f'Magnetization Mx vs Simulation Time ({field_value} {field_unit})')
axs[0].legend()
axs[0].grid()


# Power Spectrum of Mx
axs[1].plot(xf_GHz, power_spectrum_mx, color='red')
axs[1].plot(xf_GHz[peaks_mx], power_spectrum_mx[peaks_mx], 'x')
axs[1].set_xlim([0, 60])
axs[1].set_xlabel('Frequency (GHz)')
axs[1].set_ylabel('Power')
axs[1].set_title(f'Power Spectrum of Magnetization Mx ({field_value} {field_unit})')
for peak in peaks_mx:
    axs[1].annotate(f'{xf_GHz[peak]:.2f} GHz', (xf_GHz[peak], power_spectrum_mx[peak]))
axs[1].grid()

plt.tight_layout()
plt.savefig(f'Mx_plot_{field}.png')
plt.show()
plt.close()

# Plot and save subplots for My
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# My vs Simulation Time
axs[0].plot(time, my_detrended, label='My')
axs[0].set_xlabel('Simulation Time (s)')
axs[0].set_ylabel('Magnetization My')
axs[0].set_title(f'Magnetization My vs Simulation Time ({field_value} {field_unit})')
axs[0].legend()
axs[0].grid()

# Power Spectrum of My
axs[1].plot(xf_GHz, power_spectrum_my, color='green')
axs[1].plot(xf_GHz[peaks_my], power_spectrum_my[peaks_my], 'x')
axs[1].set_xlim([0, 200])
axs[1].set_xlabel('Frequency (GHz)')
axs[1].set_ylabel('Power')
axs[1].set_title(f'Power Spectrum of Magnetization My ({field_value} {field_unit})')
for peak in peaks_my:
    axs[1].annotate(f'{xf_GHz[peak]:.2f} GHz', (xf_GHz[peak], power_spectrum_my[peak]))
axs[1].grid()

plt.tight_layout()
plt.savefig(f'My_plot_{field}.png')
plt.close()

# Plot and save subplots for Mz
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Mz vs Simulation Time
axs[0].plot(time, mz_detrended, label='Mz')
axs[0].set_xlabel('Simulation Time (s)')
axs[0].set_ylabel('Magnetization Mz')
axs[0].set_title(f'Magnetization Mz vs Simulation Time ({field_value} {field_unit})')
axs[0].legend()
axs[0].grid()

# Power Spectrum of Mz
axs[1].plot(xf_GHz, power_spectrum_mz, color='blue')
axs[1].plot(xf_GHz[peaks_mz], power_spectrum_mz[peaks_mz], 'x')
axs[1].set_xlim([0, 200])
axs[1].set_xlabel('Frequency (GHz)')
axs[1].set_ylabel('Power')
axs[1].set_title(f'Power Spectrum of Magnetization Mz ({field_value} {field_unit})')
for peak in peaks_mz:
    axs[1].annotate(f'{xf_GHz[peak]:.2f} GHz', (xf_GHz[peak], power_spectrum_mz[peak]))
axs[1].grid()

plt.tight_layout()
plt.savefig(f'Mz_plot_{field}.png')
plt.close()

# Report of peak power and corresponding frequencies
report = f"""
Peak Power and Corresponding Frequencies:
-----------------------------------------
Field Value: {field}
-----------------------------------------
Mx:
"""
for peak in peaks_mx:
    report += f"    Peak Power: {power_spectrum_mx[peak]:.2e}, Frequency: {xf_GHz[peak]:.2f} GHz\n"

report += "My:\n"
for peak in peaks_my:
    report += f"    Peak Power: {power_spectrum_my[peak]:.2e}, Frequency: {xf_GHz[peak]:.2f} GHz\n"

report += "Mz:\n"
for peak in peaks_mz:
    report += f"    Peak Power: {power_spectrum_mz[peak]:.2e}, Frequency: {xf_GHz[peak]:.2f} GHz\n"

print(report)
