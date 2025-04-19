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
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='#111111')
    
    # Set dark background style
    ax.set_facecolor('#111111')
    for spine in ax.spines.values():
        spine.set_color('#333333')
    ax.tick_params(colors='#c5f8ff', which='both')
    
    # Plot membrane potential with gradient-matching color
    ax.plot(results['t'], results['V'], color="#00c8ff", linewidth=2.5)
    
    # Set labels and grid with custom colors
    ax.set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    ax.set_ylabel('Membrane Potential (mV)', fontsize=12, color='#c5f8ff')
    ax.set_title('Membrane Potential Over Time', fontsize=14, color='#00ffee')
    ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    
    # Add current injection dashed line at bottom of plot
    ax_twin = ax.twinx()
    ax_twin.plot(results['t'], results['I_ext'], color='#7066ff', linestyle='--', alpha=0.8, linewidth=1.5)
    ax_twin.set_ylabel('Current (µA/cm²)', color='#7066ff', fontsize=10)
    ax_twin.tick_params(axis='y', colors='#7066ff')
    for spine in ax_twin.spines.values():
        spine.set_color('#333333')
    
    # Ensure there's some padding
    plt.tight_layout()
    
    return fig

def create_gating_variables_plot(results, fig_width=10, fig_height=8):
    """Create a plot showing all three gating variables."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='#111111')
    
    # Set dark background style
    ax.set_facecolor('#111111')
    for spine in ax.spines.values():
        spine.set_color('#333333')
    ax.tick_params(colors='#c5f8ff', which='both')
    
    # Plot the three gating variables with blue-purple themed colors
    ax.plot(results['t'], results['n'], color="#00c8ff", linewidth=2.5, label='n (K⁺ activation)')
    ax.plot(results['t'], results['m'], color="#14a5ff", linewidth=2.5, label='m (Na⁺ activation)')
    ax.plot(results['t'], results['h'], color="#7066ff", linewidth=2.5, label='h (Na⁺ inactivation)')
    
    # Set labels and grid with custom colors
    ax.set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    ax.set_ylabel('Gating Variable Value', fontsize=12, color='#c5f8ff')
    ax.set_title('Hodgkin-Huxley Gating Variables', fontsize=14, color='#00ffee')
    ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Style the legend
    legend = ax.legend(loc='best', fontsize=10)
    legend.get_frame().set_facecolor('#222222')
    legend.get_frame().set_edgecolor('#444444')
    for text in legend.get_texts():
        text.set_color('#c5f8ff')
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    ax.set_ylim(-0.1, 1.1)  # Gating variables are between 0 and 1
    
    plt.tight_layout()
    
    return fig

def create_ionic_currents_plot(results, fig_width=10, fig_height=8):
    """Create a plot showing ionic currents."""
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='#111111')
    
    # Set dark background style
    ax.set_facecolor('#111111')
    for spine in ax.spines.values():
        spine.set_color('#333333')
    ax.tick_params(colors='#c5f8ff', which='both')
    
    # Plot the ionic currents with blue-purple gradient theme
    ax.plot(results['t'], results['IK'], color="#00c8ff", linewidth=2.5, label='IK (K⁺ current)')
    ax.plot(results['t'], results['INa'], color="#14a5ff", linewidth=2.5, label='INa (Na⁺ current)')
    ax.plot(results['t'], results['IL'], color="#00f5db", linewidth=2.5, label='IL (Leak current)')
    ax.plot(results['t'], results['I_ion'], color="#7066ff", linewidth=2.5, linestyle='--', label='I_ion (Net ionic)')
    
    # Set labels and grid with custom colors
    ax.set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    ax.set_ylabel('Current (µA/cm²)', fontsize=12, color='#c5f8ff')
    ax.set_title('Ionic Currents', fontsize=14, color='#00ffee')
    ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Style the legend
    legend = ax.legend(loc='best', fontsize=10)
    legend.get_frame().set_facecolor('#222222')
    legend.get_frame().set_edgecolor('#444444')
    for text in legend.get_texts():
        text.set_color('#c5f8ff')
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    
    plt.tight_layout()
    
    return fig

def create_comprehensive_dashboard(results, fig_width=12, fig_height=16):
    """Create a comprehensive dashboard with all key variables."""
    fig, axes = plt.subplots(4, 1, figsize=(fig_width, fig_height), sharex=True, facecolor='#111111')
    
    # Set dark background style for all subplots
    for ax in axes:
        ax.set_facecolor('#111111')
        for spine in ax.spines.values():
            spine.set_color('#333333')
        ax.tick_params(colors='#c5f8ff', which='both')
        ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Membrane Potential (top plot)
    axes[0].plot(results['t'], results['V'], color="#00c8ff", linewidth=2.5)
    axes[0].set_ylabel('Membrane\nPotential (mV)', fontsize=12, color='#c5f8ff')
    axes[0].set_title('Hodgkin-Huxley Model Simulation Results', fontsize=16, color='#00ffee')
    
    # External Current (second plot)
    axes[1].plot(results['t'], results['I_ext'], color="#7066ff", linewidth=2.5)
    axes[1].set_ylabel('External\nCurrent (µA/cm²)', fontsize=12, color='#c5f8ff')
    
    # Gating Variables (third plot)
    axes[2].plot(results['t'], results['n'], color="#00c8ff", linewidth=2.5, label='n (K⁺ activation)')
    axes[2].plot(results['t'], results['m'], color="#14a5ff", linewidth=2.5, label='m (Na⁺ activation)')
    axes[2].plot(results['t'], results['h'], color="#7066ff", linewidth=2.5, label='h (Na⁺ inactivation)')
    axes[2].set_ylabel('Gating\nVariables', fontsize=12, color='#c5f8ff')
    
    # Style the legend for gating variables
    legend2 = axes[2].legend(loc='upper right', fontsize=10)
    legend2.get_frame().set_facecolor('#222222')
    legend2.get_frame().set_edgecolor('#444444')
    for text in legend2.get_texts():
        text.set_color('#c5f8ff')
    
    # Ionic Currents (bottom plot)
    axes[3].plot(results['t'], results['IK'], color="#00c8ff", linewidth=2.5, label='IK')
    axes[3].plot(results['t'], results['INa'], color="#14a5ff", linewidth=2.5, label='INa')
    axes[3].plot(results['t'], results['IL'], color="#00f5db", linewidth=2.5, label='IL')
    axes[3].plot(results['t'], results['I_ion'], color="#7066ff", linewidth=2.5, linestyle='--', label='I_ion')
    axes[3].set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    axes[3].set_ylabel('Ionic\nCurrents (µA/cm²)', fontsize=12, color='#c5f8ff')
    
    # Style the legend for ionic currents
    legend3 = axes[3].legend(loc='upper right', fontsize=10)
    legend3.get_frame().set_facecolor('#222222')
    legend3.get_frame().set_edgecolor('#444444')
    for text in legend3.get_texts():
        text.set_color('#c5f8ff')
    
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
