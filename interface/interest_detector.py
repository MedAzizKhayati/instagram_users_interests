import numpy as np
import torch.nn as nn
import torch
from torchvision import transforms
import re
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
import torch.nn.functional as F 

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
all_interests= [
    'Fashion and Style',
    'Food and Dining',
    'Family and Relationships',
    'Sports and Fitness',
    'Entertainment',
    'Business and Industry',
    'Travel and Adventure',
    'Arts and Culture',
    'News',
    'Pets',
    'Technology and Gadgets'
]
cnn_label_mapper = [
    'Arts and Culture',
 'Entertainment',
 'Family and Relationships',
 'Fashion and Style',
 'Food and Dining',
 'News',
 'Pets',
 'Sports and Fitness',
 'Technology and Gadgets',
 'Travel and Adventure',
 'Business and Industry'
]
all_interests_idx = [all_interests.index(label) for label in cnn_label_mapper]

# Define the custom layer
class CustomTFBertMainLayer(tf.keras.layers.Layer):
    def __init__(self, *args, **kwargs):
        super(CustomTFBertMainLayer, self).__init__(*args, **kwargs)

    def call(self, inputs, **kwargs):
        # Implement the custom layer logic here
        pass

# Define the custom model for CNN
class Model(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super(Model, self).__init__()
        self.model = torch.hub.load(
            'pytorch/vision:v0.9.0', 'vgg11', weights=pretrained)
        self.model.classifier[6] = torch.nn.Linear(
            self.model.classifier[6].in_features, num_classes)
        self.model.fc = self.model.classifier[6]

    def forward(self, x):
        x = self.model(x)
        return x

# Fusion model
class FusionModel(nn.Module):
    def __init__(self, bert_model, cnn_model):
        super(FusionModel, self).__init__()
        self.bert_model = bert_model
        self.cnn_model = cnn_model

    def transform(self, image):
        # preprocessing
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomRotation(30),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Lambda(lambda x: transforms.functional.to_pil_image(x).convert('RGBA') if x.shape[0] == 4 else transforms.functional.to_pil_image(x)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])
        return transform(image)
    
    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        text = re.sub(r'#[A-Za-z0-9]+', '', text)
        text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
        # remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def prepare_data(self, input_text, tokenizer):
        input_text = self.clean_text(input_text)
        token = tokenizer.encode_plus(
            input_text,
            max_length=256, 
            truncation=True, 
            padding='max_length', 
            add_special_tokens=True,
            return_tensors='tf'
        )
        return {
            'input_ids': token.input_ids,
            'attention_mask': token.attention_mask,
        }

    def preprocess(self, image, caption):
        # Load and preprocess image
        image = self.transform(image)

        # Convert image to PyTorch tensor
        image = torch.tensor(np.array(image))

        # Load and preprocess text
        processed_data = self.prepare_data(caption, tokenizer)

        return image, processed_data

    def predict(self, posts):
        # Preprocess all images and texts
        image_inputs = []
        text_inputs = []
        X_input_ids = np.zeros((len(posts), 256))
        X_attn_masks = np.zeros((len(posts), 256))
        for i, (image, caption) in enumerate(posts):
            image_input, text_input = self.preprocess(image, caption)
            image_inputs.append(image_input)
            text_inputs.append(text_input)
            X_input_ids[i, :] = text_input['input_ids']
            X_attn_masks[i, :] = text_input['attention_mask']
        
        # Image inputs are PyTorch tensors, that we need to stack
        image_inputs = torch.stack(image_inputs)

        # Text inputs are tf tensors, that we need to stack 
        text_inputs = {
            'input_ids': X_input_ids,
            'attention_mask': X_attn_masks
        }

        # Predict
        preds = self.__predict(image_inputs, text_inputs)
        mean_preds = preds.mean(axis=0)
        print(mean_preds.shape)
        print(mean_preds)
        labels = [ 
            [all_interests[i], pred]
            for i, pred in enumerate(mean_preds) if pred
        ]
        labels.sort(key=lambda x: x[1], reverse=True)
        labels = [f"{label} - ({pred:.2f})" for label, pred in labels > 0.1][:3]
        return labels


    def __predict(self, image_inputs, text_inputs):
        # Get BERT predictions
        text_inputs = {
            'input_ids': text_inputs['input_ids'],
            'attention_mask': text_inputs['attention_mask']
        }
        bert_output = self.bert_model(text_inputs)
        bert_output = bert_output.cpu().numpy()

        # Get CNN predictions
        with torch.no_grad():
            cnn_preds = self.cnn_model(image_inputs)
            cnn_preds = F.softmax(cnn_preds, dim=1)
            
        # Use all_interests_idx to reorder the predictions, on axis 1
        cnn_preds = cnn_preds.cpu().numpy()[:, all_interests_idx]

        # # Get the fusion vector (Mean of the two vectors)
        fusion_vector = np.maximum(bert_output, cnn_preds)

        # Our vector is 2D
        return fusion_vector


# Register the custom layer
tf.keras.utils.get_custom_objects()['CustomTFBertMainLayer'] = CustomTFBertMainLayer

# Load the BERT model
with tf.keras.utils.custom_object_scope({'CustomTFBertMainLayer': CustomTFBertMainLayer}):
    interest_model = tf.keras.models.load_model('../artifacts/bert_interest_model.h5')
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

# Load the models that we will use for the fusion using ANN
cnn_model_ = torch.load('../artifacts/cnn_instagram.pt', map_location=device)

cnn_model = Model(len(all_interests))
cnn_model.load_state_dict(cnn_model_)
cnn_model = cnn_model.to(device)
cnn_model.eval()  # Set the model to evaluation mode

# Create the fusion model
interest_model = FusionModel(interest_model, cnn_model)