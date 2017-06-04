"""Test the basics of kpub's functionality."""

def test_import():
    """Can the module be imported without syntax errors?"""
    import kpub


def test_init():
    """Can we create a PublicationDB object and obtain the metrics?"""
    from kpub import PublicationDB
    db = PublicationDB()
    metrics = db.get_metrics()
    assert 'publication_count' in metrics
