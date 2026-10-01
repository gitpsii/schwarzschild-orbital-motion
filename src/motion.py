import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# SCHWARZSCHILD GEODESIC SIMULATION


# 1. Physical parameters

# Geometrized units:
# G = c = 1

M = 1.0

# Conserved specific energy
E = 0.98

# Conserved specific angular momentum
L = 4.0



# 2. Initial conditions


# Initial radial position
r0 = 41.1673

# Initial radial velocity dr/dtau
vr0 = 0.0

# Initial angular position
phi0 = 0.0

# Initial coordinate time
t0 = 0.0

# State vector:
# Y = [r, dr/dtau, phi, t]

Y0 = [
    r0,
    vr0,
    phi0,
    t0
]



# 3. Schwarzschild equations of motion


def schwarzschild_geodesic(tau, Y):

    r = Y[0]
    vr = Y[1]
    phi = Y[2]
    t = Y[3]

    # dr/dtau
    dr_dtau = vr

    # d2r/dtau2
    dvr_dtau = (
        -M / r**2
        + L**2 / r**3
        - 3 * M * L**2 / r**4
    )

    # dphi/dtau
    dphi_dtau = L / r**2

    # dt/dtau
    dt_dtau = E / (1 - 2 * M / r)

    return [
        dr_dtau,
        dvr_dtau,
        dphi_dtau,
        dt_dtau
    ]



# 4. Integration


# Proper-time interval
tau_start = 0
tau_end = 5000

tau_span = (tau_start, tau_end)

# Numerical integration
solution = solve_ivp(
    schwarzschild_geodesic,
    tau_span,
    Y0,
    method="DOP853",
    rtol=1e-10,
    atol=1e-12,
    max_step=1.0
)



# 5. Extract solution


tau = solution.t

r = solution.y[0]
vr = solution.y[1]
phi = solution.y[2]
t = solution.y[3]



# 6. Convert polar coordinates to Cartesian coordinates

x = r * np.cos(phi)
y = r * np.sin(phi)



# 7. Schwarzschild radius


rs = 2 * M

theta = np.linspace(0, 2 * np.pi, 500)

x_horizon = rs * np.cos(theta)
y_horizon = rs * np.sin(theta)


# 8. Plot orbit


plt.figure(figsize=(8, 8))

plt.plot(
    x,
    y,
    linewidth=1.2,
    label="Particle trajectory"
)

plt.plot(
    x_horizon,
    y_horizon,
    "--",
    linewidth=1.5,
    label="Schwarzschild radius"
)

# Mark initial position
plt.scatter(
    x[0],
    y[0],
    s=50,
    label="Initial position"
)

# Mark black-hole center
plt.scatter(
    0,
    0,
    s=100,
    marker="o",
    label="Black hole"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Timelike Geodesic in Schwarzschild Spacetime")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()


# 9. Plot radial distance as a function of proper time


plt.figure(figsize=(10, 5))

plt.plot(
    tau,
    r,
    linewidth=1.2
)

plt.axhline(
    rs,
    linestyle="--",
    linewidth=1.2,
    label="Schwarzschild radius"
)

plt.xlabel(r"Proper time $\tau$")
plt.ylabel(r"Radial coordinate $r$")
plt.title(r"Radial Motion: $r(\tau)$")
plt.grid(True)
plt.legend()
plt.show()


# 10. Plot angular position as a function of proper time


plt.figure(figsize=(10, 5))

plt.plot(
    tau,
    phi,
    linewidth=1.2
)

plt.xlabel(r"Proper time $\tau$")
plt.ylabel(r"Angular coordinate $\phi$")
plt.title(r"Angular Motion: $\phi(\tau)$")
plt.grid(True)
plt.show()

# 11. Basic numerical results

print(" SCHWARZSCHILD GEODESIC SIMULATION")

print(f"Mass parameter M       = {M}")
print(f"Specific energy E      = {E}")
print(f"Angular momentum L     = {L}")

print()

print(f"Initial radius r0      = {r[0]:.6f}")
print(f"Minimum radius         = {np.min(r):.6f}")
print(f"Maximum radius         = {np.max(r):.6f}")

print()

print(f"Initial phi            = {phi[0]:.6f}")
print(f"Final phi              = {phi[-1]:.6f}")

print()

print(f"Schwarzschild radius   = {rs:.6f}")

print()

print("Number of integration")
print(f"points                 = {len(tau)}")