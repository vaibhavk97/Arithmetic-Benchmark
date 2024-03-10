import pandas as pd
import itertools
import random


def create_eval_data():
  categories = ['multiply', 'addition', 'substraction']
  results = []
  for digits in range(2, 9):  # From 2 to 8 digits
    for num_numbers in range(2, 6):  # From 2 to 5 numbers
      for _ in range(20):
        for category in categories:
          numbers = [
              random.randint(10**(digits - 1), (10**digits) - 1)
              for _ in range(num_numbers)
          ]
          if category == 'multiply':
            result = 1
            for num in numbers:
              result *= num
          elif category == 'addition':
            result = sum(numbers)
          elif category == 'substraction':
            result = numbers[0]
            for num in numbers[1:]:
              result -= num
          results.append({
              'eval_category': category,
              'Num_digits': digits,
              'Num_numbers': num_numbers,
              'List_numbers': numbers,
              'Expected_result': result
          })
  df = pd.DataFrame(results)
  df.to_csv('eval_data.csv', index=False)


create_eval_data()
