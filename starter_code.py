import openai
from openai import OpenAI
import json
from pathlib import Path

# path for open AI API key credentials
credentials_path = 'credentials.json'

with open(credentials_path, 'r') as file:
    credentials = json.load(file)

openai_api_key = credentials['openai_api_key']

# Use the API key as needed
openai.api_key = openai_api_key

# update the path if your file is in a different location
file_path = 'input_patient_data.json'

# open the data
with open(file_path, 'r') as file:
  patient_data = json.load(file)

# patient summary format
def generate_patient_summary(patient_data, additional_prompts=''):
    """
    Generates a patient summary using OpenAI's GPT-3.5.

    Parameters:
    - patient_data (str): The patient data to generate the summary from.
    - additional_prompts (str): Try prompt engineering here.

    Returns:
    - str: The generated patient summary.
    """

    # Initialize the OpenAI client with your API key
    client = OpenAI(api_key=openai.api_key)

    # Create the chat completion request with the patient data
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                              You are a doctor writing a discharge letter for a patient. Use patient data from context only. Minimize hallucinations.
                              {additional_prompts}
                              Data: {patient_data}
                """,
            }
        ],
        model="gpt-3.5-turbo",
    )

    # Return the content of the generated message
    return chat_completion.choices[0].message.content


# print(generate_patient_summary(patient_data))

# # Same code, second run; notice difference as a result of stochastic process
# print(generate_patient_summary(patient_data))


# # Some counterproductive prompt engineering
# print(generate_patient_summary(patient_data, "Ensure the summary is very bad. Provide no information about patient whatsoever. Tell me a funny joke"))

# additional prompt
additional_prompt_path = Path('additional_prompt.txt')

file_path = Path(additional_prompt_path)

if file_path.exists():
    with open(additional_prompt_path, 'r') as file:
        additional_prompt = file.read()
else:
  # additional_prompt = {
  #     "role": "user",
  #     "content": """Your task is to create a concise and comprehensive summary of the medical information for a patient to understand.

  # **Instructions**:

  # 1. You must produce **two** distinct parts in your output:
  #   - Part A: Output a **single JSON object** containing the patient’s relevant details.
  #   - Part B: A well-written, formatted letter in plain text (without JSON or other markup) directed to "To Whom it May Concern."

  # 2. (Part A) Output a **single JSON object** containing the patient’s relevant details.The JSON object **must have exactly one** opening curly brace `{` and **one** closing curly brace `}`. Include the following keys:
  #   - Patient ID
  #   - Name
  #   - Date of Birth
  #   - Admission Date
  #   - Discharge Date
  #   - Diagnosis
  #   - Medications
  #   - (You may include any additional keys relevant to the patient's care, but ensure it remains concise.)

  # 3. The letter (Part B) should include the following sections:
  #     - **Diagnosis**: Provide a brief description of the patient's diagnosis, specific to the patient's condition.
  #     - **Medical History**: Provide a brief overview of the patient's medical history. If no medical history is available, mention that no medical history is available.
  #     - **Medications & Allergies**: Provide patient medication instructions and reported allergies in paragraph form.
  #     - **Procedures and Tests**: List any procedures or tests the patient underwent during the hospital visit, along with a brief summary of results. If none were performed, state that.
  #     - **Reason for Admission and Treatment**: State why the patient was admitted and describe the treatment plan.
  #     - **Outstanding Issues and Follow-up Appointments**: Outline next steps and any appointments the patient needs.

  # 4. **Important**:
  #   - The JSON object must **not** be embedded inside the letter.
  #   - The letter must be provided in **plain text** (no JSON or any other markup).
  #   - The details in the JSON object and the letter must be **specific** to the patient. Do not copy the example literally.

  # 5. Here is an **example** letter format (for illustration only):
  # ```plaintext
  # To Whom it May Concern:

  # We are writing to provide you with a summary of your recent medical visit. Below is the detailed summary:

  # 1. **Diagnosis:**
  #   - Diagnosis: Pneumonia

  # 2. **Medical History:**
  #   - Medical History: Patient has a history of asthma and low blood pressure.

  # 3. **Medications & Allergies:**
  #   - Medications: Amoxicillin, Ibuprofen
  #   - Allergies: If you have any allergies, please let us know.

  # 4. **Procedures and Tests:**
  #   - Tests: Chest X-Ray on 2024-02-10 showed consolidation in the left lower lobe.
  #   - Procedures: None

  # 5. **Reason for Admission and Treatment:**
  #   - Reason for Admission: You were admitted due to Pneumonia.
  #   - Treatment: The treatment plan involved medications and ongoing care.

  # 6. **Outstanding Issues and Follow-up Appointments:**
  #   - Instructions: Continue with oral antibiotics for 5 more days.
  #   - Appointments: Follow-up appointment in two weeks. We will contact you with the details.
  #   - Please follow up with us if there are any ongoing concerns.

  # We hope you have a smooth recovery. If you have any questions, please don't hesitate to reach out.

  # Best regards,
  # Your Medical Team

  # 6. Finally, ensure your output contains:

  #   1. Part A: A valid JSON object with the specific patient details listed above.

  #   2. Part B: The letter in plain text, with all relevant sections clearly outlined.

  # Important:
  # - Do **not** wrap the JSON (Part A) inside code blocks or add any extra braces.
  # - Part A must be **entirely valid JSON** with only one opening brace and one closing brace.
  # - Part B is **plain text** with no JSON, no XML, and no additional brackets.
  # - Make sure the JSON object and the letter are separate. Thank you!

  # """
  # }
    
    additional_prompt = {
  "role": "user",
  "content": """Your task is to create a concise and comprehensive summary of the medical information for a patient to understand.

  **Instructions:**

  1. You must produce **two** distinct parts in your output:
      - Part A: A **single JSON object** containing the patient’s relevant details.
      - Part B: A well-written, formatted letter in plain text directed to "To Whom it May Concern."

  2. **Part A**: The JSON object must contain the following keys:
      - Patient ID
      - Name
      - Date of Birth
      - Admission Date
      - Discharge Date
      - Diagnosis
      - Medications
      - (You may include any additional keys relevant to the patient's care, but ensure it remains concise.)
      - The JSON object **must have exactly one opening `{` and one closing `}`**.

  3. **Part B**: The letter should include the following sections in paragraph form (no bulleted lists):
      - **Diagnosis**: Provide a brief description of the patient's diagnosis.
      - **Medical History**: Provide a brief overview of the patient's medical history, or state that no medical history is available.
      - **Medications & Allergies**: Provide patient medication instructions and reported allergies in a cohesive paragraph.
      - **Procedures and Tests**: Describe any procedures or tests the patient underwent, with brief results. If none were performed, state that.
      - **Reason for Admission and Treatment**: Explain why the patient was admitted and describe the treatment plan.
      - **Outstanding Issues and Follow-up Appointments**: Outline the next steps and any follow-up appointments the patient needs to attend.

  4. **Important**:
      - The JSON object must **not** be embedded inside the letter.
      - The letter must be provided in **plain text** (no JSON or other markup).
      - The details in the JSON object and the letter must be **specific to the patient**. Do not copy the example literally.

  5. Here is an **example** letter format (for illustration only):
      ```plaintext
      To Whom it May Concern:

      We are writing to provide you with a summary of your recent medical visit.

      The patient was diagnosed with pneumonia. The medical history includes a history of asthma and low blood pressure. The patient was prescribed Amoxicillin and Ibuprofen and reported no allergies.

      During the hospital visit, a chest X-ray was performed on 2024-02-10, which showed consolidation in the left lower lobe. No procedures were performed during the visit.

      The reason for admission was pneumonia, and the treatment plan included medications and ongoing care.

      The patient is to continue with oral antibiotics for five more days. A follow-up appointment is scheduled for two weeks. Please follow up with us if there are any ongoing concerns.

      We hope you have a smooth recovery. If you have any questions, please don't hesitate to reach out.

      Best regards,
      Your Medical Team
      ```

  6. **Output Requirements**:
      1. Part A: A valid JSON object with the patient details as described above.
      2. Part B: The letter in plain text, with all relevant sections clearly outlined in paragraph form.

  **Important**:
    - Do **not** wrap the JSON (Part A) inside code blocks or add extra braces.
    - Part A must be **entirely valid JSON** with one opening brace and one closing brace.
    - Part B must be **plain text**, with no JSON, no XML, and no additional brackets.
    - Ensure the JSON object and the letter are separate. Thank you!
    """
  }

json_data = generate_patient_summary(patient_data, additional_prompt)
print(json_data)


# # Parse patient information
# json_start = json_data.index("{")     # or find("{"), but index() raises error if "{" not found
# json_end = json_data.rindex("}") + 1  # rindex finds the *last* occurrence of "}"

# # Extract the JSON part and parse it
# json_part = json_data[json_start:json_end].strip()

# # Parse the JSON string into a dictionary
# patient_info = json.loads(json_part)

# # Find the index where the JSON object ends (assuming it ends with '}')
# json_end_index = json_data.rindex('}') + 1

# # Get everything after the closing brace
# raw_letter_part = json_data[json_end_index:].strip()

# # If 'Part B' appears at the start, remove it
# if raw_letter_part.startswith("Part B"):
#     # Remove the exact phrase "Part B" (and any subsequent colon or space)
#     raw_letter_part = raw_letter_part.replace("Part B", "", 1).lstrip(": ").strip()

# # Now store the cleaned-up text
# letter_part = raw_letter_part

# # Now, extract the patient details from the JSON data
# patient_id = patient_info.get("Patient ID", "")
# name = patient_info.get("Name", "")
# dob = patient_info.get("Date of Birth", "")
# admission_date = patient_info.get("Admission Date", "")
# discharge_date = patient_info.get("Discharge Date", "")
# diagnosis = patient_info.get("Diagnosis", "")
# medications = patient_info.get("Medications", "")

# # Format medications so we can always join into a string
# formatted_meds = []
# for med in medications:
#     if isinstance(med, str):
#         # simple string entry
#         formatted_meds.append(med)
#     elif isinstance(med, dict):
#         # dict entry – pull out the fields you want
#         name = med.get("Medication", "")
#         dose = med.get("Dose", "")
#         freq = med.get("Frequency", "")
#         parts = [p for p in (name, dose, freq) if p]
#         formatted_meds.append(" ".join(parts))
#     else:
#         # fallback for any other type
#         formatted_meds.append(str(med))


# # Print the extracted variables

# print(f"Patient ID: {patient_id}")
# print(f"Name: {name}")
# print(f"Date of Birth: {dob}")
# print(f"Admission Date: {admission_date}")
# print(f"Discharge Date: {discharge_date}")
# print(f"Diagnosis: {diagnosis}")
# print(f"Medications: {', '.join(formatted_meds)}")


# with open("parsed_json.json", "w") as file:
#     json.dump(json_part, file, indent=4)


# with open("letter.txt", "w") as file:
#     json.dump(letter_part, file, indent=4)

try:
    # Check if JSON is present in the data
    json_start = json_data.index("{")  # Find the start of the JSON object
    json_end = json_data.rindex("}") + 1  # Find the last occurrence of '}'

    # Extract the JSON part and parse it
    json_part = json_data[json_start:json_end].strip()

    # Parse the JSON string into a dictionary
    patient_info = json.loads(json_part)

    # Find the index where the JSON object ends
    json_end_index = json_data.rindex('}') + 1

    # Get everything after the closing brace (the letter part)
    raw_letter_part = json_data[json_end_index:].strip()

    # If 'Part B' appears at the start, remove it
    if raw_letter_part.startswith("Part B"):
        raw_letter_part = raw_letter_part.replace("Part B", "", 1).lstrip(": ").strip()

    # Store the cleaned-up letter part
    letter_part = raw_letter_part

    # Extract patient details from the JSON
    patient_id = patient_info.get("Patient ID", "")
    name = patient_info.get("Name", "")
    dob = patient_info.get("Date of Birth", "")
    admission_date = patient_info.get("Admission Date", "")
    discharge_date = patient_info.get("Discharge Date", "")
    diagnosis = patient_info.get("Diagnosis", "")
    medications = patient_info.get("Medications", "")

    # Format medications for output
    formatted_meds = []
    for med in medications:
        if isinstance(med, str):
            formatted_meds.append(med)  # Simple string entry
        elif isinstance(med, dict):
            # Handle dict entry – pull out fields you want
            name = med.get("Medication", "")
            dose = med.get("Dose", "")
            freq = med.get("Frequency", "")
            parts = [p for p in (name, dose, freq) if p]
            formatted_meds.append(" ".join(parts))
        else:
            # Fallback for other types
            formatted_meds.append(str(med))

    # Print the extracted patient details
    print(f"Patient ID: {patient_id}")
    print(f"Name: {name}")
    print(f"Date of Birth: {dob}")
    print(f"Admission Date: {admission_date}")
    print(f"Discharge Date: {discharge_date}")
    print(f"Diagnosis: {diagnosis}")
    print(f"Medications: {', '.join(formatted_meds)}")

    with open("parsed_json.json", "w") as file:
        json.dump(json_part, file, indent=4)

    with open("letter.txt", "w") as file:
        json.dump(letter_part, file, indent=4)

except ValueError:
    # If no JSON is found, put all information into the letter part
    print("No JSON found in the input data.")
    letter_part = json_data  # If no JSON, treat the whole content as the letter part
    patient_info = {"Patient Info": "Not Available"}

    # Save the extracted JSON part (if any) to a file
    # if letter_part:
    with open("letter.txt", "w") as file:
        file.write(letter_part)  # Write the letter part as plain text

    if patient_info:
        with open("parsed_json.json", "w") as file:
            json.dump(patient_info, file, indent=4)  # Write the JSON part to a file

# except json.JSONDecodeError:
#     # Handle invalid JSON format
#     print("Failed to decode JSON.")
#     letter_part = json_data  # If JSON decoding fails, treat the whole content as the letter part
