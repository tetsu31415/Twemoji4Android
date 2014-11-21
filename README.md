Twemoji4Android
===============

A tool that makes color emoji for Android from [Twemoji](https://github.com/twitter/twemoji).

# Requirements
* Python
* FontTools
* librsvg

# Usage
Run
```
$ make
```

# Licenses
### Twemoji4Android 
This software is licensed under the MIT License.  
See [LICENSE](LICENSE)

### noto
https://code.google.com/p/noto/  
Copyright 2013 Google, Inc. All Rights Reserved.  
Licensed under the Apache License, Version 2.0.  
See [LICENSE-NOTO](LICENSE-NOTO)

Resources that used in this software:
* nototools/
* color\_emoji/
* third\_party/color\_emoji/

I made the following changes to "add\_glyphs.py" and "emoji\_builder.py":
* The separator for combining characters was changed from "_" to "-".  
* Added glyphs for 0, …, 9, \#, U+20E3.  

### Twemoji
https://github.com/twitter/twemoji  
Copyright 2014 Twitter, Inc and other contributors   
Graphics are licensed under CC-BY 4.0: https://creativecommons.org/licenses/by/4.0/  
See [LICENSE-GRAPHICS](LICENSE-GRAPHICS)  

Resources that used in this software:
* svg/
