import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp


# Physical parameters
M = 1.0
L = 4.0

# Initial conditions
r0 = 40
radial_velocity_0 = 0.0
phi0 = 0.0
initial_state = [r0,radial_velocity_0,phi0]
tau_max = 5000

# Schwarzschild geodesic equations
def geodesic_equations(tau, state):
    r, radial_velocity, phi = state
    dr_dtau = radial_velocity
    d2r_dtau2 = (-M / r**2+ L**2 / r**3- 3 * M*L**2/ r**4)
    dphi_dtau = L / r**2
    return [dr_dtau,d2r_dtau2,dphi_dtau]

solution = solve_ivp(geodesic_equations,(0, tau_max),initial_state,method="DOP853",rtol=1e-10,atol=1e-12,max_step=1.0)

if not solution.success:
    raise RuntimeError("Numerical integration failed.")
r = solution.y[0]
phi = solution.y[2]
x = r * np.cos(phi)
y = r * np.sin(phi)

schwarzschild_radius = 2 * M
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel(r"$x$", fontsize=12)
ax.set_ylabel(r"$y$", fontsize=12)
ax.set_title("Particle Motion in Schwarzschild Spacetime",fontsize=15,pad=15)
ax.grid(True, alpha=0.2)
padding = 0.08

x_range = x.max() - x.min()
y_range = y.max() - y.min()

x_min = x.min() - padding * x_range
x_max = x.max() + padding * x_range
y_min = y.min() - padding * y_range
y_max = y.max() + padding * y_range

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Black hole
black_hole = plt.Circle((0, 0),schwarzschild_radius,color="black",zorder=5)
ax.add_patch(black_hole)
horizon_boundary = plt.Circle((0, 0),schwarzschild_radius,fill=False,linestyle="--",linewidth=1.2,alpha=0.7)
ax.add_patch(horizon_boundary)

# Trajectory and particle objects
trajectory, = ax.plot([],[],linewidth=1.4,label="Particle trajectory")
particle, = ax.plot([],[],"o",markersize=6,label="Particle")
info = (r"$G=c=1$" "\n"
    rf"$M={M}$" "\n"
    rf"$L={L}$")

ax.text(0.03,0.97,info,transform=ax.transAxes,verticalalignment="top",fontsize=10,bbox=dict(boxstyle="round,pad=0.4",alpha=0.85))
ax.legend(loc="upper right")
number_of_frames = 500
frame_indices = np.linspace(0,len(x) - 1,number_of_frames,).astype(int)

def update(frame):
    index = frame_indices[frame]
    trajectory.set_data(x[:index + 1],y[:index + 1])
    particle.set_data(np.array([x[index]]), np.array([y[index]]))
    return trajectory, particle

# Animation
animation = FuncAnimation(fig,update,frames=number_of_frames,interval=30,blit=True)
animation.save("schwarzschild_orbit.gif",writer=PillowWriter(fps=30))
plt.show()

# Static orbit plot
fig_static, ax_static = plt.subplots(figsize=(8, 8))
ax_static.set_aspect("equal", adjustable="box")
ax_static.set_xlabel(r"$x$", fontsize=12)
ax_static.set_ylabel(r"$y$", fontsize=12)
ax_static.set_title("Particle Trajectory in Schwarzschild Spacetime",fontsize=15,pad=15)
ax_static.grid(True, alpha=0.2)
ax_static.plot(x,y,linewidth=1.4,label="Particle trajectory")

# Black hole
black_hole_static = plt.Circle((0, 0),schwarzschild_radius,color="black",zorder=5)
ax_static.add_patch(black_hole_static)
horizon_static = plt.Circle((0, 0),schwarzschild_radius,fill=False,linestyle="--",linewidth=1.2,alpha=0.7,label=r"Schwarzschild radius $r_s=2M$")
ax_static.add_patch(horizon_static)
ax_static.scatter(x[0],y[0],s=45,zorder=6,label="Initial position")

info_static = (r"$G=c=1$" "\n"rf"$M={M}$" "\n"rf"$L={L}$")
ax_static.text(0.03,0.97,info_static,transform=ax_static.transAxes,verticalalignment="top",fontsize=10,bbox=dict(boxstyle="round,pad=0.4",alpha=0.85))
ax_static.set_xlim(x_min, x_max)
ax_static.set_ylim(y_min, y_max)
ax_static.legend(loc="upper right")
plt.tight_layout()
plt.savefig("schwarzschild_orbit.png",dpi=300,bbox_inches="tight")