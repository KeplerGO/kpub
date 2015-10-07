Title: Publication database
Save_as: publications.html

[TOC]

## Summary

The Guest Observer Office curates <a href="kpub.html">a database
of scientific publications</a> pertaining to Kepler and K2.
The database currently contains
{{ metrics["publication_count"] }} publications,
of which {{ metrics["refereed_count"] }} are peer-reviewed.
This page present a series of statistics
that demonstrate the important impact of Kepler/K2 data
on astronomical research.

Please contact us if you spot an error in the database,
such as a missing publication.

Last update: {{ now.strftime('%d %b %Y') }}.

<hr/>

## Breakdown by year & mission

The graph below shows the number of publications as a function
of year and mission.
The publication count for Kepler is {{ metrics["kepler_count"] }},
that of K2 is {{ metrics["k2_count"] }}.

![Publication rate by mission and year]({filename}/images/kpub/kpub-publication-rate.png)

<a href="kpub-kepler.html" class="btn btn-info btn-lg">
View all Kepler publications &raquo;
</a>
<a href="kpub-k2.html" class="btn btn-danger btn-lg">
View all K2 publications &raquo;
</a>
<a href="kpub.html" class="btn btn-default btn-lg">
View all publications &raquo;
</a>

<hr/>

## Breakdown by subject

Both Kepler and K2 data have been used for scientific applications
that reach far beyond exoplanet research.
While {{ metrics["exoplanets_count"] }} works relate to exoplanets
({{ "%.0f"|format(metrics["exoplanets_fraction"]*100) }}%),
a total of {{ metrics["astrophysics_count"] }}
pertain to other areas of astrophysics
({{ "%.0f"|format(metrics["astrophysics_fraction"]*100) }}%).


![Publications by subject]({filename}/images/kpub/kpub-piechart.png)

<a href="kpub-exoplanets.html" class="btn btn-warning btn-lg">
View all exoplanet publications &raquo;
</a>
<a href="kpub-astrophysics.html" class="btn btn-success btn-lg">
View all astrophysics publications &raquo;
</a>

<hr/>

## Most-cited publications

Kepler/K2 publications have cumulatively been cited
{{ metrics["citation_count"] }} times.
The list below shows the most-cited publications,
based on the citation count obtained from NASA ADS.

{% for art in most_cited %}
{{loop.index}}. {{art['title'][0].upper()}}  
{{ ', '.join(art['author'][0:3]) }}{% if art['author']|length > 3 %}, et al.{% endif %}    
{{ '[{bibcode}](http://adsabs.harvard.edu/abs/{bibcode})'.format(**art) }}
<span class="badge">{{ art['citation_count'] }} citations</span>
{% endfor -%}

<hr/>

<!-- 
## Most-read publications

The read count shown below is obtained from the ADS API
and indicates the number of times the article has been downloaded
within the last 90 days.

{% for art in most_read %}
{{loop.index}}. {{art['title'][0].upper()}}  
{{ ', '.join(art['author'][0:3]) }}{% if art['author']|length > 3 %}, et al.{% endif %}    
{{ '[{bibcode}](http://adsabs.harvard.edu/abs/{bibcode})'.format(**art) }}
<span class="badge">{{ "%.0f"|format(art['read_count']) }} reads</span>
{% endfor -%}

<hr/>

-->

## Most-active authors

The entries in the publication database have been authored and co-authored
by a total of {{ metrics["author_count"] }} unique author names.
Here we list the most-active authors, defined as those with six or more first-author publications in our database.

{% for author in most_active_first_authors %}
 * {{author[0]}} ({{ "%.0f"|format(author[1]) }} publications)
{% endfor -%}

