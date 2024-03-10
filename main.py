## Testing the abilities of different models to do arithmetic:
import pandas as pd
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.base_provider import Model
import tqdm


class Evaluator:

  def __init__(self, dataset_path: str) -> None:
    self.dataset = pd.read_csv(dataset_path)

  def evaluate(self, model: Model):
    model_responses = []  # To store model responses
    matches = []  # To store match results

    for idx, row in self.dataset.iterrows():
      op = row["eval_category"]
      match op:
        case "multiply":
          op = "*"
        case "addition":
          op = "+"
        case "substraction":
          op = "-"
      expression = str(op).join([str(x) for x in eval(row["List_numbers"])])
      expected_answer = row["Expected_result"]
      for attempt in range(3):
        try:
          if row[
              "Model_response"] != "Error: Model failed to predict after 3 attempts.":
            model_response = row["Model_response"]
            break
          model_response = model.predict(expression)
          break
        except Exception as e:
          if attempt < 2:  # If it's not the last attempt
            print(f"Attempt {attempt + 1} failed, retrying...", e)
          else:
            print("Failed after 3 attempts.", e)
            model_response = "Error: Model failed to predict after 3 attempts."
      model_responses.append(model_response)
      is_matched = expected_answer in model_response or expected_answer in model_response.replace(
          ",", "")
      matches.append(is_matched)

    # Update the DataFrame after the loop
    self.dataset["Model_response"] = model_responses
    self.dataset["matched"] = matches
    self.dataset["model_name"] = model.name

    # Save the updated DataFrame
    self.dataset.to_csv(f"./results/{model.name}_arithmetic_test.csv",
                        index=False)

    grouped = self.dataset.groupby(
        ['eval_category', 'Num_digits', 'Num_numbers', 'model_name'])
    accuracy_df = grouped.apply(lambda x: pd.Series(
        {'accuracy': 100 * x['matched'].sum() / len(x)})).reset_index()

    # Save the accuracy results to a CSV file
    accuracy_df.to_csv(f"./results/{model.name}_arithmetic_results.csv")
    return accuracy_df


if __name__ == "__main__":
  evaluator = Evaluator("./dataset/eval_data.csv")
  # evaluator.evaluate(OpenAIProvider("gpt-3.5-turbo"))
  # evaluator.evaluate(OpenAIProvider("gpt-4-turbo-preview"))
  evaluator.evaluate(AnthropicProvider("claude-3-opus-20240229"))
