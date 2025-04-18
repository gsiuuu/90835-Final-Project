# 90835-Final-Project

# Patient Discharge Summary Generator

In modern healthcare settings, preparing clear and accurate discharge summaries can be time‑consuming for busy clinicians. This project leverages OpenAI’s GPT‑3.5 API alongside a Streamlit web interface to automate the creation of both structured patient data exports and patient discharge letters. By feeding a simple JSON record of a patient’s information into the system, users receive back a validated JSON object and a summary discharge letter for the patient.

Instructions to Set Up the Project:

1. **Clone the repository** to your local machine and navigate into the project folder.
2. **Install dependencies** using `pip install -r requirements.txt`, which includes Streamlit and the OpenAI Python client.
3. **Configure your OpenAI credentials** by creating a `credentials.json` file in the root directory with your API key under the property `openai_api_key`.
4. **Run the application** via `streamlit run app.py` and open the provided URL in your browser.

The structure of the app is as follows:

- **Upload** a JSON file containing fields such as patient name, dates, diagnosis, and medications.  
- **(Optional)** Add any extra instructions or context in the prompt box to guide the AI’s tone, style, or focus.  
- **Generate** your summary by clicking on the "Generate Summary" button.
- **View patient data** by clicking the  checkbox to show patient information.
- **Review the letter** to understand important discharge information for the patient.

