db-update:
	kpub-update

db-push:
	kpub-export > data/kpub-export.csv
	git add data/kpub.db data/kpub-export.csv
	git commit -m "Regular db update"
	git push
