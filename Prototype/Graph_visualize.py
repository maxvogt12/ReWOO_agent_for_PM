from IPython.display import Image
from PIL import Image


def graph_visualize_png(app):
    # Assuming 'app' is your compiled graph
    graph_image = app.get_graph().draw_png()

    # Save the image to a file
    with open("state_graph.png", "wb") as f:
        f.write(graph_image)

    # Open the saved image using the default image viewer
    Image.open("state_graph.png").show()

def graph_visualize_ASCII(app):
    # Printing ASCII version to terminal
    app.get_graph().print_ascii()


