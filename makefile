source = ncmdump.py
OS := $(shell uname)

ifeq ($(OS), Windows_NT)
	excutable = ncmdump.exe
else
	excutable = ncmdump
endif

ifeq ($(OS), Linux)
	command = python3 -m PyInstaller $(source) -F
else
	command = pyinstaller $(source) -F
endif

$(excutable): $(source)
	$(command)
	-rm ./$(excutable)
	cp ./dist/$(excutable) ./$(excutable)



.PHONY: clean
clean :
	-rm ./build -R
	-rm ./dist -R
