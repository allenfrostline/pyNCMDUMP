source = ncmdump.py
ifeq ($(OS), Windows_NT)
	excutable = ncmdump.exe
else
	excutable = ncmdump
endif

$(excutable): $(source)
	
	pyinstaller $(source) -F 
	rm ./$(excutable)
	cp ./dist/$(excutable) ./$(excutable)



.PHONY: clean
clean :
	-rm ./build -R
	-rm ./dist -R
