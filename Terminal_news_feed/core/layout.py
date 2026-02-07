from textual.containers import Horizontal
from textual.events import Key
from textual.widget import Widget
from textual.widgets import ListItem, ListView, Static

from core.cache import load_cache, save_cache
from core.feeds import fetch_feeds


class FeedHeader(ListItem):
    def __init__(self, title: str):
        super().__init__(
            Static(
                f"\n[red]> [red][bold yellow]{title.upper()}[/bold yellow]", expand=True
            )
        )
        self.can_focus = False


class ArticleItem(ListItem):
    def __init__(self, article: dict):
        super().__init__(Static(f"\n[magenta]{article['title']}[magenta]", expand=True))
        self.article = article


class MainLayout(Widget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.items = []
        self.mode = "list"

        self.feed_list = ListView()
        self.content = Static("Select an article", expand=True)

    def compose(self):
        yield Horizontal(
            self.feed_list,
            self.content,
        )

    async def on_mount(self):
        self.feed_list.styles.width = "40%"
        self.feed_list.styles.min_width = 30
        self.content.styles.width = "60%"

        self.feed_list.styles.padding = (1, 2)
        self.content.styles.padding = (1, 2)

        self.content.update("Loading feeds...")
        await self.load_feeds()
        self.content.update("Select an article")

        self.feed_list.focus()

    async def refresh_feeds(self):
        await self.load_feeds()

    async def load_feeds(self):
        self.feed_list.clear()

        cached = load_cache()
        if cached:
            self.items = cached
        else:
            self.items = fetch_feeds(self.config["feeds"])
            save_cache(self.items)

        for item in self.items:
            if item["type"] == "header":
                self.feed_list.append(FeedHeader(item["title"]))
            else:
                self.feed_list.append(ArticleItem(item))

    async def on_list_view_selected(self, event: ListView.Selected):
        if hasattr(event.item, "article"):
            self.open_article(event.item.article)

    def open_article(self, article: dict):
        self.mode = "reader"
        summary = article.get("summary", "").strip()
        if not summary:
            summary = "No reader view available for this item.\n\nPress 'o' to open in browser."

        self.content.update(f"[cyan]{article.get('title','')}\n\n{summary}[/cyan]")
        self.content.focus()

    def back_to_list(self):
        self.mode = "list"
        self.feed_list.focus()

    async def on_key(self, event: Key):
        if self.mode == "list":
            if event.key == "j":
                self.feed_list.action_cursor_down()
            elif event.key == "k":
                self.feed_list.action_cursor_up()
            elif event.key in ("l", "enter"):
                item = self.feed_list.highlighted_child
                if item and hasattr(item, "article"):
                    self.open_article(item.article)
            elif event.key == "o":
                item = self.feed_list.highlighted_child
                if item and hasattr(item, "article"):
                    import webbrowser

                    webbrowser.open(item.article["link"])

        elif self.mode == "reader":
            if event.key == "h":
                self.back_to_list()
            elif event.key == "o":
                item = self.feed_list.highlighted_child
                if item and hasattr(item, "article"):
                    import webbrowser

                    webbrowser.open(item.article["link"])
