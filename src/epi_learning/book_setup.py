"""Kernel setup applied before every notebook executed by the book build.

Jupyter Book 1 ran this as ``nb_execution_pre_code``. Jupyter Book 2 (MyST)
has no such option, so ``scripts/build_book.py`` installs an IPython startup
file that calls :func:`configure_book_kernel` in every kernel the build
launches. Nothing here runs on Colab or in a local JupyterLab session: the
notebooks themselves stay unchanged and keep their own Colab setup cell.

What it does, in order:

1. ``chdir`` to the repository root so ``data/synthetic/...`` resolves
   (MyST starts each kernel in the notebook's own directory).
2. Register the installed CJK fonts and put them first in ``font.sans-serif``
   (see :func:`epi_learning.viz.configure_chinese_font`).
3. Apply the house matplotlib look: ``ggplot`` style at 150 dpi.
4. Make Plotly emit self-contained HTML that the static site can display.
"""

from __future__ import annotations

import os
from pathlib import Path

#: Plotly renderer used during the build. ``notebook`` embeds plotly.js in the
#: first figure's ``text/html`` output, so the chart renders on a static page
#: with no Jupyter frontend and no CDN request.
PLOTLY_RENDERER = "notebook"

#: Matplotlib figure resolution for the built site.
FIGURE_DPI = 150


def find_repo_root(start: Path, max_levels: int = 6) -> Path | None:
    """Return the closest ancestor of *start* that holds ``data/synthetic``.

    Parameters
    ----------
    start:
        Directory to start from (normally the kernel's working directory).
    max_levels:
        How many parent directories to inspect before giving up.

    Returns
    -------
    Path or None
        The repository root, or ``None`` when no ancestor within
        *max_levels* contains both ``pyproject.toml`` and ``data/synthetic``.
    """
    if max_levels < 0:
        raise ValueError(f"max_levels must be >= 0, got {max_levels}")
    candidate = start.resolve()
    for _ in range(max_levels + 1):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "data" / "synthetic"
        ).is_dir():
            return candidate
        if candidate.parent == candidate:
            break
        candidate = candidate.parent
    return None


def configure_matplotlib() -> None:
    """Apply CJK fonts, the ``ggplot`` style and the site figure dpi.

    The style is applied first because ``plt.style.use`` resets the font
    family list; the CJK fonts are then placed in front of it.
    """
    import matplotlib.pyplot as plt

    from epi_learning.viz import configure_chinese_font

    plt.style.use("ggplot")
    configure_chinese_font()
    plt.rcParams["figure.dpi"] = FIGURE_DPI


def configure_plotly() -> None:
    """Select :data:`PLOTLY_RENDERER` when Plotly is installed."""
    try:
        import plotly.io as pio
    except ImportError:
        return
    pio.renderers.default = PLOTLY_RENDERER


def configure_book_kernel(start: Path | None = None) -> Path | None:
    """Prepare a freshly started kernel for executing a book notebook.

    Parameters
    ----------
    start:
        Directory to search upward from; defaults to the current directory.

    Returns
    -------
    Path or None
        The directory the kernel switched to, or ``None`` if the repository
        root was not found (the working directory is then left unchanged).
    """
    root = find_repo_root(Path.cwd() if start is None else start)
    if root is not None:
        os.chdir(root)
    configure_matplotlib()
    configure_plotly()
    return root
