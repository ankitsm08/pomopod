class PomopodClientError(Exception):
  """Exception raised when the HTTP client request fails."""

  def __init__(self, status_code: int = 500, message: str = "Client request failed"):
    """
    Args:
      status_code (int): HTTP status code.
      message (str): The main error message.
    """
    self.status_code = status_code
    self.message = message
    super().__init__(f"{status_code}: {message}")


def handle_error(e: Exception) -> None:
  """Handle exceptions and print appropriate error message."""
  from rich import print as rprint

  if isinstance(e, PomopodClientError):
    rprint(f"[red]Error ({e.status_code}): {e.message}[/red]")
  else:
    rprint(f"[red]Unexpected error: {e}[/red]")
