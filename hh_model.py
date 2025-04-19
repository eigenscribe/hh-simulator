import numpy as np

def alpha_n(V):
    """Rate constant alpha_n(V) for gating variable n."""
    return (0.01 * (10.0 - (V + 65.0))) / (np.exp((10.0 - (V + 65.0)) / 10.0) - 1.0)

def beta_n(V):
    """Rate constant beta_n(V) for gating variable n."""
    return 0.125 * np.exp(-(V + 65.0) / 80.0)

def alpha_m(V):
    """Rate constant alpha_m(V) for gating variable m."""
    return (0.1 * (25.0 - (V + 65.0))) / (np.exp((25.0 - (V + 65.0)) / 10.0) - 1.0)

def beta_m(V):
    """Rate constant beta_m(V) for gating variable m."""
    return 4.0 * np.exp(-(V + 65.0) / 18.0)

def alpha_h(V):
    """Rate constant alpha_h(V) for gating variable h."""
    return 0.07 * np.exp(-(V + 65.0) / 20.0)

def beta_h(V):
    """Rate constant beta_h(V) for gating variable h."""
    return 1.0 / (np.exp((30.0 - (V + 65.0)) / 10.0) + 1.0)

def steady_state_n(V):
    """Compute steady-state value of n for given voltage V."""
    return alpha_n(V) / (alpha_n(V) + beta_n(V))

def steady_state_m(V):
    """Compute steady-state value of m for given voltage V."""
    return alpha_m(V) / (alpha_m(V) + beta_m(V))

def steady_state_h(V):
    """Compute steady-state value of h for given voltage V."""
    return alpha_h(V) / (alpha_h(V) + beta_h(V))

def time_constant_n(V):
    """Compute time constant tau_n for given voltage V."""
    return 1.0 / (alpha_n(V) + beta_n(V))

def time_constant_m(V):
    """Compute time constant tau_m for given voltage V."""
    return 1.0 / (alpha_m(V) + beta_m(V))

def time_constant_h(V):
    """Compute time constant tau_h for given voltage V."""
    return 1.0 / (alpha_h(V) + beta_h(V))
