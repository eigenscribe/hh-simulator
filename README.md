# Neural Signal Analysis Simulator

This application provides an interactive simulation of neural signal dynamics using the classic Hodgkin-Huxley model. It allows users to explore how neurons generate and propagate action potentials under different conditions.

## Features

- Interactive visualization of the Hodgkin-Huxley model
- Customizable simulation parameters
- Analysis of membrane potential, ionic currents, and gating variables
- Multiple current injection patterns
- High-quality, publication-ready plots
- Downloadable simulation data

## Quick Start

1. Clone this repository
2. Install the required packages:
   ```
   pip install streamlit numpy matplotlib pandas
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```

## The Hodgkin-Huxley Model

The Hodgkin-Huxley model is a set of nonlinear differential equations that describes how action potentials in neurons are initiated and propagated. It models the electrical characteristics of excitable cells such as neurons and muscle cells.

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
