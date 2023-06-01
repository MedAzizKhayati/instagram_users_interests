import streamlit as st
import os
from PIL import Image
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
    display_interest()
    display_images()
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

def display_images():
    # Get file paths of images from your disk based on the test
    image_dir = "images/"
    image_files = get_image_files(image_dir)
    images = []
     # Create a grid layout with 3 columns
   
    if len(image_files) > 0:
        st.write("Displaying images:")
        cols = st.columns(len(image_files))
        
        # Display the images side by side in the grid layout
        for i, file in enumerate(image_files[:5]):  # Display the first 5 images
            image = Image.open(file)
            # Resize the image to 300x300 pixels
            image = image.resize((300, 300))

            # Display the image in the appropriate column
            with cols[i]:
                st.image(image, caption=file, use_column_width=True)
    else:
        st.write("No images found for the given test.")

def display_interest():
    st.markdown("### User interests")
    lst = ['a', 'b', 'c']

    for i in lst:
        st.markdown("- " + i)
    
def paginator(label, items, items_per_page=10, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.
        
    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    page_format_func = lambda i: "Page %s" % i
    page_number = location.selectbox(label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)
if __name__ == "__main__":
    main()
