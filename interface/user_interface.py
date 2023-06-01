import streamlit as st
import os
from PIL import Image
import requests
import io
import numpy as np
import matplotlib.pyplot as plt
from interest_detector import interest_model


HOST = "https://graph.facebook.com/v16.0/"
TOKEN = "EAAkrxJG28MYBAJZBIGOYXHGjMuS8ZAuECKLpeQiLXsT8WzHI7ComTfzgNrb5S9ZB5DZAZBRFi88Wv3hMx7QHTZCnxui7SgzjCZBJZBwA6X0v3bVza0ZArrQleI4fIzvKXiAL1W4AK93sZB9s7XaCZBcePUiEDTmIyUJxh0JVvmINlPspPBQ3NX9g6HmeVlfH65MrfTQoYQb7vZBNmzVVLHxV25xL"
IG_ACCOUNT_ID = "17841458726840626"


def main():
    # Set page title
    st.set_page_config(page_title="Instagram users interest", layout="wide")
    # Render the sidebar
    render_sidebar()

    # Render the main content
    render_content()


def render_sidebar():
    st.sidebar.title("Instagram users interest")
    # Add sidebar content here


def render_content():
    st.title("User interest prediction")
    insta_user = st.text_input("Type an instagram username", "")
    if insta_user:
        posts = extract_datas(insta_user)
        display_interest(posts)
        display_images(posts)


def get_image_files(directory):
    # Filter and return image files based on the test
    # You can modify this function based on your specific requirements
    image_files = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".png"):
            # Check if the test matches the image file name or any other criteria

            image_files.append(os.path.join(directory, file))
    return image_files


def display_images(posts):
    # Get file paths of images from your disk based on the test
    # Create a grid layout with 4 columns
    st.write("Displaying images:")
    cols = st.columns(5)
    i = 0
    # Display the images in rows of 4
    for post in posts:
        post[0] = post[0].resize((300, 300))
        # Display the image in the appropriate column
        with cols[i % 5]:
            st.image(post[0], caption=post[1], use_column_width=True)
        
        # Increment the column index
        i += 1


def display_interest(posts):
    st.markdown("### User interests")
    interests = predict_interest(posts)
    for i in interests:
        st.markdown("- " + i)


def predict_interest(posts):
    return interest_model.predict(posts)


def extract_datas(insta_user):
    # Extract data from the API
    limit = 10
    json = get_instagram_user_details(insta_user, limit)
    images = get_imgs(json, limit=limit)
    return images


def get_imgs(dataset, local=False, ext="jpg", video=False, limit=6):
    img = None
    images = []
    posts = dataset["business_discovery"]["media"]["data"]
    try:
        for post in posts:
            if post.get("media_type", "") == "VIDEO" and not video:
                continue
            if not local:
                media_url = post["media_url"]
                caption = post["caption"]
                response = requests.get(media_url)
                img = response.content
                img = Image.open(io.BytesIO(img))
                images.append([img, caption])
    except Exception as e:
        print("Error: ", e)
    return images



def get_instagram_user_details(username, limit=6):
    url = f"""{HOST}{IG_ACCOUNT_ID}?fields=
    business_discovery.username({username}){{
        name,
        biography,
        followers_count,
        follows_count,
        media_count,
        profile_picture_url,
        media.limit({limit}){{
            media_type,
            media_url,
            timestamp,
            caption,
            comments_count,
            like_count
        }}}}
        &access_token={TOKEN}"""
    url = url.replace("\n", "").replace(" ", "")
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    main()
