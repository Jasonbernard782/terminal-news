from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from core.config import load_config
from core.layout import MainLayout


class TerminalNews(App):
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()
        self.config = load_config()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield MainLayout(self.config)
        yield Footer()

    async def action_refresh(self):
        layout = self.query_one(MainLayout)
        await layout.refresh_feeds()


def main():
    app = TerminalNews()
    app.run()


if __name__ == "__main__":
    main()
