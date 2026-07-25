import json
from typing import Any, Generator, Optional

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from serpdive import SearchResponse, SerpDive, SerpDiveError


def _as_bool(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


def _as_max_results(value: Any) -> Optional[int]:
    """Coerces max_results to the API's accepted range (1-10), None when unset."""
    if value is None or value == "":
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return max(1, min(10, number))


class SerpdiveSearchTool(Tool):
    """
    A tool for searching the web through the SERPdive API.
    """

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("serpdive_api_key")
        if not api_key:
            yield self.create_text_message(
                "SERPdive API key is missing. Please set it in the provider credentials."
            )
            return

        query = str(tool_parameters.get("query") or "").strip()
        if not query:
            yield self.create_text_message("Please input a query.")
            return

        model = tool_parameters.get("model")
        if model not in ("krill", "mako", "moby"):
            model = None
        answer = _as_bool(tool_parameters.get("answer"))
        max_results = _as_max_results(tool_parameters.get("max_results"))

        try:
            with SerpDive(api_key=api_key) as client:
                response = client.search(
                    query,
                    model=model,
                    answer=True if answer else None,
                    max_results=max_results,
                )
        except SerpDiveError as e:
            yield self.create_text_message(f"SERPdive search failed: {e}")
            return

        if not response.results and not response.answer and not response.extra_info:
            yield self.create_text_message(f"No results found for '{query}'.")
            return

        # Return the verbatim API payload for downstream nodes
        yield self.create_json_message(response.raw)

        # Return a formatted markdown version of the same payload
        yield self.create_text_message(self._format_as_text(response))

    def _format_as_text(self, response: SearchResponse) -> str:
        """
        Formats the search response into markdown text.
        """
        output_lines = []

        if response.answer:
            output_lines.append(f"**Answer:** {response.answer}\n")

        if response.extra_info:
            output_lines.append(
                "**Direct answer data:**\n```json\n"
                + json.dumps(response.extra_info, ensure_ascii=False, indent=2)
                + "\n```\n"
            )

        for idx, result in enumerate(response.results, 1):
            title = result.title or "No Title"
            output_lines.append(f"# Result {idx}: [{title}]({result.url})\n")
            output_lines.append(f"**URL:** {result.url}\n")
            if result.date:
                output_lines.append(f"**Published:** {result.date}\n")
            if result.content:
                output_lines.append(f"**Content:**\n{result.content}\n")
            output_lines.append("---\n")

        return "\n".join(output_lines)
