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
    # Are the values returned by get_metrics consistent?
    for year in range(2009, 2019):
        metrics = db.get_metrics(year=year)
        assert metrics['publication_count'] == annual['both'][year]
        assert metrics['kepler_count'] == annual['kepler'][year]
        assert metrics['k2_count'] == annual['k2'][year]
