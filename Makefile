
all: ThunderThings.app.zip ThunderThings.xpi

ThunderThings.app.zip:
	cd app && $(MAKE) ThunderThings.app &&zip -r -9 ../ThunderThings.app.zip ThunderThings.app

ThunderThings.xpi:
	cd add-on && zip -r -FS ../ThunderThings.xpi * --exclude '*.git*' '*~' '*.DS_Store'

.PHONY: all clean

clean:
	rm ThunderThings.app.zip ThunderThings.xpi
	cd app && $(MAKE) clean

