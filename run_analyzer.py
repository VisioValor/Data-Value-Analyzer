from src.analyzers.dataset_analyzer import DatasetAnalyzer
from src.utils.report_utils import print_report
import os

def main():
    print("\n" + "="*60)
    print("Dataset Value Analyzer")
    print("="*50)
    print("\nThis tool analyzes your dataset and estimates its market value.")
    print("\nSupported file formats:")
    print("- CSV files (.csv)")
    print("- Excel files (.xlsx, .xls)")
    
    analyzer = DatasetAnalyzer()

    while True:
        print("\nTo analyze your dataset:")
        print("1. Make sure your file is in CSV or Excel format")
        print("2. Copy the full path to your file")
        print("3. Paste the path below")
        print("\nExample paths:")
        print("Windows: C:\\Users\\YourName\\Documents\\dataset.csv")
        print("Mac/Linux: /home/username/documents/dataset.csv")
        print("\nEnter 'quit' to exit the program")
        
        print("\nPlease paste your file path:")
        file_path = input().strip()

        if file_path.lower() == 'quit':
            print("\nThank you for using Dataset Value Analyzer!")
            break

        if not os.path.exists(file_path):
            print("\nError: File not found!")
            print("Please check that:")
            print("- The file path is correct")
            print("- The file exists")
            print("- You have permission to access the file")
            continue

        print("\nAnalyzing dataset...")
        print("This may take a moment depending on the size of your dataset...")
        report = analyzer.analyze_dataset(file_path)
        print_report(report)
        
        print("\nWould you like to analyze another dataset? (yes/no)")
        if input().lower().strip() != 'yes':
            print("\nThank you for using Dataset Value Analyzer!")
            break

if __name__ == "__main__":
    main() 