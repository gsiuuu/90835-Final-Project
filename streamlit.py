# import streamlit as st
# import json
# import subprocess
# import os

# # Initialize session state if needed
# if "json_output" not in st.session_state:
#     st.session_state["json_output"] = None
# if "letter_text" not in st.session_state:
#     st.session_state["letter_text"] = None

# st.set_page_config(layout="centered", page_title="Patient Discharge Summary Generator")
# st.title("Patient Discharge Summary Generator")

# # 1. File Uploader for Patient Data (JSON)
# uploaded_file = st.file_uploader("Upload patient data (JSON)", type="json")
# if uploaded_file is not None:
#     with open("input_patient_data.json", "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     st.success("Uploaded patient data successfully saved as 'input_patient_data.json'.")

# # 2. Additional prompt text area
# additional_prompt = st.text_area(
#     "Enter additional prompt (optional):", 
#     help="Any text entered here will be added to the prompt for the LLM and saved to additional_prompt.txt."
# )

# # 3. Run External Python Script and Display Output
# if st.button("Generate Summary"):
#     # Handle additional prompt: save file if text provided, else remove any existing file.
#     if additional_prompt.strip():
#         try:
#             with open("additional_prompt.txt", "w", encoding="utf-8") as prompt_file:
#                 prompt_file.write(additional_prompt)
#             st.info("Additional prompt saved as 'additional_prompt.txt'.")
#         except Exception as e:
#             st.error(f"Failed to write additional prompt to file: {e}")
#     else:
#         # Remove the file if exists so that an empty prompt isn't used
#         if os.path.exists("additional_prompt.txt"):
#             os.remove("additional_prompt.txt")

#     # Run the external script (adjust the filename if necessary)
#     try:
#         subprocess.run(["python", "starter_code.py"], check=True)
#     except subprocess.CalledProcessError as e:
#         st.error("An error occurred while generating the summary.")
#         st.error(f"Error details: {e}")
#     else:
#         # Read and store the JSON file output in session state
#         if os.path.exists("parsed_json.json"):
#             try:
#                 with open("parsed_json.json", "r", encoding="utf-8") as json_file:
#                     loaded = json_file.read()
#                     try:
#                         # Try to load the JSON directly from string
#                         parsed = json.loads(loaded)
#                     except json.JSONDecodeError:
#                         # If that fails, assume it's already a dictionary-like string
#                         parsed = loaded
#                     st.session_state["json_output"] = parsed
#             except Exception as e:
#                 st.error(f"Failed to load patient data output: {e}")
#         else:
#             st.error("The parsed patient data was not found.")

#         # Read and store the discharge letter text file in session state
#         if os.path.exists("letter.txt"):
#             try:
#                 with open("letter.txt", "r", encoding="utf-8") as txt_file:
#                     summary_text = txt_file.read()
#                 summary_text = summary_text.replace("\\n", "\n")
#                 st.session_state["letter_text"] = summary_text
#             except Exception as e:
#                 st.error(f"Failed to read the discharge letter file: {e}")
#         else:
#             st.error("The discharge letter was not found.")

# # --------------------------
# # Display custom-formatted data (wrapped in a checkbox)
# # --------------------------
# if st.session_state["json_output"] is not None:
#     show_data = st.checkbox("Show Parsed Patient Data")
#     if show_data:
#         # Ensure we have a dictionary for patient_info
#         patient_info = st.session_state["json_output"]
#         if isinstance(patient_info, str):
#             try:
#                 patient_info = json.loads(patient_info)
#             except Exception as e:
#                 st.error("Failed to parse JSON output into a dictionary.")
#                 patient_info = {}

#         # Helper function to safely get a field (with fallback)
#         def get_value(key):
#             return patient_info.get(key, "N/A")
        
#         # Extract fields from patient_info
#         patient_id = get_value("Patient ID")
#         name = get_value("Name")
#         dob = get_value("Date of Birth")
#         admission_date = get_value("Admission Date")
#         discharge_date = get_value("Discharge Date")
#         diagnosis = get_value("Diagnosis")
        
#         # Handle Medications: It might be a list of strings or a list of dictionaries
#         meds = patient_info.get("Medications", [])
#         if isinstance(meds, list):
#             meds_str = ", ".join(
#                 m if isinstance(m, str) else 
#                 (str(list(m.keys())[0]) if isinstance(m, dict) and m else str(m))
#                 for m in meds
#             )
#         else:
#             meds_str = str(meds)
        
#         st.subheader("Parsed Patient Data")
#         st.write(f"Patient ID: {patient_id}")
#         st.write(f"Name: {name}")
#         st.write(f"Date of Birth: {dob}")
#         st.write(f"Admission Date: {admission_date}")
#         st.write(f"Discharge Date: {discharge_date}")
#         st.write(f"Diagnosis: {diagnosis}")
#         st.write(f"Medications: {meds_str}")

# # --------------------------
# # Display discharge letter
# # --------------------------
# if st.session_state["letter_text"] is not None:
#     st.subheader("Generated Discharge Letter:")
#     st.markdown(st.session_state["letter_text"])



import streamlit as st
import json
import subprocess
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize session state if needed
if "json_output" not in st.session_state:
    st.session_state["json_output"] = None
if "letter_text" not in st.session_state:
    st.session_state["letter_text"] = None

st.set_page_config(layout="centered", page_title="Patient Discharge Summary Generator")
st.title("Patient Discharge Summary Generator")

logging.info("Streamlit app initialized")

# 1. File Uploader for Patient Data (JSON)
uploaded_file = st.file_uploader("Upload patient data (JSON)", type="json")
if uploaded_file is not None:
    with open("input_patient_data.json", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Uploaded patient data successfully saved as 'input_patient_data.json'.")
    logging.info("Patient data uploaded and saved successfully")

# 2. Additional prompt text area
additional_prompt = st.text_area(
    "Enter additional prompt (optional):", 
    help="Any text entered here will be added to the prompt for the LLM and saved to additional_prompt.txt."
)

# 3. Run External Python Script and Display Output
if st.button("Generate Summary"):
    logging.info("Generate Summary button clicked")
    
    # Handle additional prompt: save file if text provided, else remove any existing file.
    if additional_prompt.strip():
        try:
            with open("additional_prompt.txt", "w", encoding="utf-8") as prompt_file:
                prompt_file.write(additional_prompt)
            st.info("Additional prompt saved as 'additional_prompt.txt'.")
            logging.info("Additional prompt saved successfully")
        except Exception as e:
            st.error(f"Failed to write additional prompt to file: {e}")
            logging.error(f"Failed to write additional prompt: {e}")
    else:
        # Remove the file if exists so that an empty prompt isn't used
        if os.path.exists("additional_prompt.txt"):
            os.remove("additional_prompt.txt")
            logging.info("Existing additional prompt file removed")
    
    # Run the external script (adjust the filename if necessary)
    try:
        logging.info("Running external script 'starter_code.py'")
        subprocess.run(["python3", "starter_code.py"], check=True)
        logging.info("External script 'starter_code.py' executed successfully")
    except subprocess.CalledProcessError as e:
        st.error("An error occurred while generating the summary.")
        st.error(f"Error details: {e}")
        logging.error(f"Error while running the script: {e}")

    # Read and store the JSON file output in session state
    if os.path.exists("parsed_json.json"):
        try:
            with open("parsed_json.json", "r", encoding="utf-8") as json_file:
                loaded = json_file.read()
                try:
                    # Try to load the JSON directly from string
                    parsed = json.loads(loaded)
                    logging.info("Parsed patient data successfully from 'parsed_json.json'")
                except json.JSONDecodeError:
                    # If that fails, assume it's already a dictionary-like string
                    parsed = loaded
                    logging.warning("Failed to parse JSON, assuming raw string format")
                st.session_state["json_output"] = parsed
        except Exception as e:
            st.error(f"Failed to load patient data output: {e}")
            logging.error(f"Error loading parsed patient data: {e}")
    else:
        st.error("The parsed patient data was not found.")
        logging.error("Parsed patient data file 'parsed_json.json' not found.")

    # Read and store the discharge letter text file in session state
    if os.path.exists("letter.txt"):
        try:
            with open("letter.txt", "r", encoding="utf-8") as txt_file:
                summary_text = txt_file.read()
            summary_text = summary_text.replace("\\n", "\n")
            st.session_state["letter_text"] = summary_text
            logging.info("Discharge letter text successfully loaded from 'letter.txt'")
        except Exception as e:
            st.error(f"Failed to read the discharge letter file: {e}")
            logging.error(f"Error reading discharge letter file: {e}")
    else:
        st.error("The discharge letter was not found.")
        logging.error("Discharge letter file 'letter.txt' not found.")

# --------------------------
# Display custom-formatted data (wrapped in a checkbox)
# --------------------------
if st.session_state["json_output"] is not None:
    show_data = st.checkbox("Show Parsed Patient Data")
    if show_data:
        # Ensure we have a dictionary for patient_info
        patient_info = st.session_state["json_output"]
        if isinstance(patient_info, str):
            try:
                patient_info = json.loads(patient_info)
                logging.info("Parsed patient data from string format")
            except Exception as e:
                st.error("Failed to parse JSON output into a dictionary.")
                logging.error(f"Error parsing patient data string: {e}")
                patient_info = {}

        # Helper function to safely get a field (with fallback)
        def get_value(key):
            return patient_info.get(key, "N/A")
        
        # Extract fields from patient_info
        patient_id = get_value("Patient ID")
        name = get_value("Name")
        dob = get_value("Date of Birth")
        admission_date = get_value("Admission Date")
        discharge_date = get_value("Discharge Date")
        diagnosis = get_value("Diagnosis")
        
        # Handle Medications: It might be a list of strings or a list of dictionaries
        meds = patient_info.get("Medications", [])
        if isinstance(meds, list):
            meds_str = ", ".join(
                m if isinstance(m, str) else 
                (str(list(m.keys())[0]) if isinstance(m, dict) and m else str(m))
                for m in meds
            )
        else:
            meds_str = str(meds)

        st.subheader("Parsed Patient Data")
        st.write(f"Patient ID: {patient_id}")
        st.write(f"Name: {name}")
        st.write(f"Date of Birth: {dob}")
        st.write(f"Admission Date: {admission_date}")
        st.write(f"Discharge Date: {discharge_date}")
        st.write(f"Diagnosis: {diagnosis}")
        st.write(f"Medications: {meds_str}")
        logging.info("Displayed parsed patient data")

# --------------------------
# Display discharge letter
# --------------------------
if st.session_state["letter_text"] is not None:
    st.subheader("Generated Discharge Letter:")
    st.markdown(st.session_state["letter_text"])
    logging.info("Displayed discharge letter")
