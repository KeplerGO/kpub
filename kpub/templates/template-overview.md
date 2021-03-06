Title: Publications
Save_as: publications.html

[TOC]

We request that scientific publications using data obtained from the Kepler
or K2 projects include one of the following acknowledgments:

*This paper includes data collected by the Kepler mission. Funding for
the Kepler mission is provided by the NASA Science Mission
directorate.*

*This paper includes data collected by the K2 mission. Funding for
the K2 mission is provided by the NASA Science Mission
directorate.*

## Publication database

The Guest Observer office curates a list of scientific publications
pertaining to Kepler and K2.
The database contains {{ metrics["publication_count"] }} publications,
of which {{ metrics["refereed_count"] }} are peer-reviewed.
It demonstrates the important impact of Kepler/K2 data
on astronomical research.

You can access the publication list by mission:

 * <a href="kpub-kepler.html">Kepler publications &raquo;</a>
 * <a href="kpub-k2.html">K2 publications &raquo;</a>

Or by topic:

 * <a href="kpub-exoplanets.html">Exoplanet publications &raquo;</a>
 * <a href="kpub-astrophysics.html">Astrophysics publications &raquo;</a>

You also can mine the database yourself by accessing a spreadsheet of the publications: [kepler-publications.xls](/data/kepler-publications.xls)

If you spot an error, such as a missing entry,
please get in touch or open an issue in the <a href="https://github.com/KeplerGO/kpub">GitHub repository</a> of the database.

Last update: {{ now.strftime('%d %b %Y') }}.

<hr/>

## Breakdown by year & mission

The graph below shows the number of publications as a function
of year and mission.
The publication count for Kepler is {{ metrics["kepler_count"] }}
while that of K2 is {{ metrics["k2_count"] }}.
The number of refereed papers is {{ metrics["kepler_refereed_count"]}} for Kepler and {{ metrics["k2_refereed_count"] }} for K2.

[![Publication rate by mission and year](/images/kpub/kpub-publication-rate-without-extrapolation.png)](/images/kpub/kpub-publication-rate-without-extrapolation.png)

<hr/>

## Number of authors

The entries in the publication database have been authored and co-authored
by a total of {{ metrics["author_count"] }} unique author names.
We define the author name at "last name, first initial".
Slight variations in the spelling may increase the number of unique names,
while common names with the same first initial may result in undercounting.

[![Number of Kepler and K2 papers and unique authors over time](/images/kpub/kpub-author-count.png)](/images/kpub/kpub-author-count.png)

<hr/>

## Breakdown by subject

Both Kepler and K2 data have been used for scientific applications
that reach far beyond exoplanet research.
While {{ metrics["exoplanets_count"] }} works relate to exoplanets
({{ "%.0f"|format(metrics["exoplanets_fraction"]*100) }}%),
a total of {{ metrics["astrophysics_count"] }}
pertain to other areas of astrophysics
({{ "%.0f"|format(metrics["astrophysics_fraction"]*100) }}%).

The graph below details the breakdown of K2 papers by science topic.

[![Publications by subject](/images/kpub/k2-science-piechart.png)](/images/kpub/k2-science-piechart.png)

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

Below we list the most-active authors, defined as those with six or more first-author publications in our database.

{% for author in most_active_first_authors %}
 * {{author[0]}} ({{ "%.0f"|format(author[1]) }} publications)
{% endfor -%}
