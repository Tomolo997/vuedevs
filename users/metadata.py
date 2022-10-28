from dataclasses import dataclass

@dataclass
class ProductMetadata(object):
    """
    Metadata for a Stripe product.
    """
    stripe_id: str
    name: str
    description: str = ''
    is_default: bool = False


STANDARD = ProductMetadata(
    stripe_id='price_1LeXROK8VMxCSHFy5cnOiYPh',
    name='standard',
    description='Hire freelance, contract or full-time django developers',
    is_default=True,
)