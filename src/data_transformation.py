def normalize_text(product_description):
    """Normalize Product Description into a dict object
    with pre-defined keys.

    Args:
        product_description (str): Product Description

    Returns:
        dict: normalized values of Product Description
    """
    
    try:
        words = product_description.split()
    except:
        return None
    
    return words