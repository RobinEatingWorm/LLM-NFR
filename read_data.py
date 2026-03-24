from pathlib import Path
import json
import pandas as pd

def read_csv(path):
    df = pd.read_csv(path, index_col="ID")
    results = {}
    results["TP"] = int(df['category'].value_counts().get('TP', 0))
    results["FP"] = int(df['category'].value_counts().get('FP', 0))
    results["TN"] = int(df['category'].value_counts().get('TN', 0))
    results["FN"] = int(df['category'].value_counts().get('FN', 0))

    return results

def main():
    results = {}
    for model_result in Path('results').iterdir():
        results[str(model_result).strip("/")[1]] = read_csv(model_result)
    
    total = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    for result in results:
        
        total["TP"] += results[result]["TP"] 
        total["FP"] += results[result]["FP"] 
        total["TN"] += results[result]["TN"] 
        total["FN"] += results[result]["FN"] 
    
    results["total"] = total

    with open("./results/all_results", 'w') as json_file:
        json.dump(results, json_file, indent=4)



if __name__ == "__main__":
    main()
