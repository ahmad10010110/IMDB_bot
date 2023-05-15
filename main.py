# Import functions from the 'funcs' module
from funcs import *

# Main program

# Initialize the message index to 0
message_index = 0

# Check the status of the bot using the 'bot_status' function
if bot_status() == False:
    print('there is a problem')

# If the bot is running, enter an infinite loop that listens for updates from users
else:
    while True:
        # Get the latest updates using the 'get_updates' function and assign them to a variable called 'received'
        received = get_updates()

        # Extract the relevant information from each update using the 'extract_updates' function and assign the result to a variable called 'updates'
        updates = extract_updates(received)

        # Loop over all the updates
        for update in updates:

            # Check if the update contains text or callback data
            if "text" in update or "callback_query" in update:
                # If the 'type' key in the current update dictionary is not 'callback_query'
                if update["type"] == "message" or update["type"] == "edited_message":
                    # Check if the received message starts with a command "/"
                    if update["text"][0] == "/":
                        # Handle the command using the 'command_handler' function
                        command_handler(update, message_index)
                        message_index += 1
                        ignore_update(urlBOT, update)
                        # The received message did not contain a command. We need to figure out what was the last command issued by the user, so that we can provide a response based on it.

                    else:
                        chat_id = update["chat_id"]
                        if chat_id in users_command:
                            user_command = users_command[chat_id]["user_command"]
                            # Get the user's command from the dictionary

                            if user_command == "/search_movie":
                                search_movie_handler(urlBOT, urlAPI, update)
                                # Call the function to handle a movie search
                                ignore_update(urlBOT, update)

                            elif user_command == "/search_people":
                                search_people_handler(urlBOT, urlAPI, update)
                                # Call the function to handle a people search
                                ignore_update(urlBOT, update)

                            else:
                                command_handler(update, message_index)
                                # Call the general command handler function
                                message_index += 1
                                ignore_update(urlBOT, update)

                # If the 'type' key in the current update dictionary is 'callback_query'
                elif update["type"] == "callback_query":
                    callback_data = update["callback_query"]
                    callback_query = json.loads(callback_data)
                    # callback_query = [category, message_id, change_index]
                    category = callback_query[0]

                    if category == path["movie250"] or category == path["series250"] or category == path["pop_movies"] or category == path["pop_series"]:
                        generate_top_movies(urlBOT, urlAPI, update)
                        # Call the function to generate a list of the top movies
                        ignore_update(urlBOT, update)

                    elif category == path["search_movie"]:
                        search_movie_handler(urlBOT, urlAPI, update)
                        # Call the function to handle a movie search
                        ignore_update(urlBOT, update)

                    elif category == path["search_people"]:
                        search_people_handler(urlBOT, urlAPI, update)
                        # Call the function to handle a people search
                        ignore_update(urlBOT, update)

                    elif category == path["movie_info"]:
                        more_info_movie_result(urlBOT, urlAPI, update)
                        # Call the function to get more information about a movie
                        ignore_update(urlBOT, update)

                    elif category == path["people_info"]:
                        more_info_people_result(urlBOT, urlAPI, update)
                        # Call the function to get more information about a person
                        ignore_update(urlBOT, update)

                    elif category == path["actors"]:
                        actors_results(urlBOT, update)
                        # Call the function to get information about actors in a movie
                        ignore_update(urlBOT, update)

                    elif category == path["directors"] or category == path["writers"]:
                        writers_or_directors_result(urlBOT, update)
                        # Call the function to get information about writers or directors in a movie
                        ignore_update(urlBOT, update)

                    elif category == path["plot"]:
                        plot_result(urlBOT, update)
                        # Call the function to get the plot summary of a movie
                        ignore_update(urlBOT, update)

                    elif category == path["finance"]:
                        finance_result(urlBOT, update)
                        # Call the function to get financial information about the movie
                        ignore_update(urlBOT, update)

                    elif category == path["trailer"]:
                        trailer_result(urlBOT, urlAPI, update)
                        # Call the function to get the movie trailer
                        ignore_update(urlBOT, update)

                    elif category == path["similars"]:
                        similars_results(urlBOT, update)
                        # Call the function to get similar movies
                        ignore_update(urlBOT, update)

                    elif category == path["images"]:
                        images_result(urlBOT, urlAPI, update)
                        # Call the function to get images of the movies
                        ignore_update(urlBOT, update)

                    elif category == path["backstage"]:
                        backstage_result(urlBOT, update)
                        # Call the function to get backstages of the movies
                        ignore_update(urlBOT, update)

                    elif category == path["posters"]:
                        posters_result(urlBOT, update)
                        # Call the function to get posters of the movies
                        ignore_update(urlBOT, update)

                    elif category == path["backdrops"]:
                        backdrops_result(urlBOT, update)
                        # Call the function to get backdrops of the movies
                        ignore_update(urlBOT, update)

                    elif category == path["bests"]:
                        best_works_result(urlBOT, update)
                        # Call the function to get the best works of the person
                        ignore_update(urlBOT, update)

                    else:
                        ignore_update(urlBOT, update)

            # If I receive something that is not valid, I will ignore it
            else:
                ignore_update(urlBOT, update)


