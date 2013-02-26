SOURCE = "content"

build:
	python ford.py build $(SOURCE)

serve:
	python ford.py serve $(SOURCE)

qs:
	rm -rf content
	cp -r sample.content content
	python ford.py serve content
	
rqs:
	rm -rf content
	rm -rf sample.content
