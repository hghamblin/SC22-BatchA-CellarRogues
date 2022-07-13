# Need AI Caption?
## Created By: Anvita, Emanuele, Ivy, Matthew, Ronok, Zalea

### Description
This model will generate a social media caption based on user input. The model will ask the user to input a prompt, something that they would like to be included in the caption, and the model will generate a caption based on the prompt.



### Demo Video




### Datasets Used
The three datasets we used in our project are Instagram captions, song lyrics, and haiku poems. All of these datasets were found on Kaggle.



### Model Type
This generator is an GPT-2, natural language processing model.



### Challenges Faced
During the creation of our generator, one of the challenges was censoring profanity. In order for our model to be accessible to all ages without restrictions, we wanted our generator to negate the use of inappropriate language. Another major problem was the possible inappropriate use of emojis with a caption. We wanted to make sure that the emojis generated in the caption corresponded with the emotion being expressed. This meant that during preprocessing we had to figure out a way to censor profanity and make sure that corresponding emojis for the caption were being generated.



### Unique Features
Unique features in our model were sentiment analysis and check boxes for different types of captions. We used the sentiment analysis feature to generate appropriate emojis for each caption. It the sentiment value is greater than 0, the model will generate a happy emoji. If the sentiment value is less than zero, the caption will have a sad or mad emoji after it. Finally, if the sentiment level is equal to 0, it will output an emoji with a neutral expression. There are three options for the check boxes - captions generated from only the caption dataset, captions generated with the lyrics, haikus, and captions datasets, and an option to add emojis to the end of the caption. The user will have the option to select whichever options they would like their caption to have.



### Expansions
Our ideas to enhance this model are to incorporate computer vision aspects and find a way to generate hashtags that relate to the caption. Using computer vision, we would like to create a model that would allow the user to upload their image/post of choice and generate a caption without having the user type in a prompt. This way the captions generated will relate to the exact image the user would like to post.



### Example Outputs


