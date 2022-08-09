from textual.app import App
from textual.widgets import Static

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class MarginApp(App):
    CSS = """

    Screen {
        background: white;
        color: black;
    }
   
    Static {
        margin: 4 8;  
        background: blue 20%;  
        border: blue wide;
    }    
    
    """

    def compose(self):
        yield Static(TEXT)


app = MarginApp()