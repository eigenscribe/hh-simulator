import numpy as np
from hh_model import alpha_n, beta_n, alpha_m, beta_m, alpha_h, beta_h, steady_state_n, steady_state_m, steady_state_h

def create_current_injection_pattern(
    t, 
    pulses=None, 
    base_current=0.0,
    noise_amplitude=0.0
):
    """
    Create a current injection pattern based on defined pulses.
    
    Args:
        t (np.ndarray): Time vector in ms.
        pulses (list): List of dictionaries, each containing:
            - start (float): Start time of pulse in ms.
            - end (float): End time of pulse in ms.
            - amplitude (float): Current amplitude in µA/cm².
            - noise (float, optional): Noise amplitude for this pulse.
        base_current (float): Baseline current in µA/cm².
        noise_amplitude (float): Global noise amplitude.
        
    Returns:
        np.ndarray: Current injection pattern over time.
    """
    if pulses is None:
        pulses = []
        
    # Initialize with base current
    I_ext = np.ones_like(t) * base_current
    
    # If global noise is set, add it to the entire pattern
    if noise_amplitude > 0:
        I_ext += noise_amplitude * np.random.randn(len(t))
    
    # Apply each pulse
    for pulse in pulses:
        start = pulse['start']
        end = pulse['end']
        amplitude = pulse['amplitude']
        noise = pulse.get('noise', 0.0)
        
        # Find indices within the pulse time range
        idx = (t >= start) & (t < end)
        
        # Set the current for this pulse
        I_ext[idx] = amplitude
        
        # Add noise specific to this pulse if specified
        if noise > 0:
            I_ext[idx] += noise * np.random.randn(np.sum(idx))
    
    return I_ext

def hodgkin_huxley_sim(
    t_start=-30.0,
    t_end=200.0,
    dt=0.01,
    V_initial=-65.0,
    gNa=120.0,
    gK=36.0,
    gL=0.3,
    ENa=50.0,
    EK=-77.0,
    EL=-54.4,
    Cm=1.0,
    current_injection=None
):
    """
    Simulate the Hodgkin-Huxley model with customizable parameters.
    
    Args:
        t_start (float): Start time in ms.
        t_end (float): End time in ms.
        dt (float): Timestep in ms.
        V_initial (float): Initial membrane potential in mV.
        gNa (float): Maximum sodium conductance in mS/cm².
        gK (float): Maximum potassium conductance in mS/cm².
        gL (float): Leak conductance in mS/cm².
        ENa (float): Sodium reversal potential in mV.
        EK (float): Potassium reversal potential in mV.
        EL (float): Leak reversal potential in mV.
        Cm (float): Membrane capacitance in µF/cm².
        current_injection (np.ndarray or None): Custom current injection pattern. If None, use default pattern.
        
    Returns:
        dict: Dictionary containing simulation results.
    """
    # Time vector
    t = np.arange(t_start, t_end + dt, dt)
    nSteps = len(t)
    
    # Allocate buffers for storing results
    V_trace = np.zeros(nSteps)
    n_trace = np.zeros(nSteps)
    m_trace = np.zeros(nSteps)
    h_trace = np.zeros(nSteps)
    I_ext_trace = np.zeros(nSteps)
    
    # Ionic current traces
    IK_trace = np.zeros(nSteps)
    INa_trace = np.zeros(nSteps)
    IL_trace = np.zeros(nSteps)
    I_ion_trace = np.zeros(nSteps)
    
    # Membrane capacitance trace (constant)
    Cm_trace = np.ones(nSteps) * Cm
    
    # Initial conditions
    V = V_initial
    n_gate = steady_state_n(V)
    m_gate = steady_state_m(V)
    h_gate = steady_state_h(V)
    
    # Use custom current injection if provided, otherwise create default pattern
    if current_injection is None:
        default_pulses = [
            {'start': 5, 'end': 25, 'amplitude': 10, 'noise': 2},
            {'start': 50, 'end': 70, 'amplitude': -5, 'noise': 0},
            {'start': 100, 'end': 120, 'amplitude': 7, 'noise': 1},
            {'start': 150, 'end': 170, 'amplitude': -3, 'noise': 0},
            {'start': 170, 'end': 200, 'amplitude': 5, 'noise': 0}
        ]
        I_ext_trace = create_current_injection_pattern(t, default_pulses)
    else:
        I_ext_trace = current_injection
    
    # Run the simulation loop
    for i in range(nSteps):
        # Store current state
        V_trace[i] = V
        n_trace[i] = n_gate
        m_trace[i] = m_gate
        h_trace[i] = h_gate
        
        # Current injection is already set
        I_ext = I_ext_trace[i]
        
        # Compute rate constants
        an = alpha_n(V)
        bn = beta_n(V)
        am = alpha_m(V)
        bm = beta_m(V)
        ah = alpha_h(V)
        bh = beta_h(V)
        
        # Update gating variables (Euler method)
        dn_dt = an * (1.0 - n_gate) - bn * n_gate
        dm_dt = am * (1.0 - m_gate) - bm * m_gate
        dh_dt = ah * (1.0 - h_gate) - bh * h_gate
        
        n_gate += dn_dt * dt
        m_gate += dm_dt * dt
        h_gate += dh_dt * dt
        
        # Compute ionic currents (µA/cm²)
        IK = gK * (n_gate**4) * (V - EK)
        INa = gNa * (m_gate**3) * h_gate * (V - ENa)
        IL = gL * (V - EL)
        I_ion = IK + INa + IL
        
        # Store ionic currents
        IK_trace[i] = IK
        INa_trace[i] = INa
        IL_trace[i] = IL
        I_ion_trace[i] = I_ion
        
        # Update membrane potential using Euler's method: dV/dt = (I_ext - I_ion)/Cm
        V += dt * (I_ext - I_ion) / Cm
    
    # Package results
    results = {
        't': t,
        'V': V_trace,
        'n': n_trace,
        'm': m_trace,
        'h': h_trace,
        'I_ext': I_ext_trace,
        'IK': IK_trace,
        'INa': INa_trace,
        'IL': IL_trace,
        'I_ion': I_ion_trace,
        'Cm': Cm_trace
    }
    
    return results
