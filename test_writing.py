from writing import HandwritingApp
from unittest.mock import MagicMock, patch
from PIL import Image, ImageDraw
import tkinter as tk

def test_init():
    app = HandwritingApp()
    assert app.canvas_width == 400
    assert app.canvas_height == 300
    assert app.last_x is None
    assert app.last_y is None

@patch('PIL.Image.Image.save')
def test_save_image(mock_save):
    app = HandwritingApp()
    app.image = Image.new("RGB", (app.canvas_width, app.canvas_height), "white")
    app.save_image()
    mock_save.assert_called_once_with("handwriting.png")

def test_paint():
    app = HandwritingApp()
    app.canvas = MagicMock()
    app.draw = MagicMock()

    # First paint event: no previous points
    event = MagicMock()
    event.x, event.y = 50, 50
    app.paint(event)
    assert app.last_x == 50
    assert app.last_y == 50

    # Second paint event: should draw a line
    event.x, event.y = 100, 100
    app.paint(event)
    app.canvas.create_line.assert_called_once_with((50, 50, 100, 100), fill="black", width=5)
    app.draw.line.assert_called_once_with((50, 50, 100, 100), fill="black", width=5)

def test_reset():
    app = HandwritingApp()
    app.last_x, app.last_y = 50, 50
    app.reset(None)  # Event is not used
    assert app.last_x is None
    assert app.last_y is None

@patch('tkinter.Tk')
@patch('tkinter.Canvas')
@patch('tkinter.Button')
def test_writing_board(mock_button, mock_canvas, mock_tk):
    app = HandwritingApp()

    # Mock the existing root
    app.root = MagicMock()
    app.root.winfo_exists.return_value = True

    # Mock the destroy method
    app.root.destroy = MagicMock()

    # Mock the Tkinter components
    mock_instance = mock_tk.return_value
    mock_canvas_instance = mock_canvas.return_value

    # Call writing_board
    app.writing_board()

    # Check if root is created
    mock_tk.assert_called_once()
    mock_instance.title.assert_called_once_with("Answer")

    # Check if canvas is created and packed
    mock_canvas.assert_called_once_with(mock_instance, width=400, height=300, bg="white")
    mock_canvas_instance.pack.assert_called_once()

    # Check if save button is created and packed
    mock_button.assert_called_once_with(mock_instance, text="Save", command=app.save_image)
    mock_button.return_value.pack.assert_called_once()

    # Check if bindings are set
    mock_canvas_instance.bind.assert_any_call("<B1-Motion>", app.paint)
    mock_canvas_instance.bind.assert_any_call("<ButtonRelease-1>", app.reset)

