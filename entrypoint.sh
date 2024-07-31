#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Start the Streamlit server
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
