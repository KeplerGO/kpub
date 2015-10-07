Title: {{ title }}
Save_as: {{ save_as }}

[TOC]
{% for month in articles %}

{{ month }}
{{ "-" * month|length }}
{% for art in articles[month] %}
{{loop.index}}. [{{ art['title'][0].upper() }}](http://adsabs.harvard.edu/abs/{{ art["bibcode"] }})  
{{ ', '.join(art['author'][0:3]) }}{% if art['author']|length > 3 %}, et al.{% endif %}    
{{ art["year"] }}, {% if art["pub"] == "ArXiv e-prints" -%}
    pre-print
{%- elif 'REFEREED' in art["property"] -%}
    refereed
{%- elif 'NOT REFEREED' in art["property"] -%}
    not refereed
{%- endif -%}
{{ ' ([{bibcode}](http://adsabs.harvard.edu/abs/{bibcode}))'.format(**art) }}  
{% endfor -%}
{% endfor -%}