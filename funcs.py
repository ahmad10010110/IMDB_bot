import requests   # Importing the "requests" module for making HTTP requests
import json       # Importing the "json" module for handling JSON data

#################################################################################

# Stores your Telegram bot token in the variable 'token'.
token = "your token"


# This is the URL for Telegram's API that will be used to make requests to their server.
urlBOT = "https://api.telegram.org/bot{}/".format(token)
# request format: https://api.telegram.org/bot<your-bot-token>/<command>

#################################################################################

# This dictionary maps bot commands to their corresponding API methods.
commands = {
    'bot': 'getme',
    'update': 'getUpdates',
    'send': 'sendMessage',
    'photo': 'sendPhoto',
    'edit_txt': 'editMessageText',
    'edit_caption': 'editMessageCaption',
    'edit_image': 'editMessageMedia'
}

# This list stores the bot's available commands.
bot_commands = [
    "/start",
    "/search_movie",
    "/search_people",
    "/help",
    "error",
    "/top_movies",
    "movie250",
    "series250",
    "pop_movies",
    "pop_series"
]

# This dictionary maps search paths to numeric values, which are used for tracking user navigation.
path = {
    "search_movie": 0,
    "movie_info": 1,
    "actors": 2,
    "person_info": 3,
    "all_works": 4,
    "bests": 5,
    "plot": 6,
    "directors": 7,
    "writers": 8,
    "trailer": 9,
    "images": 10,
    "posters": 11,
    "backstage": 12,
    "backdrops": 13,
    "similars": 14,
    "/top_movies": 15,
    "movie250": 16,
    "series250": 17,
    "pop_movies": 18,
    "pop_series": 19,
    "search_people": 20,
    "people_info": 21,
    "finance": 22
}
#################################################################################

# This dictionary stores movies that users searched. It is used for API limitation purposes.
# The keys are search expressions and the values are results.
searched_movies = {}

# This dictionary stores additional information about movies. The keys are movie IDs and the values are results.
more_info_movie_dict = {}

# This dictionary stores trailers for movies. The keys are movie IDs and the values are results.
trailer_movie_dict = {}

# This dictionary stores posters for movies. The keys are movie IDs and the values are results.
posters_movie_dict = {}

# This dictionary stores images for movies. The keys are movie IDs and the values are results.
images_movie_dict = {}

# This dictionary stores people that users searched. It is used for API limitation purposes.
# The keys are search expressions and the values are results.
searched_people = {}

# This dictionary stores global data, which can be accessed by functions across the program.
global_datas = {}

####################################################################################

# This dictionary stores user commands and their search data.
# The keys are chat IDs, which correspond to specific users.
# The values are dictionaries that store categories, expressions/titles, message IDs, and search data.
# Example: {"chat_id": {"category": {"expression": {"message_id": message_id, "data": search_data}}}}
users = {}

# This dictionary stores the last command made by each user.
# The keys are chat IDs and the values are dictionaries that store the message index and the user command.
# Example: {"chat_id": {"message_index": message_index, "user_cmd": user_cmd}}
users_command = {}

# This dictionary stores message IDs and their corresponding message indexes.
# The keys are message indexes and the values are message IDs.
dict_message = {}

# This variable stores the current message index.
message_index = 0


# bot id
bot_id = "@your_id"

######################################################################################3

apikey = r"your api key"
urlAPI = "https://imdb-api.com/en/API/"

# imdb API comands (urlAPI + amdb[command] + expression)
imdb = {
 "search" : 'Search/',  # expression = everything
 "keyword_search" : "Keyword/",  # expression = keyword(it'a a descriprion)
 "people" : "SearchName/",  # expression = name
 "company" : "SearchCompany/",  # expression = name
 "information_films" : "Title/", # expression = movie_id
 "information_pepole" : "Name/",  # expression = name_id
 "awards_films" : "Awards/",  # expression = movie_id
 "awards_pepole" : "NameAwards/",  # expression = name_id
 "rating" : "Ratings/",  # expression = movie_id
 "full_casts" : "FullCast/",  # expression = movie_id
 "posters" : "Posters/",  # expression = movie_id
 "images" : "Images/",  # expression = movie_id
 "trailers" : "Trailer/",  # expression = movie_id
 "YouTube_trailers" : "YouTubeTrailer/",  # expression = movie_id
 "external_sites" : "ExternalSites/",  # expression = movie_id
 "Wikipedia" : "Wikipedia/",  # expression = movie_id
 "user_reviews" : "Reviews/",  # expression = movie_id
 "FAQ" : "FAQ/",  # expression = movie_id
 "Top_250_movies" : "Top250Movies/",  # expression = nothing
 "Top_250_Series" : "Top250TVs/",  # expression = nothing
 "pop_100_movies" : "MostPopularMovies/",  # expression = nothing
 "pop_250_Series" : "MostPopularTVs/",  # expression = nothing
 "movies_in_theaters" : "InTheaters/"   # expression = nothing
}
###################################################################################

# This function checks the status of the bot.
# It sends a request to the Telegram API using the "getme" method, which returns information about the bot.
# The function then parses the response and returns the value of the "ok" field, which indicates whether the request was successful.
def bot_status(URL=urlBOT):
    # Construct the URL by appending the "getme" method to the base URL.
    URL = URL + commands['bot']
    # Send a GET request to the API using the constructed URL.
    bot_status = requests.get(URL)
    # Parse the response as JSON and store it in the "status" variable.
    status = bot_status.json()
    # Return the value of the "ok" field in the response, which indicates whether the request was successful.
    return status["ok"]
####################################################################################

# This function retrieves updates from a specified URL using the requests module.
# It takes in a URL parameter, which is set to a default value of "url".
def get_updates(URL= urlBOT):
  # Send a GET request to the API using the constructed URL and the "getUpdates" method.
  response = requests.get(URL + commands['update'])
  # Parse the response as JSON and store it in the "recived" variable.
  recived = response.json()
  # Return the parsed JSON data.
  return recived
#########################################################################################

# extracting update messages
# This function takes a dictionary containing some update messages.
# It extracts the relevant information from each message and returns a list of dictionaries,
# with each dictionary representing one message and containing its important details.
def extract_updates(recived):
    # Extract the 'result' key from the input dictionary
  results = recived['result']
  # updates = [{"update_id":update_id,"type":type message "chat_id":chat_id, "text":text}]
  updates = []
  # Loop over all the update messages in the 'results' list
  for result in results:
    # Create a new dictionary to store the important details of the current message
    update = {}
    # Get the 'update_id' key from the input dictionary and add it to the 'update' dictionary
    update["update_id"] = result['update_id']

    # If the current message is a new message
    if 'message' in result.keys():
      if "text" in result['message']:
        # Add the type, chat_id, and text of the message to the 'update' dictionary
        update["type"] = "message"
        update["chat_id"] = result['message']['chat']['id']
        update["text"] = result['message']['text']
        # saving important result in updates
        updates.append(update)
      else:
        # Add the type, chat_id, and text of the message to the 'update' dictionary
        update["type"] = "message"
        update["chat_id"] = result['message']['chat']['id']
        # saving important result in updates
        updates.append(update)


    # If the current message is an edited message
    elif "edited_message" in result.keys():
      if "text" in result['message']:
        # Add the type, chat_id, and text of the edited message to the 'update' dictionary
        update["type"] = "edited_message"
        update["chat_id"] = result['edited_message']['chat']['id']
        update["text"] = result['edited_message']['text']
        # Add the 'update' dictionary to the list of updates
        updates.append(update)
      else:
        # Add the type, chat_id, and text of the message to the 'update' dictionary
        update["type"] = "message"
        update["chat_id"] = result['message']['chat']['id']
        update["text"] = result['message']['text']
        # saving important result in updates
        updates.append(update)

    # If the current message is a callback query
    elif "callback_query" in result.keys():
      # Add the type, chat_id, and movie_id of the callback query to the 'update' dictionary
      update["type"] = "callback_query"
      update["chat_id"] = result["callback_query"]["message"]["chat"]["id"]
      update["callback_query"] = result["callback_query"]["data"]
      # Add the 'update' dictionary to the list of updates
      updates.append(update)
  # Return the list of updates
  return updates

#########################################################################################

# This function takes two parameters: 'URL' and 'update'.
# The 'URL' parameter is the base URL of the Telegram API endpoint, and the 'update' parameter is a dictionary containing information about a single update.
def ignore_update(URL, update):
  # Get the 'update_id' key from the input dictionary and assign it to a variable called 'update_id'
  update_id = update["update_id"]

  # Create a variable named 'command' that specifies the API method to be used when sending a request to the Telegram API endpoint
  command = commands['update']

  # Send a POST request to the Telegram API endpoint using the 'requests' library.
  # The URL for the request is constructed by concatenating the 'URL' parameter, the 'command' variable,
  # and a query string that includes an offset value equal to 'update_id + 1'.
  # The purpose of this request is to tell the API to ignore updates with the same or lower 'update_id',
  # since they have already been processed.
  # Assign the response of the server to the 'status' variable
  status = requests.post(URL + command + '?offset={}'.format(update_id + 1))

  # Return nothing
  return None

##########################################################################################

def send_msg(urlBOT, chat_id, message_index, type_msg):

    images = {
          "start" : "https://image.tmdb.org/t/p/original/7rvVWbvg0CuNzYigehTs0lRUCs8.jpg",
          "search_movie" : "https://image.tmdb.org/t/p/original/xnUN3JkvchTvOClcQBPzkmWm1Km.jpg",
          "search_people" : "https://m.media-amazon.com/images/M/MV5BNjEzNGNhNzgtYTk5NC00ZjU4LTljNGQtMWYxODU3NGNiODRkXkEyXkFqcGdeQXVyNjY1MTg4Mzc@._V1_Ratio1.5000_AL_.jpg",
          "help" : "https://image.tmdb.org/t/p/original/5N2UE5KXelFxhcMigyZ9N9CMqEc.jpg",
          "error" : "https://image.tmdb.org/t/p/original/rTlmMq5OzZbNuW1ue0EgllZHuAq.jpg"
    }

    if type_msg == "/start":
        image = images["start"]
        caption = f"Hello and welcome to our Telegram bot! Our bot provides a variety of functions such as searching for movies based on their titles, searching for actors, and many other features that you can choose from within the bot's commands.\nWe also offer a movie recommendation service where you can search for a movie that you really like and we will suggest similar movies for you to watch. So, if you're looking for a great movie to watch, our bot is the perfect place to start!\nPlease feel free to explore all the features in the bot and don't hesitate to contact us if you have any questions or feedback. We hope you enjoy using our bot!\n\n{bot_id}"

    elif type_msg == "/search_movie":
        image = images["search_movie"]
        caption = f"Welcome to the movie search section! Simply type in the name of the movie or TV show you're looking for and send it to us. We'll provide related results that include a summary and cast.\nIf you want more information about any result, please let us know, and we'll give you additional details.\nTo start a new search, choose search_movie in the command section of the bot. Thank you for choosing our bot to help you find great movies and TV shows!\n\n{bot_id}"

    elif type_msg == "/search_people":
        image = images["search_people"]
        caption = f"simply type the name of the person you are looking for in the chat section of the bot and send it. The bot will then show you a list of people who match your search criteria along with their pictures.\nIf you want to search for another person, simply click on the Commands section and select the Search_people command to start a new search.\nThank you for using our bot!\n\n{bot_id}"

    elif type_msg == "/help":
        image = images["help"]
        caption = f"Hello and welcome to our Telegram bot! Here's a list of all the commands you can use:\n\n1. /search_movie - Use this command followed by a movie name to get information about that movie.\n\n2. /search_people - Use this command followed by a celebrity's name to get information about that person.\n\n3. /top_movies - Use this command to get a list of the top 250 movies of all time according to IMDb.\n\n4. /help - Use this command to get a list of all available commands and their descriptions.\nWe hope you find these commands useful! Don't hesitate to reach out if you have any other questions. \n\n{bot_id}"

    elif type_msg == "error":
        image = images["error"]
        caption = f"I deeply apologize for any inconvenience caused by the recent technical issue. The problem was due to my excessive use of the chatbot, which resulted in the temporary restriction of your access. I understand this may have caused frustration and I'm taking all necessary steps to prevent this from happening again in the future. Your usage limit will be replenished within the next 24 hours. Thank you for your patience and understanding while we work to resolve this matter.  \n\n{bot_id}"


    else:
        image = images["error"]
        caption = f"Command not found. Please select your desired command from the commands section at the bottom.\n\n{bot_id}"

    # Create a dictionary 'display' and add 'chat_id', 'photo', and 'caption' to it
    display = {}
    display["chat_id"] = chat_id
    display["photo"] = image
    display["caption"] = caption

    # Get the command from the 'commands' dictionary and construct a URL with the BOT token and command
    command = commands["photo"]
    URL = urlBOT + command

    # Send a POST request to the constructed URL with the 'display' dictionary as data
    sending = requests.post(URL, display)

    # Convert the response JSON to a dictionary 'status'
    status = sending.json()

    # If the request was successful
    if status["ok"]:

      # Save information about the user's command into the 'users_command' dictionary
      users_command[chat_id] = {
        "message_index" : message_index,
        "user_command" : type_msg
      }

      # Get the message ID from the 'status' dictionary
      message_id = status["result"]["message_id"]

      # If the message ID is not already in the 'dict_message' dictionary values
      if message_id not in dict_message.values():

        # Add the message index and message ID as key-value pair to the 'dict_message' dictionary
        # {message_index : message_id}
        dict_message[message_index] = message_id

      # Print True and the user's command type
      print(True,type_msg)

    else:
      # If the request was not successful, print False and the message "send_msg"
      print(False, "send_msg")


################################################################################################

# Define a function 'command_handler' that takes in an update and message index as arguments
def command_handler(update, message_index):
  # Extract the chat ID and user command from the update dictionary
  chat_id = update["chat_id"]
  user_command = update["text"]

  # If the user command is not in the list of bot commands
  if user_command not in bot_commands:
    # Send a message with the "not_found" status using the 'send_msg' function
    status = send_msg(urlBOT, chat_id, message_index, "not_found")

  # If the user command is one of the first five bot commands
  elif user_command in bot_commands[0:5]:
    # Send a message with the user's command as the status using the 'send_msg' function
    status = send_msg(urlBOT, chat_id, message_index, user_command)

  # If the user command is none of the above
  else:
    # Call the 'top_movies_handler' function passing in the BOT URL, message index, and update as arguments
    top_movies_handler(urlBOT, message_index, update)


################################################################################################

# Define a function 'top_movies_handler' that takes in the BOT URL, message index, and update as arguments
def top_movies_handler(urlBOT, message_index, update):
  # Extract the chat ID and user command from the update dictionary
  chat_id = update["chat_id"]
  user_command = update["text"]
  # Set the initial value of index to 0
  index = 0

  # If the user command is '/top_movies'
  if user_command == "/top_movies":
    # Set the image and caption for the message
    image = "https://image.tmdb.org/t/p/original/9K63TQPGxBeqChSRNsyTGiEH0HL.jpg"
    caption = f"\n\n1. Top 250 IMDb movies: This is a list of the best movies according to people who've used the IMDb website. The list includes some of the most popular and highly acclaimed films ever made, as rated by users.\n\n2. Top 250 IMDb TV series: This is a list of the best TV shows according to people who've used the IMDb website. The list includes some of the most beloved and sought-after TV series, as rated by users.\n\n3. Most popular movies: This is a list of the movies that are currently getting the most attention from people on IMDb based on page views. The rankings can change daily and offer insight into what's currently trending in the world of movies.\n\n4. Most popular TV series: This is a list of the TV shows that are currently getting the most attention from people on IMDb based on page views. The rankings can change daily and provide insight into what's currently popular in the world of television.\n\nI hope this explanation is helpful!\n\n{bot_id}"

    # Create callback_query lists for each of the four categories
    # callback_query = [categgory, message_index, index, change_index]
    movie250 = [path["movie250"], message_index, index, 0]
    movie250_button_str = json.dumps(movie250)

    # callback_query = [categgory, message_index, index, change_index]
    series250 = [path["series250"], message_index, index, 0]
    series250_button_str = json.dumps(series250)

    # callback_query = [categgory, message_index, index, change_index]
    pop_movies = [path["pop_movies"], message_index, index, 0]
    pop_movies_button_str = json.dumps(pop_movies)

    # callback_query = [categgory, message_index, index, change_index]
    pop_series = [path["pop_series"], message_index, index, 0]
    pop_series_button_str = json.dumps(pop_series)

    # Creating a dictionary of buttons
    buttoms = [
        {"Top 250 IMDb movies" : movie250_button_str},
         {"Top 250 IMDb TV series" : series250_button_str},
         {"Most popular movies" : pop_movies_button_str},
         {"Most popular TV series" : pop_series_button_str}
         ]

    # Creating reply markup string using the reply_markup_maker function
    reply_markup_str = reply_markup_maker(buttoms)

    # Creating a dictionary to store display information such as chat_id, image, caption and reply_markup
    display = {}
    display["chat_id"] = chat_id
    display["photo"] = image
    display["caption"] = caption
    display["reply_markup"] = reply_markup_str

    # Setting the command and URL to send the display information
    command = commands['photo']
    URL = urlBOT + command

    # Sending the display information to the specified URL using the requests.post method
    sending = requests.post(URL, display)
    status = sending.json()

    # Checking if the message was sent successfully or not
    if status['ok']:
      # Saving user's current command for future use
      users_command[chat_id] = {
        "message_index" : message_index,
        "user_command" : user_command
                }

      # Storing the message_id in dict_message dictionary
      message_id = status["result"]["message_id"]
      if message_id not in dict_message.values():
        # {message_index : message_id}
        dict_message[message_index] = message_id
      # Printing True if the message was sent successfully
      print(True)

    else:
      # Printing False if the message was not sent successfully
      print(False, "top_movies_handler")

#########################################################################################

def generate_top_movies(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]
  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callback_query = [categgory, message_index, index, change_index]
  category = callback_query[0]
  message_index = callback_query[1]
  index = callback_query[2]
  change_index = callback_query[3]
  message_id = dict_message[message_index]

  if category not in global_datas:
      if category == path["movie250"]:
        URL = urlAPI + imdb["Top_250_movies"] + apikey

      elif category == path["series250"]:
        URL = urlAPI + imdb["Top_250_Series"] + apikey

      elif category == path["pop_movies"]:
        URL = urlAPI + imdb["pop_100_movies"] + apikey

      elif category == path["pop_series"]:
        URL = urlAPI + imdb["pop_250_Series"] + apikey

      response = requests.get(URL)
      top_results = response.json()

      if top_results["errorMessage"] == "":
        tops = top_results["items"]
        global_datas[category] = tops


  # if top in global
  tops = global_datas[category]

  index = index + change_index
  if index < 0 :
      index = len(tops) - 1
  elif index >= len(tops):
      index = 0

  top = tops[index]

  display = {}
  image = top["image"]
  rank = top["rank"]
  title = top["title"]
  year = top["year"]
  description = top["crew"]
  imDbRating = top["imDbRating"]
  movie_id = top["id"]
  page = f"{index+1}/{len(tops)}"

  caption = f"Rank: {rank}\n\n🎥 Title:\t {title} \nYear: {year}\n\n 🎞 Description:\n {description}\n\n imDbRating: {imDbRating}\n\n ✅ Result: \t {page}\n\n{bot_id} "

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # buttns
  # callback_query = [categgory, message_index, index, change_index]
  previous = [category, message_index, index, -1]
  previous_button_str = json.dumps(previous)

  # callback_query = [categgory, message_index, index, change_index]
  next = [category, message_index, index, 1]
  next_button_str = json.dumps(next)

  buttoms = [{"<  Previous": previous_button_str, "Next  >": next_button_str}]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  sending = requests.post(URL, data)
  status = sending.json()

  if status['ok']:
    print(True)

  else:
      print(False, "generate_top_movies")

##############################################################################################

def search_movie_handler(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]
  message_type = update["type"]

  # Get the search expression from the input dictionary and assign it to a variable called 'expression'
  if update["type"] != "callback_query":
    expression = update["text"]
    # {chat_id : {"message_id" : message_id, "user_cmd":  user_cmd}
    message_index = users_command[chat_id]["message_index"]
    message_id = dict_message[message_index]

    if expression not in searched_movies:
      # Create a URL for the search request using the 'urlAPI', 'apikey', and 'expression' variables.
      URL = urlAPI + 'Search/' + apikey + '/' + expression

      # Send a GET request to the specified URL using the 'requests' library,
      # and assign the response from the server to a variable named 'response'
      response = requests.get(URL)

      # Convert the response content to a JSON object using the '.json()' method,
      # and assign the result to a variable named 'search_results'
      search_results = response.json()

      # If there are no errors in the search results
      if search_results["errorMessage"] == "":
        # Get the list of search results from the search results dictionary
        search_data = []

        for result in search_results["results"]:
          if result["image"] != '' :
            search_data.append(result)
        #saving
        searched_movies[expression]= search_data

    #saving user activity
    if chat_id not in users:
      # users = {chat_id : {message_index : {category : expression/title}}}
      users[chat_id] = {message_index : {}}

    elif message_index not in users[chat_id]:
      users[chat_id][message_index] = {}
    # users = {chat_id : {message_index : {category : expression/title}}}
    #users[chat_id][message_index] = {"search_movie" : expression}
    users[chat_id][message_index]["search_movie"] = expression
    search_data = searched_movies[expression]
    movie_index = 0
    change_index = 0

  # handeling callback_query for search
  elif update["type"] == "callback_query":
    callback = update["callback_query"]
    # callback_query that we recived is str and we have to conver ir to dict
    callback_query = json.loads(callback)
    # callback_query = ["category", message_index, movie_index, change_index]
    message_index = callback_query[1]
    movie_index = callback_query[2]
    change_index = callback_query[3]
    message_id = dict_message[message_index]


    # users = {chat_id : {message_index : {category : expression/title}}}
    expression = users[chat_id][message_index]["search_movie"]
    search_data = searched_movies[expression]

  else:
    return False


  # Get the chat ID from the input dictionary and assign it to a variable called 'chat_id'

  if len(search_data) == 0:
    return send_msg(urlBOT, chat_id, message_index, "error")

  movie_index = movie_index + change_index

  if movie_index < 0 :
    movie_index = len(search_data) - 1
  elif movie_index >= len(search_data):
    movie_index = 0

  result = search_data[movie_index]

  title = result["title"]
  description = result["description"]
  movie_id = result["id"]
  page = f"{movie_index+1}/{len(search_data)}"
  caption = f"\n🎥 Title:\t {title} \n 🎞 Description:\n {description}\n ✅ Result for {(expression)}:  :\t {page}"

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  movie_information_buttom = [path["movie_info"], path["search_movie"], message_index, movie_id, movie_index]
  movie_information_buttom_str = json.dumps(movie_information_buttom)

  # callback_query = ["category", message_index, movie_index, change_index]
  previous = [path["search_movie"], message_index, movie_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callback_query = ["category", message_index, movie_index, change_index]
  next = [path["search_movie"], message_index, movie_index, 1]
  next_buttom_str = json.dumps(next)


  buttoms = [{"🔎 Movie Information 🔍" : movie_information_buttom_str}, {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str}]
  reply_markup_str = reply_markup_maker(buttoms)

  image = result["image"]

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "search_movie_handler")

###############################################################################################

def more_info_movie_result(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  callback_query = json.loads(callback)
  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  message_id = dict_message[message_index]
  movie_id = callback_query[3]
  movie_index = callback_query[4]
  command = imdb["information_films"]

  if movie_id not in more_info_movie_dict:
    imdbURL = urlAPI + command + apikey + '/' + movie_id
    response = requests.get(imdbURL)
    result = response.json()

    if result["errorMessage"] == "":
        if chat_id not in users:
          # users = {chat_id : {message_index : {category : expression/title}}}
          users[chat_id] = {message_index : {}}

        # saving movie
        more_info_movie_dict[movie_id]= result

    else:
      return send_msg(urlBOT, chat_id, message_index, "error")


  # users = {chat_id : {message_index : {category : expression/id}}}
  users[chat_id][message_index]["more_info_movie"] = movie_id
  result = more_info_movie_dict[movie_id]


  title = result["title"]
  imDbRating = result["imDbRating"]
  genres = result["genres"]
  typ = result["type"]
  description = result["keywords"]
  award = result["awards"]

  image = result['image']
  caption = f"\n🎬 Title:\t {title} \n\n🎞Type:\t {typ}\n\n🎭 Genres:\t {genres}\n\nIMDB Rating:\t  {imDbRating} \n\n🏆 Awards:\t {award}\n\n💫 Description:\t {description}\n\n {bot_id} "
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callquery = ["category", "last_category", message_index, movie_index, actor_index, change_actor_index]
  actors = [path["actors"], path["movie_info"], message_index, movie_index, 0, 0]
  actors_buttom_str = json.dumps(actors)

  # callback_back_query = ["category", "last_category", message_index, movie_index]
  plot = [path["plot"], path["movie_info"], message_index, movie_index]
  plot_buttom_str = json.dumps(plot)


  # callquery = ["category", "last_category", message_index, movie_index, person_index, change_person_index]
  writers = [path["writers"], path["movie_info"], message_index, movie_index, 0, 0]
  writers_buttom_str = json.dumps(writers)

  # callquery = ["category", "last_category", message_index, movie_index, person_index, change_person_index]
  directors = [path["directors"], path["movie_info"], message_index, movie_index, 0, 0]
  directors_buttom_str = json.dumps(directors)


  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  trailer = [path["trailer"], path["movie_info"], message_index, movie_id, movie_index]
  trailer_buttom_str = json.dumps(trailer)


  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  images = [path["images"], path["movie_info"], message_index, movie_id, movie_index]
  images_buttom_str = json.dumps(images)

  # callquery = ["category", "last_category", message_index, movie_index, similar_index. change_similar_index]
  similars = [path["similars"], path["movie_info"], message_index, movie_index, 0, 0]
  similars_buttom_str = json.dumps(similars)

  # callback_back_query = ["category", "last_category", message_index, movie_index]
  finance = [path["finance"], path["movie_info"], message_index, movie_index]
  finance_buttom_str = json.dumps(finance)

  # callback_query = ["category", message_index, movie_index, change_index]
  #rturn = [last_category, message_index, movie_index, 0]
  #rturn_buttom_str = json.dumps(rturn)
  # making buttoms
  buttoms = []
  # first line
  firstline = {}
  if len(result["actorList"]) > 0:
    firstline["Actors and Actresses"] = actors_buttom_str
  if len(firstline) > 0:
    buttoms.append(firstline)

  #second line
  buttoms.append({"Trailer": trailer_buttom_str, "Images": images_buttom_str})

  #third ;ome
  thirdline = {}
  if len(result["writerList"]) > 0:
    thirdline["Writers"] = writers_buttom_str

  if len(result["similars"]) > 0:
    thirdline["Similars"] = similars_buttom_str

  if len(result["directorList"]) > 0:
    thirdline["Directors"] = directors_buttom_str
  #adding buttoms in second line that exist in our data
  if len(thirdline) > 0:
    buttoms.append(thirdline)

  # third line buttons
  fourhtline = {}
  if len(result["boxOffice"]) > 0:
    fourhtline["Finance"] = finance_buttom_str

  if len(result["plot"]) > 0:
    fourhtline["Plot"] = plot_buttom_str

  if len(fourhtline) > 0:
    buttoms.append(fourhtline)

  # str mikonim
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
              "chat_id" : chat_id,
              'message_id' : message_id,
              "media" : media,
              "reply_markup" : reply_markup_str
          }

  # sending as edit message
  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()

  if check['ok']:
          print(True)
        # Otherwise, print 'False'
  else:
          print(False, movie_id)

##############################################################################################

def search_people_handler(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]
  message_type = update["type"]

  # Get the search expression from the input dictionary and assign it to a variable called 'expression'
  if update["type"] != "callback_query":
    expression = update["text"]
    # {chat_id : {"message_id" : message_id, "user_cmd":  user_cmd}
    message_index = users_command[chat_id]["message_index"]
    message_id = dict_message[message_index]

    if expression not in searched_people:
      # Create a URL for the search request using the 'urlAPI', 'apikey', and 'expression' variables.
      URL = urlAPI + imdb["people"] + apikey + '/' + expression

      # Send a GET request to the specified URL using the 'requests' library,
      # and assign the response from the server to a variable named 'response'
      response = requests.get(URL)

      # Convert the response content to a JSON object using the '.json()' method,
      # and assign the result to a variable named 'search_results'
      search_results = response.json()

      # If there are no errors in the search results
      if search_results["errorMessage"] == "":
        # Get the list of search results from the search results dictionary
        search_data = []

        for result in search_results["results"]:
          if result["image"] != '' :
            search_data.append(result)
        # saving
        searched_people[expression]= search_data

      else:
        return send_msg(urlBOT, chat_id, message_index, "error")

    # sving history of user
    if chat_id not in users:
      # users = {chat_id : {message_index : {category : expression/title}}}
      users[chat_id] = {message_index : {}}

    elif message_index not in users[chat_id]:
      users[chat_id][message_index] = {}
      # users = {chat_id : {message_index : {category : expression/title}}}
    users[chat_id][message_index]["search_people"] = expression

    search_data = searched_people[expression]
    people_index = 0
    change_index = 0

  # handeling callback_query for search
  elif update["type"] == "callback_query":
    callback = update["callback_query"]
    # callback_query that we recived is str and we have to conver ir to dict
    callback_query = json.loads(callback)
    # callback_query = ["category", message_index, people_index, change_index]
    message_index = callback_query[1]
    people_index = callback_query[2]
    change_index = callback_query[3]
    message_id = dict_message[message_index]


    # users = {chat_id : {message_index : {category : expression/title}}}
    expression = users[chat_id][message_index]["search_people"]
    search_data = searched_people[expression]

  else:
    return False


  # Get the chat ID from the input dictionary and assign it to a variable called 'chat_id'

  if len(search_data) == 0:
    return send_msg(urlBOT, chat_id, message_index, "error")

  people_index = people_index + change_index

  if people_index < 0 :
    people_index = len(search_data) - 1
  elif people_index >= len(search_data):
    people_index = 0

  result = search_data[people_index]

  title = result["title"]
  description = result["description"]
  people_id = result["id"]
  page = f"{people_index+1}/{len(search_data)}"
  caption = f"\n🎥 Title:\t {title} \n 🎞 Description:\n {description}\n ✅ Result for {(expression)}:  :\t {page}"

  # callback_query = ["category", "last category", message_index, people_id, people_index]
  people_information_buttom = [path["people_info"], path["search_people"], message_index, people_id, people_index]
  people_information_buttom_str = json.dumps(people_information_buttom)

  # callback_query = ["category", message_index, movie_index, change_index]
  previous = [path["search_people"], message_index, people_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callback_query = ["category", message_index, movie_index, change_index]
  next = [path["search_people"], message_index, people_index, 1]
  next_buttom_str = json.dumps(next)

  buttoms = [{"🔎 People Information 🔍" : people_information_buttom_str}, {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str}]
  reply_markup_str = reply_markup_maker(buttoms)

  image = result["image"]

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "search_people_handler")

##############################################################################################

def more_info_people_result(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  callback_query = json.loads(callback)

  # callback_query = ["category", "last category", message_index, people_id, people_index]
  category = callback_query[0]
  last_category = callback_query[1]
  command = imdb["information_pepole"]
  message_index = callback_query[2]
  people_id = callback_query[3]
  people_index = callback_query[4]

  if last_category != path["search_people"]:
    movie_index = callback_query[5]

  message_id = dict_message[message_index]

  if people_id not in searched_people:
    imdbURL = urlAPI + command + apikey + '/' + people_id
    response = requests.get(imdbURL)
    result = response.json()

    if result["errorMessage"] == "":
        if chat_id not in users:
          # users = {chat_id : {message_index : {category : expression/title}}}
          users[chat_id] = {message_index : {}}

        # saving person
        searched_people[people_id]= result

    else:
      return False

  # users = {chat_id : {message_index : {category : expression/id}}}
  users[chat_id][message_index]["more_info_people"] = people_id
  result = searched_people[people_id]

  person_name = result["name"]
  person_image = result["image"]
  person_summary = result["summary"]
  person_birthDate = result["birthDate"]
  person_deathDate = result["deathDate"]

  if person_deathDate == None:
    person_deathDate = "is alive"

  person_awards = result["awards"]
  person_height = result["height"]
  person_castMovies = result["castMovies"]

  # making capriom
  detacher = "-"*50

  header = f"\nName:\t {person_name} \n\nBirth Date:\t {person_birthDate}\n\nDeath Date:\t {person_deathDate}\n\nHeight:\t  {person_height} \n"
  body = f" \n✨ Summary: \n{person_summary}\n\n 🏆 Awards:\t {person_awards}\n\n  "

  caption = header + detacher + body + detacher

  media = f'{{"type":"photo", "media":"{person_image}", "caption":"{caption}"}}'

  # making buttoms
  # callback_query = ["category", "last category", message_index, people_id, people_index, best_index, change_best_index]
  best_works = [path["bests"], category, message_index, people_id, people_index, 0, 0]
  best_works_str = json.dumps(best_works)

  if last_category != path["search_people"]:
    # callback_query = ["category", "last category", message_index, people_id, people_index, change_index, best_index, change_best_index, movie_index]
    best_works = [path["bests"], category, message_index, people_id, people_index, 0, 0, movie_index]
    best_works_str = json.dumps(best_works)

  buttoms = []
  if len(result["knownFor"]) != 0:
    buttoms.append({"Best Works" : best_works_str})

  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "more_people_handler")

###########################################################################################

def actors_results(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

 # callquery = ["category", "last_category", message_index, movie_index, actor_index, change_actor_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_index = callback_query[3]
  actor_index = callback_query[4]
  change_actor_index = callback_query[5]

  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  data = more_info_movie_dict[movie_id]
  actors = data["actorList"]

  actor_index = actor_index + change_actor_index
  if actor_index < 0 :
    actor_index = len(actors) - 1
  elif actor_index >= len(actors):
    actor_index = 0

  actor = actors[actor_index]

  # display
  image = actor["image"]
  name = actor["name"]
  asCharacter = actor["asCharacter"]
  people_id = actor["id"]
  page = f"{actor_index+1}/{len(actors)}"

  caption = f"\n Name:  {name} \n🎭 As Character:  {asCharacter}\n ✅ Result for actors: {page} "

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'


  # callback_query = ["category", "last category", message_index, people_id, people_index, movie_index]
  read_more_buttom = [path["people_info"], path["actors"], message_index, people_id, actor_index, movie_index]
  read_more_buttom_str = json.dumps(read_more_buttom)

  # callquery = ["category", "last_category", message_index, movie_index, actor_index, change_actor_index]
  previous = [path["actors"], path["actors"], message_index, movie_index, actor_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_index, actor_index, change_actor_index]
  next = [path["actors"], path["actors"], message_index, movie_index, actor_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["actors"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)


  buttoms = [
      {"🔎 Read More 🔍" : read_more_buttom_str},
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
        {"<<   Rrturn" : rturn_buttom_str}
        ]
  reply_markup_str = reply_markup_maker(buttoms)


  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, "actors_results")

###############################################################################################

def writers_or_directors_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

 # callquery = ["category", "last_category", message_index, movie_index, person_index, change_person_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_index = callback_query[3]
  person_index = callback_query[4]
  change_person_index = callback_query[5]

  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  result = more_info_movie_dict[movie_id]

  if category == path["writers"]:
    title = "Writers"
    output_ls = result["writerList"]

  else :
    title = "Directors"
    output_ls = result["directorList"]

  person_index = person_index + change_person_index
  if person_index < 0 :
    person_index = len(output_ls) - 1
  elif person_index >= len(output_ls):
    person_index = 0

  output = output_ls[person_index]
  name = output["name"]
  person_id = output["id"]

  page = f"{person_index+1}/{len(output_ls)}"


  image = result['image']
  caption  = f"{title}\n\nName:\n {name}\n\n✅ Result for actors: {page}  "
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callback_query = ["category", "last category", message_index, people_id, people_index, movie_index]
  read_more_buttom = [path["people_info"], category, message_index, person_id, person_index, movie_index]
  read_more_buttom_str = json.dumps(read_more_buttom)

  # callquery = ["category", "last_category", message_index, movie_index, person_index, change_actor_index]
  previous = [category, category, message_index, movie_index, person_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_index, person_index, change_actor_index]
  next = [category, category, message_index, movie_index, person_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], category, message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttons = [
          {"🔎 Read More 🔍" : read_more_buttom_str},
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
      {"<<   Rrturn" : rturn_buttom_str}
  ]
  reply_markup_str = reply_markup_maker(buttons)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False)

###############################################################################################

def plot_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

 # callquery = ["category", "last_category", message_index, movie_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_index = callback_query[3]

  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  result = more_info_movie_dict[movie_id]

  plot = result["plot"]
  duration = result["runtimeStr"]
  countries = result["countries"]
  languages = result["languages"]
  runtime = result["runtimeStr"]


  image = result['image']
  caption  = f"\n▶ Plot:\n {plot}\n\n ⏱ Duration:\t{duration}\n\n  🔊 languages:\t {languages}\n\n🏷 Countries:{countries}\n\n "
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["actors"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttons = [
      {"<<   Rrturn" : rturn_buttom_str}
  ]
  reply_markup_str = reply_markup_maker(buttons)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False)

#############################################################################################

def finance_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

 # callquery = ["category", "last_category", message_index, movie_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_index = callback_query[3]

  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  result = more_info_movie_dict[movie_id]

  box = result["boxOffice"]
  companies = result["companies"]
  budget = box["budget"]
  openingWeekendUSA = box["openingWeekendUSA"]
  grossUSA = box["grossUSA"]
  cumulativeWorldwideGross = box["cumulativeWorldwideGross"]


  image = result['image']
  caption  = f"\n▶ Companies:\n{companies}\n\n💵Budget:\t{budget}\n\nOening Weekend USA:\t{openingWeekendUSA}\n\nGross USA:{grossUSA}\n\nCumulative Worldwide Gross:{cumulativeWorldwideGross}\n\n{bot_id} "
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["finance"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttons = [
      {"<<   Rrturn" : rturn_buttom_str}
  ]
  reply_markup_str = reply_markup_maker(buttons)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False)

##############################################################################################

def trailer_result(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  category = callback_query[0]
  last_category = callback_query[1]
  command = imdb["trailers"]
  message_index = callback_query[2]
  movie_id = callback_query[3]
  movie_index = callback_query[4]

  message_id = dict_message[message_index]

  if movie_id not in trailer_movie_dict:
    imdbURL = urlAPI + command + apikey + '/' + movie_id
    response = requests.get(imdbURL)
    results = response.json()

    if results["errorMessage"] != "":
      return False

    # {mocvie_id : results}
    # saving movie
    trailer_movie_dict[movie_id] = results

  results = trailer_movie_dict[movie_id]

  title = results["fullTitle"]
  videostatus = results["videoTitle"]
  descruption = results["videoDescription"]
  trailer = results["linkEmbed"]
  date = results["uploadDate"]
  image = results["thumbnailUrl"]


  caption = f"\n🎬 Title:\t {title} \n\n🎞{videostatus}\n{trailer}\n\nDescruption:\t {descruption}\n\nDate:\t  {date}"
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["finance"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttoms = [{"<<  Return": rturn_buttom_str}]

  # str mikonim
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
              "chat_id" : chat_id,
              'message_id' : message_id,
              "media" : media,
              "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False)
##############################################################################################

def similars_results(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

 # callquery = ["category", "last_category", message_index, movie_index, similar_index. change_similar_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_index = callback_query[3]
  similar_index = callback_query[4]
  change_similar_index = callback_query[5]


  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  data = more_info_movie_dict[movie_id]
  similars = data["similars"]

  similar_index = similar_index + change_similar_index

  if similar_index < 0 :
    similar_index = len(similars) - 1
  elif similar_index >= len(similars):
    similar_index = 0

  similar = similars[similar_index]

  similar_id = similar["id"]
  title = similar["title"]
  image = similar["image"]
  imDbRating = similar["imDbRating"]

  page = f"{similar_index+1}/{len(similars)}"

  caption = f"\n Title:  {title} \n\nIMDB Rating:  {imDbRating}\n ✅ Result for similars: {page} "

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  movie_information_buttom = [path["movie_info"], path["similars"], message_index, similar_id, movie_index]
  movie_information_buttom_str = json.dumps(movie_information_buttom)

 # callquery = ["category", "last_category", message_index, movie_index, similar_index. change_similar_index]
  previous = [path["similars"], path["similars"], message_index, movie_index, similar_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_index, similar_index, change_similar_index]
  next = [path["similars"], path["similars"], message_index, movie_index, similar_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["similars"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttoms = [
      {"🔎 Read More 🔍" : movie_information_buttom_str},
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
        {"<<   Rrturn" : rturn_buttom_str}
        ]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "similars_results")

##############################################################################################

def images_result(urlBOT, urlAPI, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_id = callback_query[3]
  movie_index = callback_query[4]

  movie_id = users[chat_id][message_index]["more_info_movie"]
  message_id = dict_message[message_index]

  # {mocvie_id : results}
  result = more_info_movie_dict[movie_id]

  # display
  image = result['image']
  title = result["title"]
  caption = f"\n Images for:\t {title} \n\n"
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}\n\n{bot_id}"}}'

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, poster_index, change_poster_index]
  posters_buttom = [path["posters"], path["images"], message_index, movie_id, movie_index, 0, 0]
  posters_buttom_str = json.dumps(posters_buttom)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  backstage_buttom = [path["backstage"], path["images"], message_index, movie_id, movie_index, 0, 0]
  backstage_buttom_str = json.dumps(backstage_buttom)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backdrops_index, change_backdrops_index]
  backdrops_buttom = [path["backdrops"], path["images"], message_index, movie_id, movie_index, 0, 0]
  backdrops_buttom_str = json.dumps(backdrops_buttom)

  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  rturn = [path["movie_info"], path["images"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  if movie_id not in images_movie_dict:
    command = imdb["images"]
    imdbURL = urlAPI + command + apikey + '/' + movie_id
    response = requests.get(imdbURL)
    results = response.json()

    if results["errorMessage"] != "":
      return False

    # {mocvie_id : results}
    # saving movie
    images_movie_dict[movie_id] = results


  if movie_id not in posters_movie_dict:
    command = imdb["posters"]
    imdbURL = urlAPI + command + apikey + '/' + movie_id
    response = requests.get(imdbURL)
    results = response.json()

    if results["errorMessage"] != "":
      return False

    # {mocvie_id : results}
    # saving movie
    posters_movie_dict[movie_id] = results


  results = images_movie_dict[movie_id]
  backstage = results["items"]

  results = posters_movie_dict[movie_id]
  posters = results["posters"]
  backdrops = results["backdrops"]

  # making buttons
  buttoms = []
  if len(posters) > 0:
    buttoms.append({"Posters" : posters_buttom_str})

  if len(backstage) > 0:
    buttoms.append({"Backstage" : backstage_buttom_str})

  if len(backdrops) > 0:
    buttoms.append({"Backdrops" : backdrops_buttom_str})

  buttoms.append({"<<  Return" : rturn_buttom_str})
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
      "chat_id" : chat_id,
      'message_id' : message_id,
      "media" : media,
      "reply_markup" : reply_markup_str
            }

  # sending as edit message
  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()

  if check['ok']:
          print(True)
        # Otherwise, print 'False'
  else:
          print(False)

###############################################################################################

def backstage_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_id = callback_query[3]
  movie_index = callback_query[4]
  backstage_index = callback_query[5]
  change_backstage_index = callback_query[6]

  message_id = dict_message[message_index]

  results = images_movie_dict[movie_id]
  images = results["items"]

  backstage_index = backstage_index + change_backstage_index

  if backstage_index < 0 :
    backstage_index = len(images) - 1
  elif backstage_index >= len(images):
    backstage_index = 0

  image = images[backstage_index]

  title = image["title"]
  picture = image["image"]
  page = f"{backstage_index+1}/{len(images)}"

  caption = f"\n Title:  {title} \n\n ✅ Result for similars: {page}"
  media = f'{{"type":"photo", "media":"{picture}", "caption":"{caption}"}}'

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  previous = [path["backstage"], path["backstage"], message_index, movie_id, movie_index, backstage_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  next = [path["backstage"], path["backstage"], message_index, movie_id, movie_index, backstage_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  rturn = [path["images"], path["backstage"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttoms = [
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
        {"<<   Rrturn" : rturn_buttom_str}
        ]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "backstage")

#############################################################################################

def posters_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, posters_index, change_posters_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_id = callback_query[3]
  movie_index = callback_query[4]
  posters_index = callback_query[5]
  change_posters_index = callback_query[6]

  message_id = dict_message[message_index]


  results = posters_movie_dict[movie_id]
  posters = results["posters"]

  posters_index = posters_index + change_posters_index

  if posters_index < 0 :
    posters_index = len(posters) - 1
  elif posters_index >= len(posters):
    posters_index = 0

  poster = posters[posters_index]

  title = results["title"]
  image = poster["link"]
  width = poster["width"]
  height = poster["height"]
  aspectRatio = poster["aspectRatio"]
  page = f"{posters_index+1}/{len(posters)}"

  caption = f"\n {title} posters \n\nWidth: {width}\nHeight: {height}\naApect Ratio: {aspectRatio}\n\n✅ Result for actors: {page}"
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  previous = [path["posters"], path["posters"], message_index, movie_id, movie_index, posters_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  next = [path["posters"], path["posters"], message_index, movie_id, movie_index, posters_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  rturn = [path["images"], path["posters"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttoms = [
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
        {"<<   Rrturn" : rturn_buttom_str}
        ]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "posters")

############################################################################################

def backdrops_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backdrops_index, change_backdrops_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  movie_id = callback_query[3]
  movie_index = callback_query[4]
  backdrops_index = callback_query[5]
  change_backdrops_index = callback_query[6]

  message_id = dict_message[message_index]

  results = posters_movie_dict[movie_id]
  backdrops = results["backdrops"]

  backdrops_index = backdrops_index + change_backdrops_index

  if backdrops_index < 0 :
    backdrops_index = len(backdrops) - 1
  elif backdrops_index >= len(backdrops):
    backdrops_index = 0

  poster = backdrops[backdrops_index]

  title = results["title"]
  image = poster["link"]
  width = poster["width"]
  height = poster["height"]
  aspectRatio = poster["aspectRatio"]
  page = f"{backdrops_index+1}/{len(backdrops)}"

  caption = f"\n {title} posters \n\nWidth: {width}\nHeight: {height}\naApect Ratio: {aspectRatio}\n\n✅ Result for actors: {page}"
  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  previous = [path["backdrops"], path["backdrops"], message_index, movie_id, movie_index, backdrops_index, -1]
  previous_buttom_str = json.dumps(previous)

  # callquery = ["category", "last_category", message_index, movie_id, movie_index, backstage_index, change_backstage_index]
  next = [path["backdrops"], path["backdrops"], message_index, movie_id, movie_index, backdrops_index, 1]
  next_buttom_str = json.dumps(next)

  # callback_query = ["category", "last_category", message_index, movie_id, movie_index]
  rturn = [path["images"], path["backdrops"], message_index, movie_id, movie_index]
  rturn_buttom_str = json.dumps(rturn)

  buttoms = [
       {"<  Previous": previous_buttom_str, "Next  >": next_buttom_str},
        {"<<   Rrturn" : rturn_buttom_str}
        ]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, check, "posters")

###############################################################################################

def best_works_result(urlBOT, update):
  chat_id = update["chat_id"]

  callback = update["callback_query"]
  # callback_query that we recived is str and we have to conver ir to dict
  callback_query = json.loads(callback)

  # callback_query = ["category", "last category", message_index, people_id, people_index, best_index, change_best_index]
  category = callback_query[0]
  last_category = callback_query[1]
  message_index = callback_query[2]
  people_id = callback_query[3]
  people_index = callback_query[4]
  best_index = callback_query[5]
  change_best_index = callback_query[6]
  movie_index = 0
  if len(callback_query) == 8:
    movie_index = callback_query[7]

  message_id = dict_message[message_index]

  data = searched_people[people_id]
  person_works = data["knownFor"]

  best_index = best_index + change_best_index
  if best_index < 0 :
    best_index = len(person_works) - 1
  elif best_index >= len(person_works):
    best_index = 0

  person_work = person_works[best_index]

  # display
  movie_id = person_work["id"]
  role = person_work["role"]
  title = person_work["title"]
  year = person_work["year"]
  image = person_work["image"]

  page = f"{best_index+1}/{len(person_works)}"

  caption = f"\ntitle:  {title} \nYear:   {year}\n🎭 Role:  {role}\n\n ✅ Result for actors: {page} "

  media = f'{{"type":"photo", "media":"{image}", "caption":"{caption}"}}'

  # making buttoms
  # callback_query = ["category", "last category", message_index, movie_id, movie_index]
  movie_information_buttom = [path["movie_info"], path["bests"], message_index, movie_id, 0]
  movie_information_buttom_str = json.dumps(movie_information_buttom)

  # callback_query = ["category", "last category", message_index, people_id, people_index, best_index, change_best_index]
  previous = [category, last_category, message_index, people_id, people_index, best_index, -1, movie_index]
  previous_buttom_str = json.dumps(previous)

  # callback_query = ["category", "last category", message_index, people_id, people_index, best_index, change_best_index]
  next = [category, last_category, message_index, people_id, people_index, best_index, 1, movie_index]
  next_buttom_str = json.dumps(next)


  # callback_query = ["category", "last category", message_index, people_id, people_index]
  rturn = [path["people_info"], path["bests"], message_index, people_id, people_index, movie_index]
  rturn_str = json.dumps(rturn)


  buttoms = [
            {"🔎 Movie Information 🔍": movie_information_buttom_str},
             {"<  previous" : previous_buttom_str, "next >" : next_buttom_str},
                {"<<<<  Return": rturn_str}
              ]
  reply_markup_str = reply_markup_maker(buttoms)

  data = {
    "chat_id" : chat_id,
    'message_id' : message_id,
    "media" : media,
    "reply_markup" : reply_markup_str
            }

  command = commands['edit_image']
  URL = urlBOT + command

  status = requests.post(URL, data)
  check = status.json()
  if check['ok']:
      print(True)
  else:
      print(False, "best")

#########################################################################################

# This function takes one parameter, 'buttoms', which is a list of dictionaries that specifies the text and callback data for each button.
def reply_markup_maker(buttoms):
  # Initialize an empty dictionary called 'reply_markup'
  reply_markup = {}

  # Initialize an empty list called 'keyboards'
  keyboards = []
  inline_keyboards = []

  # Loop over all the rows of buttoms
  for line in buttoms:
    # Create a new list to represent the current row of buttons
    row_buttons = []
    # Loop over all the buttons in the current row
    for button_text, callback_data in line.items():
      # Create a dictionary called 'button' that associates the button text with its corresponding callback data
      button = {"text": button_text, "callback_data": callback_data}
      # Append the 'button' dictionary to the list of buttons for the current row
      row_buttons.append(button)

    # Append the list of buttons for the current row to the list of rows
    inline_keyboards.append(row_buttons)

  # Associate the 'inline_keyboard' list with the 'inline_keyboard' key in the 'reply_markup' dictionary
  reply_markup["inline_keyboard"] = inline_keyboards

  # Convert the 'reply_markup' dictionary to a string using the json.dumps() method,
  # and assign the result to a variable named 'reply_markup_str'
  reply_markup_str = json.dumps(reply_markup)

  # Return the 'reply_markup_str' string
  return reply_markup_str

###########################################################################################