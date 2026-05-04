"""Template tags for star rating display."""
import math

from django import template

register = template.Library()


def _star_breakdown(rating, max_stars=5):
    """Return (full_count, half_flag, empty_count) using half-star rounding."""
    try:
        r = float(rating)
    except (TypeError, ValueError):
        r = 0.0
    if not math.isfinite(r):
        r = 0.0
    max_s = int(max_stars)
    r = max(0.0, min(float(max_s), r))
    halves = int(round(r * 2))
    halves = max(0, min(max_s * 2, halves))
    full = halves // 2
    half = halves % 2
    empty = max_s - full - half
    return full, bool(half), empty


@register.inclusion_tag('bookstore_app/includes/star_row.html')
def star_row(rating, max_stars=5, size='md'):
    """
    Render a row of stars (supports half stars via Font Awesome).
    size: 'sm' | 'md' | 'lg'
    """
    full, half, empty = _star_breakdown(rating, max_stars)
    return {
        'full_range': range(full),
        'half': half,
        'empty_range': range(empty),
        'size': size,
        'rating': rating,
        'max_stars': int(max_stars),
    }
