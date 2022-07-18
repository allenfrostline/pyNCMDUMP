source = ncmdump.py
ifeq ($(OS), Windows_NT)
	excutable = ncmdump.exe
else
	excutalbe = ncmdump
endif

$(excutable): $(source)
	pyinstaller $(source) -F && cp .\\dist\\$(excutable) .


.PHONY: clean
clean :
	-rm ./build -R
	-rm ./dist -R
