"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

def enum(**args):
    """Enum."""
    return type("Enum", (), args)
