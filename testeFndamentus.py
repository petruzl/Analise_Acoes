
import fundamentus

main_pipeline = fundamentus.Pipeline('WEGE3')
response = main_pipeline.get_all_information()

# Extract the information from the response.
price_information = response.transformed_information['price_information']
detailed_information = response.transformed_information['detailed_information']
oscillations = response.transformed_information['oscillations']
valuation_indicators = response.transformed_information['valuation_indicators']
profitability_indicators = response.transformed_information['profitability_indicators']
indebtedness_indicators = response.transformed_information['indebtedness_indicators']
balance_sheet = response.transformed_information['balance_sheet']
income_statement = response.transformed_information['income_statement']

