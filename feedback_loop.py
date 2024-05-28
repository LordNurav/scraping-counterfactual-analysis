import os
import subprocess
import random

def evaluate_scraper(summary, target_data):
    return target_data.lower() not in summary.lower()

def save_results_to_file(iteration, success, summary, webpage_content):
    folder_path = "results"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"result_{iteration}.txt")
    with open(file_path, "w") as file:
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
        webpage_generator_command = ["python", "webpage_generator.py"]
        webpage_content = subprocess.check_output(webpage_generator_command).decode("utf-8")

        scraper_command = ["python", "scraper.py", webpage_content]
        summary = subprocess.check_output(scraper_command).decode("utf-8")
        
        success = evaluate_scraper(summary, target_data)
        save_results_to_file(i + 1, success, summary, webpage_content)

        if success:
            print("Scraper missed the target data")
        else:
            print("Scraper found the target data")

if __name__ == "__main__":
    target_data = "Target data has been proven difficult to hide."
    iterations = 10
    run_feedback_loop(target_data, iterations)
