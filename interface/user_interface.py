import streamlit as st
import os
from PIL import Image
import requests
import io
import numpy as np
import matplotlib.pyplot as plt


HOST = "https://graph.facebook.com/v16.0/"
TOKEN = "EAAkrxJG28MYBAIYTYDZAmZB2wPWTqzTPcM3HiS77aIFgkWadCAk26S06eHzGVqkezQujXXOH6mRoHOx77kYiqtK1oRuTMYhZChyNTZB22tuSfuyzK0sFv4CB9Ir3XDBOoIKd53Jt0649DTwiBpKmRpusqiuy5dtsk5XxuNFuUuDT7wMQbYrYI6ZBtB0rnp7ZA16zyMLwUfRUDQ7EBsdfP0"
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
        display_images(posts)
        display_interest(posts)

    # Add main content here


def get_image_files(directory):
    # Filter and return image files based on the test
    # You can modify this function based on your specific requirements
    image_files = []
    for file in os.listdir(directory):
        if file.endswith(".jpg") or file.endswith(".png"):
            # Check if the test matches the image file name or any other criteria

            image_files.append(os.path.join(directory, file))
    return image_files


def display_images(images):
    # Get file paths of images from your disk based on the test

    # Create a grid layout with 3 columns

    st.write("Displaying images:")
    cols = st.columns(len(images))
    i = 0
    # Display the images side by side in the grid layout
    for image in images:  # Display the first 5 images
        image[0] = image[0].resize((300, 300))

        # Display the image in the appropriate column
        with cols[i]:
            st.image(image[0], caption=image[1], use_column_width=True)
        i += 1


def display_interest(images, captions):
    st.markdown("### User interests")
    interests = predict_interest(images, captions)
    for i in interests:
        st.markdown("- " + i)


def predict_interest(images, captions):
    pass


def extract_datas(insta_user):
    # Extract data from the API
    json = get_instagram_user_details(insta_user)
    images = get_imgs(json)
    return images


def get_imgs(dataset, local=False, ext="jpg", video=False):
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


def get_random_images(images):
    # Randomly select five indices from the image array
    imgs = []
    # Display the randomly selected images
    for i in range(min(5, len(images))):
        image = images[i]
        imgs.append(image)
    return imgs


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

    pass


if __name__ == "__main__":
    main()
