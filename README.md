# **Micromagnetic Simulations of Ferromagnetic Resonance (FMR) Using OOMMF**  

### **Introduction**  
This repository contains scripts and documentation for micromagnetic simulations focused on **Ferromagnetic Resonance (FMR)** using the **Object-Oriented Micromagnetic Framework (OOMMF)**. The simulations explore **exchange stiffness, demagnetization factors**, and the **Landau-Lifshitz-Gilbert (LLG) equation** to model magnetization dynamics.

### **Watch the Overview Video**  
[![Watch the video](https://img.youtube.com/vi/f7RvDqdZ2IE/0.jpg)](https://youtu.be/f7RvDqdZ2IE)  
Click the thumbnail above to watch an in-depth explanation of the simulation process.

---

## **Features**  
- Computational modeling of **Ferromagnetic Resonance (FMR)**  
- Solving the **LLG equation** using **OOMMF**  
- Analysis of **demagnetization factors** and **exchange stiffness effects**  
- Time-domain and frequency-domain simulations using **Fourier Transform**  
- Comparison of **theoretical predictions** with experimental data
- Complex simulation data analysis using Python

---

## **Simulation Process**  
1️⃣ **Equilibrium Configuration:**  
   - The magnetic energy is minimized to obtain the **ground state** of the system.  

2️⃣ **Dynamic Excitation:**  
   - A small **magnetic pulse** is applied perpendicular to the DC magnetic field to excite the system.  

3️⃣ **Time Evolution:**  
   - The **magnetization dynamics** are recorded and analyzed over time.  

4️⃣ **Frequency Analysis:**  
   - The **Fast Fourier Transform (FFT)** is applied to extract resonance spectra for comparison.
 
5️⃣ **Spatial Modes Anlysis:**
   - The time varying magnetization at each cell is extracted and the spatial Fourier Transform is done to get the spatial distribution of resonance modes.

---

## **Installation & Requirements**  
Ensure that you have the following dependencies installed:  
- **OOMMF:** [Download here](http://math.nist.gov/oommf/)  
- **Python 3.11.3** (for data processing)  
- **NumPy**, **Matplotlib** (for visualization)  

