import os
import re
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

def parse_ovf_file(file_path):
    header = {}
    data = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse header
    for line in lines:
        if line.startswith('#'):
            key_value = line[1:].strip().split(': ')
            if len(key_value) == 2:
                header[key_value[0].strip()] = key_value[1].strip()
        elif line.startswith('##'):
            # End of header
            break
        else:
            # Parse data
            if '## End: Data' not in line:
                values = list(map(float, line.strip().split()))
                data.append(values)

    return header, np.array(data)

def extract_time_dependent_data(directory_path):
    time_steps = []
    magnetization_data = []

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.ovf'):
            file_path = os.path.join(directory_path, file_name)
            header, data = parse_ovf_file(file_path)

            # Extract the first six-digit numerical part after hyphen
            match = re.search(r'-(\d{9,10})-', file_name)
            if match:
                primary_step = int(match.group(1))  # Use the matched sequence as the time step
                print(f"File: {file_name}, Extracted Time Step: {primary_step}")
            else:
                print(f"Skipping file {file_name}: Could not extract numerical part from file name.")
                continue

            time_steps.append(primary_step)
            magnetization_data.append(data.tolist())  # Convert data to list to avoid ambiguity

    # Debugging: Print time steps and magnetization data lengths
    print("Time Steps:", time_steps)
    print("Magnetization Data Lengths:", [len(d) for d in magnetization_data])

    # Sort data based on primary time steps
    sorted_data = sorted(zip(time_steps, magnetization_data))
    if sorted_data:
        time_steps, magnetization_data = zip(*sorted_data)
    else:
        print("No valid files found.")
        return [], []

    return time_steps, magnetization_data

def convert_time_steps_to_simulation_times(time_steps, stage_simulation_time):
    # Convert time steps to simulation times assuming each step represents stage_simulation_time
    simulation_times = [step * stage_simulation_time for step in time_steps]

    # Ensure the time steps are correctly spaced
    unique_time_steps = sorted(set(simulation_times))
    if len(unique_time_steps) > 1:
        dt = unique_time_steps[1] - unique_time_steps[0]
    else:
        dt = 2e-12  # Small default value to avoid zero division

    # Debugging: Print simulation times and dt
    print("Simulation Times:", simulation_times)
    print("Time Step Difference (dt):", dt)

    return simulation_times, dt

def compute_fourier_transform(magnetization_data, simulation_times, dt, xnodes, ynodes, znodes):
    # Reshape magnetization data to 5D array (time, z, y, x, 3)
    magnetization_array = np.array(magnetization_data).reshape((len(simulation_times), znodes, ynodes, xnodes, 3))

    # Perform Fourier Transform on time-dependent magnetization for each cell
    fft_magnetization = np.fft.fft(magnetization_array, axis=0)

    # Compute the magnitude of the Fourier Transform
    magnitude = np.abs(fft_magnetization)

    # Compute the frequency corresponding to each mode
    frequencies = np.fft.fftfreq(len(simulation_times), d=dt)

    # Filter positive frequencies
    pos_indices = np.where(frequencies > 0)
    positive_frequencies = frequencies[pos_indices]
    magnitude = magnitude[pos_indices]

    return magnitude, positive_frequencies

def visualize_all_modes(magnitude, frequencies, frequency, xnodes, ynodes, znodes, xstepsize, ystepsize):
    # Find the index corresponding to the specified frequency
    freq_index = np.argmin(np.abs(frequencies - frequency))

    fig, axes = plt.subplots(znodes, 3, figsize=(15, znodes * 5))
    for z in range(znodes):
        for c, comp in enumerate(['Mx', 'My', 'Mz']):
            ax = axes[z, c]
            im = ax.imshow(magnitude[freq_index, z, :, :, c], cmap='viridis', origin='lower',
                           extent=[0, xnodes * xstepsize * 1e9, 0, ynodes * ystepsize * 1e9])
            ax.set_xlabel('X(nm)')
            ax.set_ylabel('Y(nm)')
            fig.colorbar(im, ax=ax)

    # Add a single title for the entire plot
    fig.suptitle(f'Resonance Frequency: {frequency:.4e} Hz', fontsize=16)

    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust layout to fit the suptitle
    plt.show()

def visualize_and_save_modes_for_layer(magnitude, frequencies, frequency, xnodes, ynodes, znodes, xstepsize, ystepsize, save_directory):
    # Find the index corresponding to the specified frequency
    freq_index = np.argmin(np.abs(frequencies - frequency))

    # Save plots for Z=2 layer
    z = 2  # Layer index
    components = ['Mx', 'My', 'Mz']

    for c, comp in enumerate(components):
        plt.figure(figsize=(8, 6))
        plt.imshow(
            magnitude[freq_index, z, :, :, c],
            cmap='viridis',
            origin='lower',
            extent=[0, xnodes * xstepsize * 1e9, 0, ynodes * ystepsize * 1e9]
        )
        plt.title(f'Spatial Mode {comp} at Z={z}\nFrequency: {frequency:.4e} Hz')
        plt.xlabel('X Axis (nm)')
        plt.ylabel('Y Axis (nm)')
        plt.colorbar(label='Magnitude')

        # Save the plot
        save_path = os.path.join(save_directory, f"Spatial_Mode_{comp}_Z{z}_Frequency_{frequency:.4e}Hz.png")
        plt.savefig(save_path)
        plt.close()
        print(f"Plot saved: {save_path}")

def generate_resonance_report(frequencies):
    # Generate the report
    report = "Resonance Frequencies (Hz):\n"
    for freq in frequencies:
        report += f"{freq:.4e}\n"

    # Save the report to a text file
    with open("resonance_frequencies_report.txt", "w") as file:
        file.write(report)

    print(report)

def select_directory(prompt):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=prompt)

# Select the input directory
directory_path = select_directory("Select the input directory")

# Assumed stage simulation time (should match the parameter in your OOMMF script)
stage_simulation_time = 2e-12  # Adjust based on your actual stage simulation time

# Mesh dimensions (adjust based on your mesh settings)
xnodes = 100
ynodes = 100
znodes = 5
xstepsize = 2e-9  # Step size in meters
ystepsize = 2e-9  # Step size in meters

time_steps, magnetization_data = extract_time_dependent_data(directory_path)
simulation_times, dt = convert_time_steps_to_simulation_times(time_steps, stage_simulation_time)
magnitude, frequencies = compute_fourier_transform(magnetization_data, simulation_times, dt, xnodes, ynodes, znodes)

# Frequency of interest
frequency_of_interest = [39.54e9, 41.69e9, 44.55e9]

# Visualize all Z values for Mx, My, and Mz for all frequencies
for freq in frequency_of_interest:
    print(f"Visualizing modes for frequency: {freq:.4e} Hz")
    visualize_all_modes(magnitude, frequencies, freq, xnodes, ynodes, znodes, xstepsize, ystepsize)

# Prompt user to select an output directory
output_directory = select_directory("Select the directory to save the plots")

# Save Z=2 modes for Mx, My, and Mz for all frequencies
for freq in frequency_of_interest:
    print(f"Saving modes for frequency: {freq:.4e} Hz")
    visualize_and_save_modes_for_layer(magnitude, frequencies, freq, xnodes, ynodes, znodes, xstepsize, ystepsize, output_directory)

generate_resonance_report(frequencies)