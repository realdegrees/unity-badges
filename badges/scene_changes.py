from badge import Badge
from io import BytesIO
from PIL import Image
from badge_drawer import draw_badge, Cell
import os
from dotenv import load_dotenv
from util.github import find_changes


class SceneChangesBadge(Badge):
    def __init__(self):
        super().__init__(id="scene-changes", label="Scene Changes")

    def create(self, owner: str, repo: str, args: dict) -> Image:
        label = args.get("label", self.label)
        header_color = args.get("color", "#434343")

        changes = find_changes(owner, repo, ".unity")
        content = [[Cell("Branch"), Cell("Scene"), Cell("Status")]]
        filename_counts = {}
        for change in changes:
            filename = change["filename"]
            if filename in filename_counts:
                filename_counts[filename] += 1
            else:
                filename_counts[filename] = 1

        for change in changes:
            if filename_counts[change["filename"]] > 1:
                change["status"] = "❌"
            else:
                change["status"] = "✅"
        for change in changes:
            content.append([
                Cell(change["branch"]),
                Cell(change["filename"]),
                Cell(change["status"]),
            ])

        footer_color = "green" if not any(
            change["status"] == "conflict" for change in changes) else "orange"
        return draw_badge(label, content if len(content) > 1 else [], max_col_width=800, padding=15, footer_color=footer_color, header_color=header_color, body_color="#555555")
