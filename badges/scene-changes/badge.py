from jinja2 import Template
from badges.badge import Badge
from util.github import find_changes

import os

template_path = os.path.join(os.path.dirname(__file__), "template.j2")
with open(template_path, "r") as file:
    template = Template(file.read())


class SceneChangesBadge(Badge):
    def __init__(self):
        super().__init__(id="scene-changes", label="Scene Changes")

    def create(self, owner: str, repo: str, args: dict) -> str:
        label = args.get("label", self.label)[:50]

        changes = find_changes(owner, repo, ".unity")

        # Iterates through all changes and finds conflicts between branches, conflicts are stored as a property of changes
        for branch, branch_data in changes.items():
            branch_scenes_modified = branch_data["scenes_modified"]
            changes[branch]["conflicts"] = []
            for compare_branch, compare_branch_data in changes.items():
                compare_branch_scenes_modified = compare_branch_data["scenes_modified"]
                if branch == compare_branch:
                    continue
                for scene in branch_scenes_modified:
                    if scene in compare_branch_scenes_modified:
                        changes[branch]["conflicts"].append(compare_branch)

        header_color = args.get("color", "#434343")
        body_color = "#555555"
        # Footer color is orange if any changes have conflicts, otherwise green
        footer_color = "orange" if any(
            len(change["conflicts"]) > 0 for _, change in changes.items()) else "lightgreen"
        
        table = template.render(header_content=label, changes=changes, header_color=header_color, body_color=body_color, footer_color=footer_color)
        return table