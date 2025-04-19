import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation import hodgkin_huxley_sim, create_current_injection_pattern
from visualization import display_simulation_results

# Set page configuration
st.set_page_config(
    page_title="Neural Signal Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and introduction
st.title("Neural Signal Analysis Simulator")
st.markdown("""
This application simulates neural signal dynamics using the Hodgkin-Huxley model, which describes how action potentials are initiated and propagated in neurons.

The Hodgkin-Huxley model is a set of nonlinear differential equations that approximate the electrical characteristics of excitable cells such as neurons and muscle cells.
""")

# Sidebar for simulation parameters
st.sidebar.title("Simulation Parameters")

# Time parameters
st.sidebar.subheader("Time Settings")
t_start = st.sidebar.number_input("Start Time (ms)", value=-30.0, step=10.0)
t_end = st.sidebar.number_input("End Time (ms)", value=200.0, min_value=50.0, step=50.0)
dt = st.sidebar.number_input("Time Step (ms)", value=0.01, min_value=0.001, max_value=1.0, step=0.01, format="%.3f")

# Membrane properties
st.sidebar.subheader("Membrane Properties")
initial_voltage = st.sidebar.number_input("Initial Membrane Potential (mV)", value=-65.0, step=5.0)
cm = st.sidebar.number_input("Membrane Capacitance (µF/cm²)", value=1.0, min_value=0.1, step=0.1)

# Channel conductances
st.sidebar.subheader("Channel Conductances (mS/cm²)")
g_na = st.sidebar.number_input("Sodium (Na⁺) Conductance", value=120.0, min_value=0.0, step=10.0)
g_k = st.sidebar.number_input("Potassium (K⁺) Conductance", value=36.0, min_value=0.0, step=5.0)
g_l = st.sidebar.number_input("Leak Conductance", value=0.3, min_value=0.0, step=0.1)

# Reversal potentials
st.sidebar.subheader("Reversal Potentials (mV)")
e_na = st.sidebar.number_input("Sodium (Na⁺) Reversal Potential", value=50.0, step=5.0)
e_k = st.sidebar.number_input("Potassium (K⁺) Reversal Potential", value=-77.0, step=5.0)
e_l = st.sidebar.number_input("Leak Reversal Potential", value=-54.4, step=5.0)

# Current injection parameters
st.sidebar.subheader("Current Injection")

# Choice between simple and advanced current injection
current_mode = st.sidebar.radio(
    "Current Injection Mode", 
    ["Simple", "Advanced (Custom Pulses)"]
)

if current_mode == "Simple":
    # Simple current injection
    amplitude = st.sidebar.slider("Stimulus Amplitude (µA/cm²)", min_value=-20.0, max_value=30.0, value=10.0, step=1.0)
    start_time = st.sidebar.slider("Stimulus Start Time (ms)", min_value=0.0, max_value=t_end-10, value=5.0, step=5.0)
    duration = st.sidebar.slider("Stimulus Duration (ms)", min_value=1.0, max_value=t_end-start_time, value=20.0, step=5.0)
    noise_level = st.sidebar.slider("Noise Level (µA/cm²)", min_value=0.0, max_value=5.0, value=0.0, step=0.5)
    
    # Create a simple current injection pattern
    custom_pulses = [{'start': start_time, 'end': start_time + duration, 'amplitude': amplitude, 'noise': noise_level}]
    
else:  # Advanced mode
    st.sidebar.markdown("### Custom Current Pulses")
    st.sidebar.markdown("You can define up to 5 custom current pulses:")
    
    # Initialize pulses list
    custom_pulses = []
    
    # Generate up to 5 configurable pulses
    for i in range(5):
        # Use an expander for each pulse to save space
        with st.sidebar.expander(f"Pulse {i+1}", expanded=(i==0)):
            enable_pulse = st.checkbox("Enable", value=(i==0), key=f"enable_{i}")
            if enable_pulse:
                pulse_start = st.number_input("Start Time (ms)", value=5.0 + i*40, min_value=0.0, max_value=t_end, key=f"start_{i}")
                pulse_duration = st.number_input("Duration (ms)", value=20.0, min_value=1.0, max_value=t_end-pulse_start, key=f"duration_{i}")
                pulse_end = pulse_start + pulse_duration
                pulse_amplitude = st.number_input("Amplitude (µA/cm²)", value=10.0 if i % 2 == 0 else -5.0, key=f"amp_{i}")
                pulse_noise = st.number_input("Noise (µA/cm²)", value=2.0 if i == 0 else 0.0, min_value=0.0, max_value=10.0, key=f"noise_{i}")
                
                custom_pulses.append({
                    'start': pulse_start,
                    'end': pulse_end,
                    'amplitude': pulse_amplitude,
                    'noise': pulse_noise
                })

# Base current and global noise
base_current = st.sidebar.number_input("Base Current (µA/cm²)", value=0.0, min_value=-20.0, max_value=20.0, step=0.5)
global_noise = st.sidebar.number_input("Global Noise Level (µA/cm²)", value=0.0, min_value=0.0, max_value=5.0, step=0.1)

# Function to run simulation with current parameters
def run_simulation():
    # Create time vector for visualization
    t_vector = np.arange(t_start, t_end + dt, dt)
    
    # Generate current injection pattern
    current_pattern = create_current_injection_pattern(
        t_vector, 
        pulses=custom_pulses,
        base_current=base_current,
        noise_amplitude=global_noise
    )
    
    # Run simulation
    results = hodgkin_huxley_sim(
        t_start=t_start,
        t_end=t_end,
        dt=dt,
        V_initial=initial_voltage,
        gNa=g_na,
        gK=g_k,
        gL=g_l,
        ENa=e_na,
        EK=e_k,
        EL=e_l,
        Cm=cm,
        current_injection=current_pattern
    )
    
    return results

# Preview current injection
if st.sidebar.checkbox("Preview Current Injection", value=True):
    t_preview = np.arange(t_start, t_end + dt, dt)
    current_preview = create_current_injection_pattern(
        t_preview, 
        pulses=custom_pulses,
        base_current=base_current,
        noise_amplitude=global_noise
    )
    
    # Create a quick preview plot in the sidebar
    fig_preview, ax_preview = plt.subplots(figsize=(3, 2))
    ax_preview.plot(t_preview, current_preview, color="#87CEFA")
    ax_preview.set_xlabel("Time (ms)")
    ax_preview.set_ylabel("Current (µA/cm²)")
    ax_preview.set_title("Current Injection Pattern")
    ax_preview.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    st.sidebar.pyplot(fig_preview)

# Run simulation button
if st.sidebar.button("Run Simulation", type="primary"):
    with st.spinner("Running Hodgkin-Huxley simulation..."):
        # Run the simulation
        sim_results = run_simulation()
        
        # Store results in session state
        st.session_state['simulation_results'] = sim_results
        st.session_state['simulation_ran'] = True

# Explanation section
with st.expander("About the Hodgkin-Huxley Model"):
    st.markdown("""
    ## The Hodgkin-Huxley Model
    
    The Hodgkin-Huxley model is the foundational mathematical model that describes how action potentials in neurons are initiated and propagated. It was developed by Alan Hodgkin and Andrew Huxley, who received the Nobel Prize in 1963 for this work.
    
    ### Key Components
    
    1. **Membrane Potential (V)**: The voltage difference across the cell membrane.
    
    2. **Ion Channels**: The model includes three types of channels:
       - Voltage-gated potassium channels (K⁺)
       - Voltage-gated sodium channels (Na⁺)
       - Leak channels (primarily carrying Cl⁻)
    
    3. **Gating Variables**:
       - **n**: Activation of potassium channels
       - **m**: Activation of sodium channels
       - **h**: Inactivation of sodium channels
    
    ### Mathematical Representation
    
    The model is described by the following differential equations:
    
    **Membrane potential**:
    ```
    Cm * dV/dt = I_ext - (gK * n⁴ * (V - EK) + gNa * m³ * h * (V - ENa) + gL * (V - EL))
    ```
    
    **Gating variables**:
    ```
    dn/dt = αn(V) * (1 - n) - βn(V) * n
    dm/dt = αm(V) * (1 - m) - βm(V) * m
    dh/dt = αh(V) * (1 - h) - βh(V) * h
    ```
    
    where α and β are voltage-dependent rate constants that determine the opening and closing of ion channels.
    """)

# Display simulation results if available
if 'simulation_ran' in st.session_state and st.session_state['simulation_ran']:
    display_simulation_results(st.session_state['simulation_results'])
else:
    # Default view before running simulation
    st.info("Adjust the parameters in the sidebar and click 'Run Simulation' to see the results.")
    
    # Show sample image
    st.markdown("""
    ## Example Output
    
    After running the simulation, you'll see detailed visualizations of:
    - Membrane potential over time
    - Gating variables (n, m, h)
    - Ionic currents
    - Comprehensive dashboards
    
    You can customize the stimulus pattern and membrane properties to observe different neuronal behaviors.
    """)

# Footer with information
st.markdown("---")
st.markdown("""
**Neural Signal Analysis Simulator** | Based on the Hodgkin-Huxley model | Created with Streamlit
""")
