import argparse
import jsonlines
import warnings
from transformers import AutoTokenizer
import os
import glob
import pandas as pd
import numpy as np

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.models.t5.tokenization_t5_fast")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers.convert_slow_tokenizer")

def test_tokenizer_string(tokenizer, test_string):
    tokens = tokenizer.tokenize(test_string)
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    decoded_string = tokenizer.decode(token_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    exact_match = test_string == decoded_string
    lowercase_match = test_string.lower() == decoded_string.lower()

    return "Success" if exact_match else ("Lowercase" if lowercase_match else "Failed")

def calculate_efficiency(tokenizer, directory):
    results = []
    file_paths = glob.glob(os.path.join(directory, '*.txt'))
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        # Extracts "language" from "prefix_language.txt"
        language = filename.split("_")[-1].split(".")[0]  

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            tokens = tokenizer.tokenize(text)
            words_count = len(text.split())
            efficiency = (words_count / len(tokens) * 100) if tokens else 0
            tokens_per_word = (len(tokens) / words_count) if words_count else 0
            results.append({
                "file": filename,
                "language": language,
                "efficiency": efficiency,
                "tokens_per_word": tokens_per_word
            })
    return results

def main(args):
    rows = []
    try:
        with jsonlines.open(args.input_file) as reader:
            for tokenizer_info in reader:
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_info["url"], use_fast=True, legacy=("mT5Tokenizer" == tokenizer_info["name"]))

                scand_result = test_tokenizer_string(tokenizer, "ÆØÅ æøå")
                nordic_result = test_tokenizer_string(tokenizer, "Åsa Ängel Örjan Ægir Øystein Ýmir Þor Ðan Måns Märtha Sölvi Kærlighed Brøn Lýður Aþena Sæði")
                eng_result = test_tokenizer_string(tokenizer, "This is a basic test of the tokenizer, to see if it is reversible in English.")
                
                file_efficiency_results = calculate_efficiency(tokenizer, args.directory)
                for result in file_efficiency_results:
                    rows.append({
                        'tokenizer': tokenizer_info["name"],
                        'scand_test': scand_result,
                        'nordic_test': nordic_result,
                        'eng_test': eng_result,
                        'file': result['file'],
                        'language': result['language'],
                        'efficiency': result['efficiency'],
                        'tokens_per_word': result['tokens_per_word'],
                    })

    except Exception as e:
        print(f"Error processing tokenizers: {e}")
    
    df = pd.DataFrame(rows)
    df['efficiency'] = pd.to_numeric(df['efficiency'], errors='coerce')

    # Function to format efficiency values with one decimal place and a percent sign
    def format_efficiency(value):
        if pd.isnull(value):
            return None
        return f"{value:.1f}%"

    # Initialize failed_summary as an empty DataFrame to handle cases where no failures occur
    failed_summary = pd.DataFrame()

    # First, identify tokenizers where all tests are "Success"
    success_tokenizers = df.groupby('tokenizer').filter(lambda x: all(x[['scand_test', 'nordic_test', 'eng_test']].eq('Success').all(axis=1)))

    if not success_tokenizers.empty:
        # Pivot to have languages as columns, efficiencies are already numeric
        success_summary = success_tokenizers.pivot(index='tokenizer', columns='language', values='efficiency')
        
        # Calculate the average efficiency directly, efficiencies are already numeric
        success_summary['Average Efficiency'] = success_summary.mean(axis=1, skipna=True)
        
        # Format all efficiency values to one decimal place
        for col in success_summary.columns.difference(['tokenizer', 'Average Efficiency']):
            success_summary[col] = success_summary[col].apply(lambda x: f"{x:.1f}%")


        # Convert 'Average Efficiency' to percentage format
        success_summary['Average Efficiency'] = success_summary['Average Efficiency'].apply(lambda x: f"{x:.1f}%")

        success_summary.reset_index(inplace=True)
        

        # Reorder columns to place 'Average Efficiency' at the end, if needed
        cols = [col for col in success_summary if col != 'Average Efficiency'] + ['Average Efficiency']
        success_summary = success_summary[cols]

        # Sorting by 'Average Efficiency' without converting back to float as it's already sorted numerically before formatting
        success_summary = success_summary.sort_values(by='Average Efficiency', ascending=False)


    # For tokenizers where any test did not succeed, include additional columns
    failed_tokenizers = df.groupby('tokenizer').filter(lambda x: any(x[['scand_test', 'nordic_test', 'eng_test']].ne('Success').any(axis=1)))

    if not failed_tokenizers.empty:
        failed_summary = failed_tokenizers.groupby('tokenizer').agg({
            'efficiency': 'first', 
            'scand_test': 'first', 
            'nordic_test': 'first', 
            'eng_test': 'first'
        }).reset_index()

        # Since 'efficiency' might already be numeric or a string with '%', 
        # check if conversion is necessary
        if failed_summary['efficiency'].dtype == object:
            # Attempt to strip '%' and convert only if dtype is object (string)
            failed_summary['efficiency'] = failed_summary['efficiency'].str.replace('%', '').astype(float)

        # Assuming 'efficiency' is now numeric, we can directly sort
        failed_summary = failed_summary.sort_values(by='efficiency', ascending=False)

        # After sorting, format the 'efficiency' values as percentages
        failed_summary['efficiency'] = failed_summary['efficiency'].apply(lambda x: f"{x:.1f}%")

        # Rename the column after all processing is complete to avoid confusion
        failed_summary = failed_summary.rename(columns={'efficiency': 'Average Efficiency'})
        
        cols = [col for col in failed_summary.columns if col != 'Average Efficiency']
        
        # Then, add 'Average Efficiency' at the end
        cols.append('Average Efficiency')
        
        # Reassign the column order
        failed_summary = failed_summary[cols]
    
    # Printing Success Summary in Markdown
    if not success_tokenizers.empty:
        print("### Success Summary\n")
        print(success_summary.to_markdown(index=False))
        print("\n")  # Add a newline for better readability

    # Printing Failure Summary in Markdown
    if not failed_summary.empty:
        print("### Failure Summary\n")
        print(failed_summary.to_markdown(index=False))

     
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tokenize test strings with various tokenizers, compute efficiency for each file in a specified directory, and report test outcomes along with efficiency metrics.")
    parser.add_argument('--input_file', type=str, default='tokenizer_list.jsonl', help='Path to the JSONL file containing tokenizer info. Default is "tokenizer_list.jsonl".')
    parser.add_argument('--directory', type=str, default='wikipedia_1k', help='Directory containing text files for calculating efficiency and tokens per word. Default is "wikipedia_1k".')

    args = parser.parse_args()
    main(args)

