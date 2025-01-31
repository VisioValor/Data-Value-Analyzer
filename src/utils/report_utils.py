def print_report(report):
    """Print the analysis report in a formatted way"""
    if report is None:
        print("Analysis failed. Please check your dataset and try again.")
        return

    print("\n" + "="*50)
    print("DATASET ANALYSIS REPORT")
    print("="*50)

    for section, details in report.items():
        print(f"\n{section}:")
        print("-" * len(section))
        if isinstance(details, dict):
            for key, value in details.items():
                print(f"{key}: {value}")
        elif isinstance(details, list):
            for item in details:
                print(item)
        else:
            print(details) 