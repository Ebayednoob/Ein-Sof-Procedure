import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.gridspec as gridspec

# Magnetic field from a single current loop at a point on its axis
def bz_from_loop(I, R, z0, z):
    mu_0 = 4 * np.pi * 1e-7
    return (mu_0 * I * R**2) / (2 * ((R**2 + (z - z0)**2)**(1.5)))

# Total field from two matched coils centered at -spacing/2 and +spacing/2
def total_bz(z_range, spacing, turns, R, I):
    bz = np.zeros_like(z_range)
    for n in range(int(turns)):
        z1 = -spacing / 2
        z2 = spacing / 2
        bz += bz_from_loop(I, R, z1, z_range)
        bz += bz_from_loop(I, R, z2, z_range)
    return bz

# Set up the figure and layout
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(2, 2, width_ratios=[3, 1])
ax_plot = fig.add_subplot(gs[:, 0])  # Main plot on the left
ax_eq_panel = fig.add_subplot(gs[0, 1])  # Equation panel on top right
ax_eq_panel.axis("off")

# Sliders area (now on the right, below the equation panel)
slider_axs = [
    plt.axes([0.72, 0.55, 0.22, 0.03]),  # Spacing
    plt.axes([0.72, 0.50, 0.22, 0.03]),  # Turns
    plt.axes([0.72, 0.45, 0.22, 0.03]),  # Radius
    plt.axes([0.72, 0.40, 0.22, 0.03])   # Current
]

# Initial parameter values
init_spacing = 0.1
init_turns = 10
init_radius = 0.05
init_current = 1.0

z = np.linspace(-0.2, 0.2, 1000)
params = {
    'spacing': init_spacing,
    'turns': init_turns,
    'R': init_radius,
    'I': init_current
}

# Initial plot
bz = total_bz(z, **params)
field_line, = ax_plot.plot(z, bz, label='Bz (T)')
ax_plot.set_title("Magnetic Field Along Axis")
ax_plot.set_xlabel("Z Position (m)")
ax_plot.set_ylabel("Magnetic Field Bz (T)")
ax_plot.grid(True)
ax_plot.legend()

# Sliders
spacing_slider = Slider(slider_axs[0], 'Coil Spacing (m)', 0.01, 0.2, valinit=init_spacing)
turns_slider = Slider(slider_axs[1], 'Turns', 1, 50, valinit=init_turns, valstep=1)
radius_slider = Slider(slider_axs[2], 'Radius (m)', 0.01, 0.1, valinit=init_radius)
current_slider = Slider(slider_axs[3], 'Current (A)', 0.1, 10, valinit=init_current)

def update(val):
    params['spacing'] = spacing_slider.val
    params['turns'] = turns_slider.val
    params['R'] = radius_slider.val
    params['I'] = current_slider.val
    new_bz = total_bz(z, **params)
    field_line.set_ydata(new_bz)
    ax_plot.relim()
    ax_plot.autoscale_view()
    fig.canvas.draw_idle()

# Connect sliders
spacing_slider.on_changed(update)
turns_slider.on_changed(update)
radius_slider.on_changed(update)
current_slider.on_changed(update)

# Reset Button (move to right below sliders)
reset_ax = plt.axes([0.78, 0.35, 0.12, 0.04])
reset_button = Button(reset_ax, 'Reset')

def reset(event):
    spacing_slider.reset()
    turns_slider.reset()
    radius_slider.reset()
    current_slider.reset()
reset_button.on_clicked(reset)

# Show equations on the side panel
eq_text = (
    "Magnetic Field from Single Loop:\n"
    r"$B_z = \frac{{\mu_0 I R^2}}{{2 (R^2 + (z - z_0)^2)^{3/2}}}$"
    "\n\nTotal Field from Two Coils:\n"
    r"$B_{total}(z) = N \cdot (B_z(z_1) + B_z(z_2))$"
    "\n\nWhere:\n"
    r"$\mu_0 = 4\pi \times 10^{-7}$ T·m/A\n"
    r"$I$ = Current (A)\n"
    r"$R$ = Radius (m)\n"
    r"$z_0$ = Coil Center (m)\n"
    r"$N$ = Number of Turns"
)
ax_eq_panel.text(0, 1, eq_text, fontsize=10, va='top')

plt.tight_layout()
plt.show()
