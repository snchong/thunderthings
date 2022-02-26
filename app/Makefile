ThunderThings.app: ThunderThings.py thunderthingscomm.py setup.py tt.icns
	python setup.py py2app
	cp -r dist/ThunderThings.app .

tt.icns: tt_1024_x_1024.png
	mkdir tt.iconset
	sips -z 16 16 tt_1024_x_1024.png --out "tt.iconset/icon_16x16.png"
	sips -z 32 32     tt_1024_x_1024.png --out "tt.iconset/icon_16x16@2x.png"
	sips -z 32 32     tt_1024_x_1024.png --out "tt.iconset/icon_32x32.png"
	sips -z 64 64     tt_1024_x_1024.png --out "tt.iconset/icon_32x32@2x.png"
	sips -z 128 128   tt_1024_x_1024.png --out "tt.iconset/icon_128x128.png"
	sips -z 256 256   tt_1024_x_1024.png --out "tt.iconset/icon_128x128@2x.png"
	sips -z 256 256   tt_1024_x_1024.png --out "tt.iconset/icon_256x256.png"
	sips -z 512 512   tt_1024_x_1024.png --out "tt.iconset/icon_256x256@2x.png"
	sips -z 512 512   tt_1024_x_1024.png --out "tt.iconset/icon_512x512.png"
	cp tt_1024_x_1024.png tt.iconset/icon_1024x1024.png
	iconutil -c icns tt.iconset
	rm -R tt.iconset


clean:
	rm -rf tt.iconset build dist __pycache__ 

.PHONY: clean