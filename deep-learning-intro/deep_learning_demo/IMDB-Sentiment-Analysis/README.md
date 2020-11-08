# IMDB-Sentiment-Analysis
Sentiment analysis on IMDB movie reviews using Rnns and Lstms in Tensorflow.

# Problem:

Given a written review of a movie, the system should determine the sentiment behind the review and classify it into either good or bad.


# Dataset:

IMDB Movie Reviews Dataset: The labeled data set consists of 50,000 IMDB movie reviews, specially selected for sentiment analysis. The sentiment of reviews is binary, meaning the IMDB rating < 5 results in a sentiment score of 0, and rating >=7 have a sentiment score of 1. No individual movie has more than 30 reviews. The 25,000 review labeled training set does not include any of the same movies as the 25,000 review test set. In addition, there are another 50,000 IMDB reviews provided without any rating labels.

### File descriptions:
- labeledTrainData - The labeled training set. The file is tab-delimited and has a header row followed by 25,000 rows containing an id, sentiment, and text for each review.  
- testData - The test set. The tab-delimited file has a header row followed by 25,000 rows containing an id and text for each review. Your task is to predict the sentiment for each one. 
- unlabeledTrainData - An extra training set with no labels. The tab-delimited file has a header row followed by 50,000 rows containing an id and text for each review. 
- sampleSubmission - A comma-delimited sample submission file in the correct format.

### Data fields:
- id - Unique ID of each review
- sentiment - Sentiment of the review; 1 for positive reviews and 0 for negative reviews
- review - Text of the review

Note: Most of our work will be on the 25k reviews contained in 'labeledTrainData' which is already uploaded in this repo.

Link: [IMDB_Movie_Reviews_Dataset](https://www.kaggle.com/c/word2vec-nlp-tutorial/data)

### Dataset Splitting:
- 20k reviews from 'labeledTrainData' were used for training.
- 1k reviews from 'labeledTrainData' were used for validation.
- 4k reviews from 'labeledTrainData' were used for testing.

# Preprocessing:

- **Clean text**: by removing extra spaces, numbers, making all letters lowercase, and removing special characters
- **Removing stop words**: removing some common stop words from the text that does not add much information regarding the sentiment.       (The stop words are dataset/stopwords.txt)
- **Tokenize the reviews**: by giving each word present in the dataset a unique number and replace the words with these numbers. 
  (When predicting a new review, if a word does not exist in the dataset and does not have a token it will be ignored)
- **Pad the sequences**: by unifying the length of every review (ex 200). Shorter reviews will be padded with 0, and longer ones will be    cut.


# Training Method:

- Used Recurrent neural nets with LSTM.

![cntk106a_model_s3](https://user-images.githubusercontent.com/6074821/46958649-9a799380-d09a-11e8-98c5-db285e002eed.png)

- Used Dropout regularization
- Used early stopping
- Used learning rate decay
- Used gradient clipping 
- Used Adam optimizer on training batches

- **Tensorflow graph:**

![png](https://user-images.githubusercontent.com/6074821/47013715-6fe61400-d148-11e8-9b1e-b4459f3a258e.png)


# Results:

- **These are the results achieved on a simple model of a single LSTM layer of 64 units and a single fully connected hidden layer of       size 64:** 
  
- **Train accuracy: 97%**
- **Validation accuracy: 89%**

![acc](https://user-images.githubusercontent.com/6074821/47013130-6b206080-d146-11e8-843a-4702718278ad.jpg)

- **Train cost: 0.027%**
- **Validation accuracy: 0.083%**

![cost](https://user-images.githubusercontent.com/6074821/47013191-9d31c280-d146-11e8-92f0-b8cc1865e4e1.jpg)

- **Prediction distribution over learning:**

![pred](https://user-images.githubusercontent.com/6074821/47013445-758f2a00-d147-11e8-8466-dd1086564d73.jpg)

- **Test accuracy: 89%**


# Usage:

Here we will discuss how to run the project, some implementational details, and variables to tweak to increase accuracy

### PreprocessData.py:
This is the first script you should run to make a .pickle file of the dataset. It cleans the data, removes stop words, tokinze, and     pad the sequences.

Variables that can be easily tweaked are:
- Stopwords (in dataset/stopwords.txt)
- Padding length 
- Size of training, validation, and test data

### TrainData.py:
This is the second script you should run to train the neural network on the dataset. The script will automatically save the best overall model even in different runs. It will be saved in best_model folder with a folder of the format 'lstm_sizes={},output_hidden_units={},time={}' with the {} indicating variables in the code. All the information of the best overall model will be saved in an extra file called 'best_model_info.pickle' that also contains all the tensorboard logs to be viewed (best overall model is decided with best overall accuracy on test set). If you run a model that is not an overall best it will be saved in saved_model folder.

Variables that can be easily tweaked are:
- Word embedding size (when fed into the RNN)
- Batch size 
- Number of LSTM units (an array supporting stacking multiple lstm cells. Example: [64,128] will make two stacked LSTM cells with sizes   64 and 128)
- LSTM dropout output keep probability
- Number of fully connected hidden units (an array supporting adding multiple hidden layers. Example: [128,256] will add two hidden       layers with sizes 128 and 256)
- Fully connected dropout keep probability
- Starting learning rate
- Learning rate decay ratio
- Gradient clipping 
- Maximum number of epochs
- Early stopping (The system only saves the best epoch when running a single model (The best loss on validation set) )
- Activation functions
- Loss function

### PredictReview.py:
This script takes a review and automatically loads the best overall model to classify it into good or bad. It can be easily tweaked to load the n best models and avg their output. Before classifying the review it also cleans and tokenize the data (using same tokenizer used on the dataset).

# Future work:
- Add UI to prediction script
- Try bidirectional LSTMS
- Try using pretrained word embeddings

# Environment Used:
- Python 3.6.1
- Tensorflow 1.9
