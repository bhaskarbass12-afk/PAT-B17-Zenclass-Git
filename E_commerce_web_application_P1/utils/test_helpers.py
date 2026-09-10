import random
from typing import Dict, List


def pick_random_products(
    products: List[Dict[str, str]], count: int = 4
) -> List[Dict[str, str]]:
    """Randomly selects `count` distinct products from `products`.

    Raises ValueError (instead of silently truncating) if there aren't
    enough products to satisfy the requested count, so a shrinking
    catalog surfaces as an obvious test failure rather than a quietly
    smaller sample.
    """
    if count > len(products):
        raise ValueError(
            f"Cannot select {count} products from a catalog of only {len(products)}"
        )
    return random.sample(products, count)
