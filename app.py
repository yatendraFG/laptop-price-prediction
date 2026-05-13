import streamlit as st
import pickle
import pandas as pd

# -----------------------------------
# Load Trained Model
# -----------------------------------
with open('LR_model.pkl', 'rb') as f:
    model = pickle.load(f)

# -----------------------------------
# Manual Mapping (Actual Brand Names)
# -----------------------------------

brand_mapping = {
    "HP": 0,
    "Lenovo": 1,
    "Asus": 2,
    "Dell": 3,
    "Acer": 4,
    "MSI": 5,
    "Samsung": 6,
    "Apple": 7,
    "Infinix": 8,
    "LG": 9
}

processor_mapping = {
    "Core i3": 0,
    "Core i5": 1,
    "Core i7": 2,
    "Ryzen 3": 3,
    "Ryzen 5": 4,
    "Ryzen 7": 5
}

cpu_mapping = {
    "Intel": 0,
    "AMD": 1
}

ram_type_mapping = {
    "DDR4": 0,
    "DDR5": 1
}

rom_type_mapping = {
    "SSD": 0,
    "HDD": 1
}

gpu_mapping = {
    "Integrated": 0,
    "NVIDIA": 1,
    "AMD Radeon": 2
}

os_mapping = {
    "Windows": 0,
    "Mac": 1,
    "DOS": 2,
    "Linux": 3
}

# -----------------------------------
# Streamlit UI
# -----------------------------------

st.set_page_config(page_title="Laptop Price Prediction")

st.title("💻 Laptop Price Prediction App")

st.write("Enter laptop specifications")

# -----------------------------------
# User Inputs
# -----------------------------------

brand = st.selectbox(
    "Brand",
    list(brand_mapping.keys())
)

spec_rating = st.slider(
    "Specification Rating",
    60.0,
    90.0,
    75.0
)

processor = st.selectbox(
    "Processor",
    list(processor_mapping.keys())
)

CPU = st.selectbox(
    "CPU",
    list(cpu_mapping.keys())
)

Ram = st.selectbox(
    "RAM (GB)",
    [2, 4, 8, 16, 32, 64]
)

Ram_type = st.selectbox(
    "RAM Type",
    list(ram_type_mapping.keys())
)

ROM = st.selectbox(
    "ROM (GB)",
    [256, 512, 1000, 2000]
)

ROM_type = st.selectbox(
    "ROM Type",
    list(rom_type_mapping.keys())
)

GPU = st.selectbox(
    "GPU",
    list(gpu_mapping.keys())
)

display_size = st.slider(
    "Display Size",
    11.0,
    18.0,
    15.6
)

resolution_width = st.selectbox(
    "Resolution Width",
    [1366, 1920, 2560, 3840]
)

resolution_height = st.selectbox(
    "Resolution Height",
    [768, 1080, 1440, 2160]
)

OS = st.selectbox(
    "Operating System",
    list(os_mapping.keys())
)

warranty = st.selectbox(
    "Warranty",
    [0, 1, 2, 3]
)

# -----------------------------------
# Prediction
# -----------------------------------

if st.button("Predict Price 💰"):

    input_data = pd.DataFrame([[
        brand_mapping[brand],
        spec_rating,
        processor_mapping[processor],
        cpu_mapping[CPU],
        Ram,
        ram_type_mapping[Ram_type],
        ROM,
        rom_type_mapping[ROM_type],
        gpu_mapping[GPU],
        display_size,
        resolution_width,
        resolution_height,
        os_mapping[OS],
        warranty
    ]], columns=[
        'brand',
        'spec_rating',
        'processor',
        'CPU',
        'Ram',
        'Ram_type',
        'ROM',
        'ROM_type',
        'GPU',
        'display_size',
        'resolution_width',
        'resolution_height',
        'OS',
        'warranty'
    ])

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Predicted Laptop Price: ₹ {prediction:,.2f}")