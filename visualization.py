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
    
    # Plot membrane potential with purple color (for voltage)
    ax.plot(results['t'], results['V'], color="#7066ff", linewidth=2.5)
    
    # Set labels and grid with custom colors
    ax.set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    ax.set_ylabel('Membrane Potential (mV)', fontsize=12, color='#c5f8ff')
    ax.set_title('Membrane Potential Over Time', fontsize=14, color='#00ffee')
    ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Set axis limits
    ax.set_xlim(min(results['t']), max(results['t']))
    
    # Add current injection dashed line at bottom of plot (current in blue)
    ax_twin = ax.twinx()
    ax_twin.plot(results['t'], results['I_ext'], color='#00c8ff', linestyle='--', alpha=0.8, linewidth=1.5)
    ax_twin.set_ylabel('Current (µA/cm²)', color='#00c8ff', fontsize=10)
    ax_twin.tick_params(axis='y', colors='#00c8ff')
    for spine in ax_twin.spines.values():
        spine.set_color('#333333')
    
    # Ensure there's some padding
    plt.tight_layout()
    
    return fig

def create_gating_variables_plot(results, fig_width=10, fig_height=12):
    """Create a plot showing all three gating variables in separate subplots."""
    # Create figure with 3 subplots (one for each gating variable)
    fig, axes = plt.subplots(3, 1, figsize=(fig_width, fig_height), sharex=True, facecolor='#111111')
    
    # Define complementary green colors for gating variables
    green_colors = ["#00ffaa", "#00cc99", "#009977"]
    
    # Set dark background style for all subplots
    for i, ax in enumerate(axes):
        ax.set_facecolor('#111111')
        for spine in ax.spines.values():
            spine.set_color('#333333')
        ax.tick_params(colors='#c5f8ff', which='both')
        ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
        ax.set_xlim(min(results['t']), max(results['t']))
        ax.set_ylim(-0.1, 1.1)  # Gating variables are between 0 and 1
    
    # n: Potassium activation
    axes[0].plot(results['t'], results['n'], color=green_colors[0], linewidth=2.5)
    axes[0].set_ylabel('n', fontsize=12, color='#c5f8ff')
    axes[0].set_title('Potassium Activation (n)', fontsize=14, color='#00ffee')
    
    # m: Sodium activation
    axes[1].plot(results['t'], results['m'], color=green_colors[1], linewidth=2.5)
    axes[1].set_ylabel('m', fontsize=12, color='#c5f8ff')
    axes[1].set_title('Sodium Activation (m)', fontsize=14, color='#00ffee')
    
    # h: Sodium inactivation
    axes[2].plot(results['t'], results['h'], color=green_colors[2], linewidth=2.5)
    axes[2].set_ylabel('h', fontsize=12, color='#c5f8ff')
    axes[2].set_title('Sodium Inactivation (h)', fontsize=14, color='#00ffee')
    
    # Set common x-axis label
    axes[2].set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    
    # Overall title
    fig.suptitle('Hodgkin-Huxley Gating Variables', fontsize=16, color='#00ffee')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Make room for suptitle
    
    return fig

def create_ionic_currents_plot(results, fig_width=10, fig_height=10):
    """Create a plot showing ionic currents."""
    # Split into individual currents and total current
    fig, axes = plt.subplots(4, 1, figsize=(fig_width, fig_height), sharex=True, facecolor='#111111')
    
    # Define blue colors for ionic currents
    blue_colors = ["#00c8ff", "#14a5ff", "#00f5db", "#00a5ff"]
    
    # Set dark background style for all subplots
    for ax in axes:
        ax.set_facecolor('#111111')
        for spine in ax.spines.values():
            spine.set_color('#333333')
        ax.tick_params(colors='#c5f8ff', which='both')
        ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
        ax.set_xlim(min(results['t']), max(results['t']))
    
    # Potassium Current
    axes[0].plot(results['t'], results['IK'], color=blue_colors[0], linewidth=2.5)
    axes[0].set_ylabel('IK\n(K⁺ current)', fontsize=12, color='#c5f8ff')
    axes[0].set_title('Potassium Current', fontsize=14, color='#00ffee')
    
    # Sodium Current
    axes[1].plot(results['t'], results['INa'], color=blue_colors[1], linewidth=2.5)
    axes[1].set_ylabel('INa\n(Na⁺ current)', fontsize=12, color='#c5f8ff')
    axes[1].set_title('Sodium Current', fontsize=14, color='#00ffee')
    
    # Leak Current
    axes[2].plot(results['t'], results['IL'], color=blue_colors[2], linewidth=2.5)
    axes[2].set_ylabel('IL\n(Leak current)', fontsize=12, color='#c5f8ff')
    axes[2].set_title('Leak Current', fontsize=14, color='#00ffee')
    
    # Net Ionic Current
    axes[3].plot(results['t'], results['I_ion'], color=blue_colors[3], linewidth=2.5)
    axes[3].set_ylabel('I_ion\n(Net current)', fontsize=12, color='#c5f8ff')
    axes[3].set_title('Net Ionic Current', fontsize=14, color='#00ffee')
    axes[3].set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    
    # Overall title
    fig.suptitle('Ionic Currents (µA/cm²)', fontsize=16, color='#00ffee')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)  # Make room for suptitle
    
    return fig

def create_comprehensive_dashboard(results, fig_width=12, fig_height=16):
    """Create a comprehensive dashboard with all key variables."""
    fig, axes = plt.subplots(5, 1, figsize=(fig_width, fig_height), sharex=True, facecolor='#111111')
    
    # Set dark background style for all subplots
    for ax in axes:
        ax.set_facecolor('#111111')
        for spine in ax.spines.values():
            spine.set_color('#333333')
        ax.tick_params(colors='#c5f8ff', which='both')
        ax.grid(True, linestyle='--', alpha=0.3, color='#444444')
    
    # Membrane Potential (top plot) - purple for voltage
    axes[0].plot(results['t'], results['V'], color="#7066ff", linewidth=2.5)
    axes[0].set_ylabel('Membrane\nPotential (mV)', fontsize=12, color='#c5f8ff')
    axes[0].set_title('Hodgkin-Huxley Model Simulation Results', fontsize=16, color='#00ffee')
    
    # External Current (second plot) - blue for current
    axes[1].plot(results['t'], results['I_ext'], color="#00c8ff", linewidth=2.5)
    axes[1].set_ylabel('External\nCurrent (µA/cm²)', fontsize=12, color='#c5f8ff')
    
    # Individual Gating Variables (green theme)
    green_colors = ["#00ffaa", "#00cc99", "#009977"]
    
    # n: Potassium activation
    axes[2].plot(results['t'], results['n'], color=green_colors[0], linewidth=2.5)
    axes[2].set_ylabel('n\n(K⁺ activation)', fontsize=12, color='#c5f8ff')
    
    # m: Sodium activation
    axes[3].plot(results['t'], results['m'], color=green_colors[1], linewidth=2.5)
    axes[3].set_ylabel('m\n(Na⁺ activation)', fontsize=12, color='#c5f8ff')
    
    # h: Sodium inactivation
    axes[4].plot(results['t'], results['h'], color=green_colors[2], linewidth=2.5)
    axes[4].set_ylabel('h\n(Na⁺ inactivation)', fontsize=12, color='#c5f8ff')
    axes[4].set_xlabel('Time (ms)', fontsize=12, color='#c5f8ff')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def display_simulation_results(results):
    """Display simulation results in Streamlit UI."""
    # Filter data to start plotting at t=0
    plot_results = filter_data_for_plotting(results)
    
    # Apply custom CSS for tabs to match gradient
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        white-space: pre-wrap;
        border-radius: 10px;
        color: white;
        font-family: 'Aclonica', sans-serif;
        padding: 0.5rem 1rem;
        background-image: linear-gradient(to right bottom, #00c8ff, #14a5ff, #7066ff, #5e17eb);
        background-size: 300% 100%;
    }
    
    .stTabs [aria-selected="true"] {
        background-position: 100% 0;
        filter: brightness(1.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create tabs for different plots (removed Ionic Currents)
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Membrane Potential", "Gating Variables"])
    
    with tab1:
        st.markdown("""<h3 style="background-image: linear-gradient(to right bottom, #00c8ff, #14a5ff, #7066ff, #5e17eb); 
                    -webkit-background-clip: text; background-clip: text; color: transparent;">Comprehensive Dashboard</h3>""", 
                    unsafe_allow_html=True)
        dashboard_fig = create_comprehensive_dashboard(plot_results)
        st.pyplot(dashboard_fig)
        
    with tab2:
        st.markdown("""<h3 style="background-image: linear-gradient(to right bottom, #00c8ff, #14a5ff, #7066ff, #5e17eb); 
                    -webkit-background-clip: text; background-clip: text; color: transparent;">Membrane Potential</h3>""", 
                    unsafe_allow_html=True)
        voltage_fig = create_membrane_potential_plot(plot_results)
        st.pyplot(voltage_fig)
        
    with tab3:
        st.markdown("""<h3 style="background-image: linear-gradient(to right bottom, #00c8ff, #14a5ff, #7066ff, #5e17eb); 
                    -webkit-background-clip: text; background-clip: text; color: transparent;">Gating Variables</h3>""", 
                    unsafe_allow_html=True)
        st.markdown("""<p style="color: #c5f8ff;">n: K⁺ activation | m: Na⁺ activation | h: Na⁺ inactivation</p>""", 
                   unsafe_allow_html=True)
        gating_fig = create_gating_variables_plot(plot_results)
        st.pyplot(gating_fig)
    
    # Option to download the full data - now available under all tabs
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
