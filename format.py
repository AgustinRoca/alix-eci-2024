import json

def custom_format_json(data, indent=0):
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            formatted_value = custom_format_json(value, indent + 2)
            items.append(f'{" " * (indent + 2)}"{key}": {formatted_value}')
        return "{\n" + ",\n".join(items) + f'\n{" " * indent}}}'
    elif isinstance(data, list):
        if all(isinstance(i, (int, float)) for i in data):
            return "[" + ", ".join(map(str, data)) + "]"
        else:
            items = []
            for item in data:
                if isinstance(item, list) and all(isinstance(i, (int, float)) for i in item):
                    formatted_value = "[" + ", ".join(map(str, item)) + "]"
                else:
                    formatted_value = custom_format_json(item, indent + 2)
                items.append(f'{" " * (indent + 2)}{formatted_value}')
            return "[\n" + ",\n".join(items) + f'\n{" " * indent}]'
    else:
        return json.dumps(data)

def format_json(input_file, output_file):
    try:
        # Read the JSON file
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Custom format the JSON data
        formatted_data = custom_format_json(data)

        # Write the formatted JSON to the output file
        with open(output_file, 'w') as f:
            f.write(formatted_data)

        print(f"JSON file has been formatted and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
input_file = 'data/parcelas_santiago.json'  # Path to your 75MB JSON file
output_file = 'data/parcelas_santiago_formatted.json'  # Path to save the formatted JSON file

format_json(input_file, output_file)
