def publish_report(evaluation_outputs):
    # Aggregate and format the evaluation outputs
    report = "Evaluation Report\n"
    report += "=" * 20 + "\n"
    report += "\n".join(f"{key}: {value}" for key, value in evaluation_outputs.items())
    with open("evaluation_report.txt", "w") as f:
        f.write(report)