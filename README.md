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

## References

- **Baker, A. A., Davies, C. S., Figueroa, A. I., Shelford, L. R., van der Laan, G., & Hesjedal, T.**  
  *Modelling ferromagnetic resonance in magnetic multilayers: Exchange coupling and demagnetisation-driven effects*,  
  *Journal of Applied Physics*, **115**(17), 17D140 (2014).  
  DOI: [10.1063/1.4868185](https://doi.org/10.1063/1.4868185)  
  [PDF Link](https://pubs.aip.org/aip/jap/article-pdf/doi/10.1063/1.4868185/14117278/17d140_1_online.pdf)  

- **Chernyshenko, Dmitri**  
  *Computational methods in micromagnetics*,  
  *PhD Thesis*, University of Southampton, June 2016.  
  URL: [https://eprints.soton.ac.uk/398126/](https://eprints.soton.ac.uk/398126/)  
