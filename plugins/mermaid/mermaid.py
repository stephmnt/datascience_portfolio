from nikola.plugin_categories import ShortcodePlugin # pyright: ignore[reportMissingImports]


class MermaidShortcode(ShortcodePlugin):
    name = "mermaid"

    def handler(self, site=None, data=None, lang=None, **kwargs):
        theme = kwargs.get("theme", "default")
        content = (data or "").strip()

        return (
            f'<div class="mermaid" data-theme="{theme}">\n'
            f'{content}\n'
            '</div>'
        )
