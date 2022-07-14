from discord import File


# TODO: Implement convert json data to csv. Time will tell if Google Sheets can take a csv through API
def json_to_csv(data):
    """Will convert json to csv"""
    return create_text_file(data, 'results.csv')


def create_text_file(message, file_name):
    """Creates file from given string"""
    file_name = f'{"".join(file_name)}'
    with open(file_name, 'w+') as f:
        f.write(message)
    with open(file_name, 'rb') as file:
        stuff = File(file, file_name)
        file.close()
        return stuff
