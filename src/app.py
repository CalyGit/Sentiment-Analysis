from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import gradio as gr

# Requirements
model_path = f"Calistus/test_trainer"
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def sentiment_analysis(text):
    text = preprocess(text)

    # PyTorch-based models
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)
    
    # Format output dict of scores
    labels = ['Negative', 'Neutral', 'Positive']
    scores = {l:float(s) for (l,s) in zip(labels, scores_) }
    
    return scores

app = gr.Interface(
    fn=sentiment_analysis, 
    inputs=gr.Textbox(placeholder="Write your tweet here..."), 
    outputs="label", 
    interpretation="default",
    examples=[["Please don't listen to anyone. Vaccinate your child"],
              ['My kid has a lump on his hand because of the vaccine'],
             ['my church does not allow any form of vaccination']],
    title= 'Sentiment Analysis App',
    description= 'This app is designed to help you gauge the emotions and opinions expressed in text, particularly focusing on discussions related to measles vaccination on X(formerly Twitter). Simply input a tweet or any text, and the app will swiftly categorize it into one of three categories: Negative, Neutral, or Positive sentiment. ')

if __name__ == "__main__":
    app.launch()