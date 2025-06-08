import pandas as pd

def evaluate_sentiment_predictions(actual_csv_path: str, predicted_csv_path: str, 
                                   actual_label_col: str = 'sentiment', 
                                   predicted_label_col: str = 'sentiment_label', 
                                   max_predictions: int = 100):
    """
    Evaluates sentiment prediction performance by comparing actual and predicted labels.

    Args:
        actual_csv_path (str): Path to CSV file containing actual sentiment labels.
        predicted_csv_path (str): Path to CSV file containing predicted sentiment labels.
        actual_label_col (str): Column name for actual labels in actual CSV. Default is 'sentiment'.
        predicted_label_col (str): Column name for predicted labels in predicted CSV. Default is 'sentiment_label'.
        max_predictions (int): Number of predicted rows to consider (to match actuals). Default is 100.

    Prints:
        - Total counts of each actual label.
        - Correct prediction counts per class.
        - Accuracy per class (correct predictions / total actuals).
        - Overall accuracy of all predictions.
    """

    # Load data
    labelled_data = pd.read_csv(actual_csv_path)
    predicted_data = pd.read_csv(predicted_csv_path)

    # Limit predicted data to max_predictions rows
    predicted_data = predicted_data.iloc[:max_predictions]

    # Add predicted labels to actual dataframe
    labelled_data['predicted'] = predicted_data[predicted_label_col]

    # Prepare dataframe for analysis
    df = labelled_data[[actual_label_col, 'predicted']].rename(columns={actual_label_col: 'actual'})

    # Count total actual labels
    actual_counts = df['actual'].value_counts()

    # Count correct predictions per class
    correct_predictions = df[df['actual'] == df['predicted']].groupby('actual').size()

    # Calculate per-class accuracy
    accuracy_per_class = (correct_predictions / actual_counts).fillna(0).round(2)

    # Print results
    print("Total actual counts:\n", actual_counts, "\n")
    print("Correct predictions per class:\n", correct_predictions, "\n")
    print("Per-class accuracy:\n", accuracy_per_class, "\n")

    # Overall accuracy
    overall_accuracy = (df['actual'] == df['predicted']).mean().round(2)
    print("Overall Accuracy:", overall_accuracy)
