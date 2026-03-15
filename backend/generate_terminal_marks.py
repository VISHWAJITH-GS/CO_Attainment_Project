import pandas as pd
import numpy as np

# --- Configuration ---
NUM_STUDENTS = 15
CO_COUNT = 6
TOTAL_MARKS = 100

# --- Create Base DataFrame ---
# Create Registration Numbers and Names
regnos = [f"312221104{i:03d}" for i in range(1, NUM_STUDENTS + 1)]
names = [f"Student {chr(64 + i)}" for i in range(1, NUM_STUDENTS + 1)]

df = pd.DataFrame({
    'REGNO': regnos,
    'Student NAME': names
})

# --- Generate Marks for 6 COs ---
# Distribute 100 marks among 6 questions (e.g., 20, 20, 20, 15, 15, 10)
q_max_marks = [20, 20, 20, 15, 15, 10]

for i in range(CO_COUNT):
    q_name = f"Q{i+1}"
    max_mark = q_max_marks[i]
    
    # Generate random marks, with a higher probability of scoring well
    # and a chance of being absent (marked as 'AB')
    marks = np.random.randint(int(max_mark * 0.4), max_mark + 1, size=NUM_STUDENTS)
    
    # Introduce a few lower scores and absences
    for j in range(NUM_STUDENTS):
        if np.random.rand() < 0.1: # 10% chance of a very low score
            marks[j] = np.random.randint(0, int(max_mark * 0.3))
        if np.random.rand() < 0.05: # 5% chance of being absent
            # Use a placeholder for absent that can be easily filtered if needed
            # For this purpose, we'll use -1 and then convert to 'AB'
            marks[j] = -1 
            
    df[q_name] = marks

# --- Create Header Structure ---
# This mimics the structure of the other files, with metadata at the top
header_df = pd.DataFrame([
    ['', '', '', '', '', '', 'Terminal Assessment Marks'],
    ['S.No', 'REGNO', 'Student NAME', 'CO1', 'CO2', 'CO3', 'CO4', 'CO5', 'CO6'],
    ['', '', '', q_max_marks[0], q_max_marks[1], q_max_marks[2], q_max_marks[3], q_max_marks[4], q_max_marks[5]]
])

# --- Prepare final student data ---
student_df = pd.DataFrame()
student_df['S.No'] = range(1, NUM_STUDENTS + 1)
student_df['REGNO'] = df['REGNO']
student_df['Student NAME'] = df['Student NAME']

# Add the question marks
for i in range(CO_COUNT):
    student_df[f'Q{i+1}'] = df[f'Q{i+1}']

# Replace -1 with 'AB' for absent students
student_df.replace(-1, 'AB', inplace=True)

# --- Write to Excel ---
output_path = 'data/TERMINAL.xlsx'
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Write header without the index or its own header
    header_df.to_excel(writer, sheet_name='Sheet1', startrow=0, index=False, header=False)
    # Write student data below the header
    student_df.to_excel(writer, sheet_name='Sheet1', startrow=len(header_df), index=False, header=False)

print(f"✅ Dummy terminal marks file created at: {output_path}")
