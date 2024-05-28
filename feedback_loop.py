import os
import subprocess
import random
import json

def evaluate_scraper(summary):
    return "target data" not in summary.lower()

def save_results_to_file(iteration, success, summary, webpage_content):
    folder_path = "results"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"result_{iteration}.txt")
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(f"Target data found in summary: {not success}\n\n")
        file.write("Summary:\n")
        file.write(summary + "\n\n")
        file.write("Webpage content:\n")
        file.write(webpage_content)
    print(f"Results saved to {file_path}")

def run_feedback_loop(target_data, iterations):
    for i in range(iterations):
        print(f"Iteration {i + 1}")
        modification_factor = random.randint(1, 3)

        # Update the modification factor in the configuration file
        update_config(modification_factor)
        
        # Generate webpage content
        webpage_generator_command = ["python", "webpage_generator.py"]
        try:
            webpage_content = subprocess.check_output(webpage_generator_command, encoding='utf-8').strip()
        except UnicodeDecodeError:
            webpage_content = subprocess.check_output(webpage_generator_command).decode('latin-1').strip()
        
        # Scrape and summarize content
        scraper_command = ["python", "scraper.py"]
        summary = subprocess.check_output(scraper_command, input=webpage_content, text=True).strip()
        
        # Evaluate and save results
        success = evaluate_scraper(summary)
        save_results_to_file(i + 1, success, summary, webpage_content)

        if success:
            print("Scraper missed the target data")
        else:
            print("Scraper found the target data")

def update_config(modification_factor):
    config = {'modification_factor': modification_factor}
    with open('config.json', 'w') as file:
        json.dump(config, file)

if __name__ == "__main__":
    target_data = "Target data has been proven difficult to hide."
    iterations = 10
    run_feedback_loop(target_data, iterations)
