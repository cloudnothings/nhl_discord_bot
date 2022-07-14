from discord import File


# TODO: Simple formatting for outputting wins and losses. Adjust as needed or copy for future funcs
def show_recent_results(matches, club_id):
    message = ""
    for match in matches:
        message += f"Match ID: {match['matchId']}\n"
        for team in match['clubs']:
            if str(team) != str(club_id):
                other_team = team
        message += f"Results:\nYour team {match['aggregate'][club_id]['score']} " \
                   f"| {match['aggregate'][other_team]['score']} Opponents\n"
    return message


# TODO: Implement convert json data to csv, Return csv as string maybe
def json_to_excel(data):
    json_to_excel_result = f"{data}.csv"
    print('nice')
    return json_to_excel_result


def create_text_file(message, file_name):
    file_name = f'{"".join(file_name)}.txt'
    with open(file_name, 'w+') as f:
        f.write(message)
    with open(file_name, 'rb') as file:
        stuff = File(file, file_name)
        file.close()
        return stuff
