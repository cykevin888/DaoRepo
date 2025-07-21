import pandas as pd
import os
import random
import json
from datetime import datetime
import multiprocessing
import math

# --- Configuration Parameters ---
TOTAL_SIZE_LIMIT_GB = 0.01
# WAV file size range in Megabytes (MB)
WAV_SIZE_RANGE_MB = (1, 7)
# Number of parallel processes to use for file generation.
# Set to 0 to automatically use (all available CPU cores - 1).
NUM_PARALLEL_PROCESSES = 2
# Directory to save the generated wav/json files
OUTPUT_DIR = 'metadata'
# Directory to save the report file
REPORT_DIR = 'report'
# Base name for the Excel report file
BASE_REPORT_NAME = 'report.xlsx'
# --- End of Configuration ---

def create_file_pair(transaction_id):
    """
    Worker function: Creates a single pair of WAV and JSON files.
    This function is executed by each process in the pool.
    """
    # Define file paths
    wav_filepath = os.path.join(OUTPUT_DIR, f"{transaction_id}.wav")
    json_filepath = os.path.join(OUTPUT_DIR, f"{transaction_id}.json")

    # 1. Create JSON file
    contact_id = random.randint(100000000, 999999999)
    data = {'contact_id': str(contact_id)}
    try:
        with open(json_filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        return None # Return None on failure

    # 2. Create WAV file
    wav_size_mb = random.uniform(WAV_SIZE_RANGE_MB[0], WAV_SIZE_RANGE_MB[1])
    size_bytes = int(wav_size_mb * 1024 * 1024)
    try:
        with open(wav_filepath, 'wb') as f:
            f.write(os.urandom(size_bytes))
    except IOError:
        # Clean up the created JSON file if WAV creation fails
        os.remove(json_filepath)
        return None

    return transaction_id

def main():
    """
    Generates JSON and WAV files in parallel and updates an Excel report.
    """
    # Create output directories if they don't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    
    # --- Pre-calculate the number of files to generate ---
    avg_wav_size_mb = sum(WAV_SIZE_RANGE_MB) / 2
    avg_wav_size_gb = avg_wav_size_mb / 1024
    num_files_to_generate = math.ceil(TOTAL_SIZE_LIMIT_GB / avg_wav_size_gb)

    print(f"Estimated number of files to generate: {num_files_to_generate}")

    # --- Generate all unique IDs upfront ---
    print("Generating unique transaction IDs...")
    existing_ids = set()
    transaction_ids = []
    for _ in range(num_files_to_generate):
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(26)])
        transaction_id = f"{date_str}{random_part}"
        while transaction_id in existing_ids:
            random_part = ''.join([str(random.randint(0, 9)) for _ in range(26)])
            transaction_id = f"{date_str}{random_part}"
        existing_ids.add(transaction_id)
        transaction_ids.append(transaction_id)
    print("...Unique IDs generated.")
    
    # --- Determine the number of processes to use ---
    if NUM_PARALLEL_PROCESSES > 0:
        cpu_count = NUM_PARALLEL_PROCESSES
    else:
        # Default behavior: use one less than the total number of CPUs to leave resources for the OS
        cpu_count = max(1, multiprocessing.cpu_count() - 1)
    
    print(f"\nStarting file generation with {cpu_count} parallel processes...")

    generated_ids = []
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=cpu_count) as pool:
        # Use imap_unordered to process the list of IDs
        results_iterator = pool.imap_unordered(create_file_pair, transaction_ids)
        
        # Iterate through the results without a progress bar
        for result in results_iterator:
            if result:
                generated_ids.append(result)
    
    if not generated_ids:
        print("No files were generated. Something went wrong.")
        return

    print(f"\nSuccessfully generated {len(generated_ids)} file pairs.")

    # --- Determine Report Filename ---
    base_report_path = os.path.join(REPORT_DIR, BASE_REPORT_NAME)
    report_file_path = base_report_path

    if not os.path.exists(report_file_path):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        report_file_path = os.path.join(REPORT_DIR, f'report_{timestamp}.xlsx')
        print(f"'{BASE_REPORT_NAME}' not found. A new report will be created: '{report_file_path}'")
    else:
        print(f"Updating existing report: '{report_file_path}'")

    # --- Update Excel Report ---
    try:
        df_existing = pd.DataFrame()
        if os.path.exists(report_file_path): 
            try:
                # Read existing data, being robust to empty files or parsing errors
                df_existing = pd.read_excel(report_file_path, header=14, engine='openpyxl')
                df_existing.columns = [col.replace('Transactioon ID', 'Transaction ID') for col in df_existing.columns]
            except Exception:
                pass # df_existing remains empty

        headers = ['organization', 'Employee', 'interaction type', 'Interaction start time', 'Transaction ID', 'Status']
        if df_existing.empty:
            df_existing = pd.DataFrame(columns=headers)

        df_new_data = pd.DataFrame({
            'Transaction ID': generated_ids,
            'Status': ['Success'] * len(generated_ids)
        })
        
        df_final = pd.concat([df_existing, df_new_data], ignore_index=True)
        df_final = df_final.reindex(columns=headers)

        with pd.ExcelWriter(report_file_path, engine='openpyxl') as writer:
            df_final.to_excel(writer, index=False, startrow=14)

        print(f"Successfully updated '{report_file_path}' with {len(generated_ids)} new transaction IDs.")
    except Exception as e:
        print(f"\nAn error occurred while updating the Excel file: {e}")
        fallback_file = 'transaction_ids.txt'
        with open(fallback_file, 'w') as f:
            for tid in generated_ids:
                f.write(f"{tid}\n")
        print(f"Transaction IDs have been saved to '{fallback_file}' as a backup.")

if __name__ == '__main__':
    # This check is crucial for multiprocessing to work correctly, especially on Windows
    main()