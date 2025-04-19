import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd

def filter_data_for_plotting(results, t_min=0):
    """Filter simulation data to start at t_min."""
    idx = results['t'] >= t_min
    filtered_results = {}
    
    for key, value in results.items():
        filtered_results[key] = value[idx]
    
    return filtered_results

def create_membrane_potential_plot(results, fig_width=10, fig_height=6):
    """Create a publication-quality plot of membrane potential."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Plot membrane potential
    ax.plot(results['t'], results['V'], color="#4B0082", linewidth=2)
    
    # Set labels and grid
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Membrane Potential (mV)', fontsize=12)
    ax.set_title('Membrane Potential Over Time', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    
    # Add current injection dashed line at bottom of plot
    ax_twin = ax.twinx()
    ax_twin.plot(results['t'], results['I_ext'], 'r--', alpha=0.7, linewidth=1.5)
    ax_twin.set_ylabel('Current (µA/cm²)', color='r', fontsize=10)
    ax_twin.tick_params(axis='y', colors='r')
    
    # Ensure there's some padding
    plt.tight_layout()
    
    return fig

def create_gating_variables_plot(results, fig_width=10, fig_height=8):
    """Create a plot showing all three gating variables."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Plot the three gating variables
    ax.plot(results['t'], results['n'], color="#FFA500", linewidth=2, label='n (K⁺ activation)')
    ax.plot(results['t'], results['m'], color="blue", linewidth=2, label='m (Na⁺ activation)')
    ax.plot(results['t'], results['h'], color="green", linewidth=2, label='h (Na⁺ inactivation)')
    
    # Set labels and grid
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Gating Variable Value', fontsize=12)
    ax.set_title('Hodgkin-Huxley Gating Variables', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=10)
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    ax.set_ylim(-0.1, 1.1)  # Gating variables are between 0 and 1
    
    plt.tight_layout()
    
    return fig

def create_ionic_currents_plot(results, fig_width=10, fig_height=8):
    """Create a plot showing ionic currents."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Plot the ionic currents
    ax.plot(results['t'], results['IK'], color="#FF4500", linewidth=2, label='IK (K⁺ current)')
    ax.plot(results['t'], results['INa'], color="#1E90FF", linewidth=2, label='INa (Na⁺ current)')
    ax.plot(results['t'], results['IL'], color="#32CD32", linewidth=2, label='IL (Leak current)')
    ax.plot(results['t'], results['I_ion'], color="magenta", linewidth=2, linestyle='--', label='I_ion (Net ionic)')
    
    # Set labels and grid
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Current (µA/cm²)', fontsize=12)
    ax.set_title('Ionic Currents', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='best', fontsize=10)
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    
    plt.tight_layout()
    
    return fig

def create_comprehensive_dashboard(results, fig_width=12, fig_height=16):
    """Create a comprehensive dashboard with all key variables."""
    fig, axes = plt.subplots(4, 1, figsize=(fig_width, fig_height), sharex=True)
    
    # Membrane Potential (top plot)
    axes[0].plot(results['t'], results['V'], color="#4B0082", linewidth=2)
    axes[0].set_ylabel('Membrane\nPotential (mV)', fontsize=12)
    axes[0].set_title('Hodgkin-Huxley Model Simulation Results', fontsize=16)
    axes[0].grid(True, linestyle='--', alpha=0.7)
    
    # External Current (second plot)
    axes[1].plot(results['t'], results['I_ext'], color="#87CEFA", linewidth=2)
    axes[1].set_ylabel('External\nCurrent (µA/cm²)', fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.7)
    
    # Gating Variables (third plot)
    axes[2].plot(results['t'], results['n'], color="#FFA500", linewidth=2, label='n (K⁺ activation)')
    axes[2].plot(results['t'], results['m'], color="blue", linewidth=2, label='m (Na⁺ activation)')
    axes[2].plot(results['t'], results['h'], color="green", linewidth=2, label='h (Na⁺ inactivation)')
    axes[2].set_ylabel('Gating\nVariables', fontsize=12)
    axes[2].grid(True, linestyle='--', alpha=0.7)
    axes[2].legend(loc='upper right', fontsize=10)
    
    # Ionic Currents (bottom plot)
    axes[3].plot(results['t'], results['IK'], color="#FF4500", linewidth=2, label='IK')
    axes[3].plot(results['t'], results['INa'], color="#1E90FF", linewidth=2, label='INa')
    axes[3].plot(results['t'], results['IL'], color="#32CD32", linewidth=2, label='IL')
    axes[3].plot(results['t'], results['I_ion'], color="magenta", linewidth=2, linestyle='--', label='I_ion')
    axes[3].set_xlabel('Time (ms)', fontsize=12)
    axes[3].set_ylabel('Ionic\nCurrents (µA/cm²)', fontsize=12)
    axes[3].grid(True, linestyle='--', alpha=0.7)
    axes[3].legend(loc='upper right', fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def display_simulation_results(results):
    """Display simulation results in Streamlit UI."""
    # Filter data to start plotting at t=0
    plot_results = filter_data_for_plotting(results)
    
    # Create tabs for different plots
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Membrane Potential", "Gating Variables", "Ionic Currents", "Data Table"])
    
    with tab1:
        st.markdown("### Comprehensive Dashboard")
        dashboard_fig = create_comprehensive_dashboard(plot_results)
        st.pyplot(dashboard_fig)
        
    with tab2:
        st.markdown("### Membrane Potential")
        voltage_fig = create_membrane_potential_plot(plot_results)
        st.pyplot(voltage_fig)
        
    with tab3:
        st.markdown("### Gating Variables")
        st.write("n: K⁺ activation | m: Na⁺ activation | h: Na⁺ inactivation")
        gating_fig = create_gating_variables_plot(plot_results)
        st.pyplot(gating_fig)
        
    with tab4:
        st.markdown("### Ionic Currents")
        st.write("IK: K⁺ current | INa: Na⁺ current | IL: Leak current | I_ion: Net current")
        currents_fig = create_ionic_currents_plot(plot_results)
        st.pyplot(currents_fig)
        
    with tab5:
        st.markdown("### Simulation Data")
        # Create a sample of the data for the table
        sample_rate = max(1, len(plot_results['t']) // 1000)  # Show max 1000 rows
        df = pd.DataFrame({
            'Time (ms)': plot_results['t'][::sample_rate],
            'V (mV)': plot_results['V'][::sample_rate],
            'n': plot_results['n'][::sample_rate],
            'm': plot_results['m'][::sample_rate],
            'h': plot_results['h'][::sample_rate],
            'I_ext (µA/cm²)': plot_results['I_ext'][::sample_rate],
            'IK (µA/cm²)': plot_results['IK'][::sample_rate],
            'INa (µA/cm²)': plot_results['INa'][::sample_rate],
            'IL (µA/cm²)': plot_results['IL'][::sample_rate]
        })
        st.dataframe(df)
        
        # Option to download the full data
        csv = pd.DataFrame({
            'Time (ms)': plot_results['t'],
            'V (mV)': plot_results['V'],
            'n': plot_results['n'],
            'm': plot_results['m'],
            'h': plot_results['h'],
            'I_ext (µA/cm²)': plot_results['I_ext'],
            'IK (µA/cm²)': plot_results['IK'],
            'INa (µA/cm²)': plot_results['INa'],
            'IL (µA/cm²)': plot_results['IL'],
            'I_ion (µA/cm²)': plot_results['I_ion']
        }).to_csv(index=False)
        
        st.download_button(
            label="Download Complete Data as CSV",
            data=csv,
            file_name="hodgkin_huxley_simulation_results.csv",
            mime="text/csv"
        )
