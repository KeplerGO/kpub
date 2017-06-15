import kpub


def test_annual_count():
    # Does the cumulative count match the annual count?
    db = kpub.PublicationDB()
    annual = db.get_annual_publication_count()
    cumul = db.get_annual_publication_count_cumulative()
    assert annual['k2'][2010] == 0  # K2 didn't exist in 2010
    # The first K2 papers started appearing in 2014; the cumulative counts should reflect that:
    assert (annual['k2'][2014] + annual['k2'][2015]) == cumul['k2'][2015]
    assert (annual['k2'][2014] + annual['k2'][2015] + annual['k2'][2016]) == cumul['k2'][2016]
