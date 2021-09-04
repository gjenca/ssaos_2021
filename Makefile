default: PQ.pdf cograph.pdf fg.pdf

.PRECIOUS: %.tex

%.pdf: %.tex
	xelatex -output-driver="xdvipdfmx -i dvipdfmx-unsafe.cfg -q -E" $(*F)
	pdfcrop $(*F).pdf
	mv -vf $(*F)-crop.pdf $(*F).pdf

%.tex: %.py graphs.tex rels.tex cdiagram.py
	python $(*F).py > $@

