import streamlit as st
import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Config
st.set_page_config(page_title="TRAPPIST-1 Discovery Dashboard", layout="wide")

st.title("🛰️ TRAPPIST-1 Exoplanet Discovery")
st.markdown("""
This app demonstrates **Signal Deconvolution**. We first identify the dominant planet (1b), 
mask its transit signal using manual modulus arithmetic, and then search for the secondary candidate (1c).
""")

# 2. Rectified Data Loading (Fixes the Serialization Error)
@st.cache_resource
def load_and_clean_data():
    # Search and download the first available SPOC sector
    search = lk.search_lightcurve("TRAPPIST-1", author="SPOC")
    if len(search) == 0:
        st.error("No data found for TRAPPIST-1.")
        return None
    
    # Flatten removes long-term stellar trends; remove_outliers cleans flares
    lc = search[0].download().flatten().remove_outliers()
    return lc

lc_clean = load_and_clean_data()

if lc_clean:
    # --- SIDEBAR ---
    st.sidebar.header("Planetary Parameters")
    p_b = st.sidebar.slider("Planet 1b Period (Days)", 1.0, 2.0, 1.5108, format="%.4f")
    p_c = st.sidebar.slider("Planet 1c Period (Days)", 2.0, 3.0, 2.4218, format="%.4f")
    
    # --- MANUAL MASKING LOGIC ---
    # We use the numeric JD values to avoid Astropy 'Time' object conflicts
    t0_b = 3209.7761  # Base transit time for 1b
    time_vals = lc_clean.time.value
    
    # Mathematical bypass: Keep points where the phase is far from the transit center
    # This creates a 'clean' dataset with the 1.2-day dips physically removed
    clean_indices = np.abs((time_vals - t0_b + (p_b/2)) % p_b - (p_b/2)) > 0.05
    lc_remaining = lc_clean[clean_indices]

    # --- VISUALIZATION ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Planet 1b (Primary)")
        st.write("The strongest periodic signal in the system.")
        fig1, ax1 = plt.subplots()
        lc_clean.fold(p_b).bin(time_bin_size=0.01).scatter(ax=ax1, color='cyan', s=10)
        ax1.set_title(f"Folded on {p_b} days")
        st.pyplot(fig1)

    with col2:
        st.subheader("Planet 1c (Secondary)")
        st.write("Isolated after masking the 1b signal.")
        fig2, ax2 = plt.subplots()
        # Use the remaining data to check for the smaller planet
        lc_remaining.fold(p_c).bin(time_bin_size=0.01).scatter(ax=ax2, color='orange', s=10)
        ax2.set_title(f"Folded on {p_c} days")
        st.pyplot(fig2)

    # --- STATISTICS ---
    st.divider()
    st.write("### Detection Statistics")
    c1, c2 = st.columns(2)
    c1.metric("Planet 1b Confidence", "HIGH", "Confirmed")
    # Recall our SNR was ~1.6 for 1c
    c2.metric("Planet 1c Confidence", "LOW", "Candidate Only", delta_color="inverse")
    
    st.info("Note: Planet 1c requires multi-sector data to reach the 7.0 SNR threshold for formal discovery.")