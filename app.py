import streamlit as st
import pickle
import pandas as pd

# Load the trained model
with open('LR_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the dictionary of label encoders
with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f) # Load the dictionary

st.title('Laptop Price Prediction App')
st.write('Enter the details of the laptop to predict its price.')

# Input fields for features (adjust based on your 'X' DataFrame columns)
# Use specific encoders for each column

# Create a dummy DataFrame to get unique values for inverse_transform, 
# as the original `df` might not be available when running the Streamlit app directly.
# This assumes the label_encoders were fitted on the complete original df.
# For a robust solution, you'd typically save the inverse_transform mappings or use a fixed list of options.
# For now, we'll recreate a temporary df to get the original categories.

# NOTE: In a real deployment, you would not rely on 'df' being in scope. 
# Instead, you would load the unique categories that were used during fitting
# and pass them to the selectbox. For this example, we'll assume 'df' is available for options.
# In a real Streamlit app, you might hardcode the options or load them from a saved file.

# Example of how to get the options for brand, if df is not globally available:
# brand_options = label_encoders['brand'].inverse_transform(range(len(label_encoders['brand'].classes_)))

# Using existing `df` from the notebook's kernel state for simplicity in Colab context.
# In a standalone app.py, you would need to load `df` or save/load the unique categories separately.

brand_le = label_encoders['brand']
brand = st.selectbox('Brand', brand_le.inverse_transform(range(len(brand_le.classes_))))

spec_rating = st.slider('Specification Rating', 60.0, 90.0, 75.0)

processor_le = label_encoders['processor']
processor = st.selectbox('Processor', processor_le.inverse_transform(range(len(processor_le.classes_))))

cpu_le = label_encoders['CPU']
CPU = st.selectbox('CPU', cpu_le.inverse_transform(range(len(cpu_le.classes_))))

Ram = st.selectbox('RAM (GB)', [2, 4, 8, 12, 16, 32, 64])

ram_type_le = label_encoders['Ram_type']
Ram_type = st.selectbox('RAM Type', ram_type_le.inverse_transform(range(len(ram_type_le.classes_))))

ROM = st.selectbox('ROM (GB)', [256, 512, 1000, 2000])

rom_type_le = label_encoders['ROM_type']
ROM_type = st.selectbox('ROM Type', rom_type_le.inverse_transform(range(len(rom_type_le.classes_))))

gpu_le = label_encoders['GPU']
GPU = st.selectbox('GPU', gpu_le.inverse_transform(range(len(gpu_le.classes_))))

display_size = st.slider('Display Size (inches)', 11.0, 18.0, 15.6)
resolution_width = st.slider('Resolution Width', 1080, 3840, 1920)
resolution_height = st.slider('Resolution Height', 768, 3456, 1080)

os_le = label_encoders['OS']
OS = st.selectbox('Operating System', os_le.inverse_transform(range(len(os_le.classes_))))

warranty = st.selectbox('Warranty (Years)', [0, 1, 2, 3])

if st.button('Predict Price'):
    # Encode categorical inputs using the loaded LabelEncoder
    encoded_brand = brand_le.transform([brand])[0]
    encoded_processor = processor_le.transform([processor])[0]
    encoded_CPU = cpu_le.transform([CPU])[0]
    encoded_Ram_type = ram_type_le.transform([Ram_type])[0]
    encoded_ROM_type = rom_type_le.transform([ROM_type])[0]
    encoded_GPU = gpu_le.transform([GPU])[0]
    encoded_OS = os_le.transform([OS])[0]

    # Create a DataFrame for prediction
    input_data = pd.DataFrame([[
        encoded_brand, spec_rating, encoded_processor, encoded_CPU, Ram, 
        encoded_Ram_type, ROM, encoded_ROM_type, encoded_GPU, display_size, 
        resolution_width, resolution_height, encoded_OS, warranty
    ]],
    columns=['brand', 'spec_rating', 'processor', 'CPU', 'Ram', 'Ram_type', 'ROM', 
             'ROM_type', 'GPU', 'display_size', 'resolution_width', 
             'resolution_height', 'OS', 'warranty'])

    # Make prediction
    prediction = model.predict(input_data)[0]
    st.success(f'Predicted Laptop Price: ₹{prediction:,.2f}')
