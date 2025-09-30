# Example script for generating seismic spectrum for soil type B
# This script demonstrates how to use the seismic calculation library
# to compute parameters and spectrum for a specific soil type

import seismic_calculations
import matplotlib.pyplot as plt
import export_utilities

# Set fixed parameters for soil type B
tipo_suelo = 'B'  # Soil type B
zona_sismica = 'III'  # Seismic zone III
region = 'Costa'  # Coastal region
R = 3  # Reduction factor
I = 1.0  # Importance factor
phi_P = 1.0  # Configuration factor in plan
phi_E = 1.0  # Configuration factor in elevation
r = 1.0  # Exponent for spectrum decay

# Calculate seismic parameters based on soil type, zone, and region
parametros, eta, Z = seismic_calculations.calculate_parameters(tipo_suelo, zona_sismica, region)
Fa, Fd, Fs, r_param = parametros['Fa'], parametros['Fd'], parametros['Fs'], parametros['r']

# Calculate the seismic spectrum
T, Sa, Se, Si, T0, Tc, TL = seismic_calculations.calculate_spectrum(Z, Fa, Fd, Fs, eta, R, I, phi_P, phi_E, r_param)

# Create a matplotlib plot of the spectrum
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(T, Sa, 'b-', label='Sa (Elastic spectrum)')
ax.plot(T, Si, 'r-', label='Si (Inelastic spectrum)')

# Mark characteristic points
ax.axvline(x=T0, color='g', linestyle='--', alpha=0.7, label=f'T0 = {T0:.2f}s')
ax.axvline(x=Tc, color='m', linestyle='--', alpha=0.7, label=f'Tc = {Tc:.2f}s')
ax.axvline(x=TL, color='c', linestyle='--', alpha=0.7, label=f'TL = {TL:.2f}s')

# Set plot limits and labels
ax.set_xlim(0, max(5, TL + 0.1))
ax.set_title('Seismic Design Spectrum NEC - Soil Type B')
ax.set_xlabel('Period T (s)')
ax.set_ylabel('Acceleration Sa (g)')
ax.grid(True)
ax.legend()

# Add parameter information to the plot
info_text = (f"Z = {Z:.2f}g, R = {R}, I = {I}\n"
            f"Fa = {Fa:.2f}, Fd = {Fd:.2f}, Fs = {Fs:.2f}, η = {eta:.2f}\n"
            f"φP = {phi_P:.2f}, φE = {phi_E:.2f}")
ax.text(0.02, 0.02, info_text, transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8))

# Export the plot to PNG using the existing export function
export_utilities.save_image(fig)

# Generate a PDF report using the existing export function
export_utilities.generate_pdf_report(T, Sa, Se, Si, zona_sismica, tipo_suelo, region, R, I, phi_P, phi_E, fig)