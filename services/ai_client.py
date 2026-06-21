"""
services/ai_client.py
Project summary service.
Provides project summaries and next-step suggestions using local project data.
"""

class AIClient:
    def _build_project_context(self, project):
        stats = project.completion_summary()
        return stats

    def summarize_project(self, project):
        stats = self._build_project_context(project)
        return (
            f"Project: {project.title}\n"
            f"Owner: {project.owner_name}\n"
            f"Tasks Complete: {stats['complete']}/{stats['total']} "
            f"({stats['percent_done']}%)"
        )

    def suggest_next_step(self, project):
        incomplete = [t for t in project.tasks if str(t.status).lower() != "complete"]
        if incomplete:
            return f"Next step: Complete '{incomplete[0].title}'."
        return "Next step: Review project and plan new tasks."
