update:
	kpub-update

push:
	kpub-export > data/kpub-export.csv
	git add data/kpub.db data/kpub-export.csv
	git commit -m "Regular db update"
	git push

refresh:
	# Update the metadata by re-fetching all entries from the ADS API
	# this will e.g. update the citation counts and bibcodes
	kpub-export > data/kpub-export.csv
	rm data/kpub.db
	kpub-import data/kpub-export.csv

