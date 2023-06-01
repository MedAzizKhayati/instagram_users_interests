import streamlit as st
import os
from PIL import Image
import requests
import io
import numpy as np
import matplotlib.pyplot as plt


HOST = "https://graph.facebook.com/v16.0/"
TOKEN = "EAANx1LUJPcYBAECAThWYdG9iRPJdR182r6UswLh9OWZAyAXACKs18MhJjEu2c9iA9fuoTTYEhuFBn0mwdGjE5n87bF3RqnwOdJWeZAZAlTzEfGhqgII4fuNNgtbBSeGTz7KD2iVkuZBqRqtN6cLfazSok8mmmYp33TOuzzjdFCfRCMp2RiJ3OIfFiLN4GtXD1f6JlU8FLaG3THQrfdOt"
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
        images, captions = extract_datas(insta_user)
        display_interest(images, captions)
        # display_images()
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
        i+=1


def display_interest(images, captions):
    st.markdown("### User interests")
    interests = compute_interest(images, captions)
    for i in interests:
        st.markdown("- " + i)


def compute_interest(images, captions):
    pass


def extract_datas(insta_user):
    # Extract data from the API
    json = {
        "business_discovery": {
            "name": "Nike",
            "biography": "Spotlighting athlete* and\xa0👟\xa0stories\n#BlackLivesMatter and #StopAsianHate",
            "followers_count": 295158500,
            "follows_count": 151,
            "media_count": 1134,
            "profile_picture_url": "https://scontent.ftun16-1.fna.fbcdn.net/v/t51.2885-15/285265415_157543166760141_7125906423211419857_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=86c713&_nc_ohc=XVAjDvQE66AAX-9x9aK&_nc_ht=scontent.ftun16-1.fna&edm=AL-3X8kEAAAA&oh=00_AfBQdKN0pOlWFnti9oPSQR-tK098OTzFfb7F6q73KIlQzw&oe=647E5693",
            "media": {
                "data": [
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                    {
                        "media_type": "CAROUSEL_ALBUM",
                        "media_url": "https://scontent.cdninstagram.com/v/t51.29350-15/350442700_635812141751378_1531557628601014694_n.jpg?_nc_cat=1&ccb=1-7&_nc_sid=8ae9d6&_nc_ohc=y71D5Otv7mwAX-huCG8&_nc_ht=scontent.cdninstagram.com&edm=AL-3X8kEAAAA&oh=00_AfAGd20I_t1cTnXUUUtOqOaDfcswq09m51ZlH3JCwwJL1w&oe=647E1EFE",
                        "timestamp": "2023-06-01T16:01:55+0000",
                        "caption": "The 2023 Be True Collection is here. Made in collaboration with designer and artist Zoe Schlacter (they/them), bold geometric patterns and swirling graphics serve as a celebration of the legends and dreamers of LGBTQIA+ communities and their legacies.\n\nAvailable now. Link in bio. 💃✨",
                        "comments_count": 435,
                        "like_count": 30590,
                        "id": "17990014702890528",
                    },
                ]
            },
        }
    }

    images = get_imgs(json)
    get_random_images(images)
    display_images(images)
    captions = get_captions(insta_user, json)
    return images, captions


def get_imgs(dataset, local=False, ext="jpg", video=False):
    img = None
    images = []
    posts = dataset["business_discovery"]["media"]["data"]
    n = 0
    try:
        for post in posts:
            if post.get("media_type", "") == "VIDEO" and not video:
                return None
            if not local:
                media_url = post["media_url"]
                caption  = post["caption"]
                response = requests.get(media_url)
                img = response.content
                img = Image.open(io.BytesIO(img))
                images.append([img, caption])

    except Exception as e:
        print("Error: ", e)
    return images


def get_random_images(images):
    # Randomly select five indices from the image array
    indices = np.random.choice(len(images), 5, replace=False)
    imgs = []
    # Display the randomly selected images
    for i in range(5):
        image = images[indices[i]]
        imgs.append(image)
    return imgs


def get_user_acc(insta_user):
    pass


def get_images(insta_user, json):
    pass


def get_captions(insta_user, json):
    pass


if __name__ == "__main__":
    main()
