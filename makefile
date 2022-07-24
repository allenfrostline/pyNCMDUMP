source = ncmdump.py
OS := $(shell uname)

ifeq ($(OS), Windows_NT)
	excutable = ncmdump.exe
else
	excutable = ncmdump
endif

command = pyinstaller $(source) -F

$(excutable): $(source)
	$(command)
	-rm ./$(excutable)
	cp ./dist/$(excutable) ./$(excutable)



.PHONY: clean
clean :
	-rm ./build -R
	-rm ./dist -R
