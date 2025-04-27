import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def select_directory(prompt):
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=prompt)

# Select the input directory
input_dir = select_directory("Select the input directory")

# Define the output directory within the input directory
output_dir = os.path.join(input_dir, "converted")

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through all files in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".omf") and not os.path.isdir(os.path.join(input_dir, file_name)):
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name.replace(".omf", ".ovf"))

        # Run the conversion command
        command = [
            "tclsh",
            r"C:\Users\joshi\Downloads\oommf12b4_20200930_86_x64\oommf\oommf.tcl",
            "avf2ovf",
            input_file,
            output_file,
            "-format",
            "text"
        ]

        subprocess.run(command, check=True)
        print(f"Converted: {input_file} to {output_file}")

print("All files have been converted.")
