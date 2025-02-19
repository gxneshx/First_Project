A simple Telegram Bot made to test Python skills.

It has several functions:

1. Throws a random fact.
2. A classic ChatGPT interaction. Mostly in correspondence.
3. A dialog simulation with a famous person.
4. Quiz. 
   It doesn't work as expected though, unfortunately. 
   Sometimes, you receive questions and answers, and sometimes the behaviour is unpredictable. 
   It happens because of the prompt sent. Even ChatGPT itself doesn't understand why it doesn't work for him.
5. Translator. 
   The following languages: English, German, Italian, French, Spanish.
6. Voice ChatGPT. 
   One sends voice messages and receives voice answers from ChatGPT. Can be slow sometimes.
7. Movies, books, music recommendations. 
   As it states, the function recommends movies, books, or music. One needs to choose a theme first. 
   Then, you'll be asked to enter a genre. Then, the bot will send recommendations. 
   It can be extremely slow sometimes, brace yourselves. 
   Also, due to how AI chats interpret prompts, there will always be multiple recommendations.
8. Image recognizer. 
   Works with pictures and URLs. The maximum size of the picture must be 10 MB.
9. Curriculum Vitae generator. 
   One sends facts about themselves, career, etc. and get a quiet pretty generated CV based on the provided info. 

To get maximum profit of speaking with ChatGPT in different bot functions, you need to send one correct and structured message at a time.
If a message with mixed states or statements is sent, it can be interpreted incorrectly.
Therefore, simply, to get good and correct answers, you need to send the same condition questions. The other is up to you.

The bot requires a 'credentials.py' file in which a ChatGPT Token and a Telegram token should be listed under the variables ChatGPT_TOKEN and BOT_TOKEN, respectively. 
You can create the file manually or use the one from the repository. Don't forget to paste your token in this case then.

The main "bot.py" module is made the way that each Telegram Bot function realization is separated with two rows.
If functions in that module are separated with only one row, it means that the functions are within one logic realization and related to each other.

The bot is being developed and updated. Stand by.