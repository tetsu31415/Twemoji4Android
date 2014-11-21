# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# November 21, 2014
# Modified by tetsu31415

EMOJI = Twemoji
font: $(EMOJI).ttf

EMOJI_SVG = ./svg/

EMOJI_PNG128 = ./png/

EMOJI_BUILDER = ./emoji_builder.py
ADD_GLYPHS = ./add_glyphs.py
PUA_ADDER = ./nototools/map_pua_emoji.py

$(EMOJI_PNG128): $(EMOJI_SVG)
	@echo "Generating PNGs..."
	@mkdir -p "$(EMOJI_PNG128)"
	@for svg in "$(EMOJI_SVG)"/*.svg; do \
		base="`basename "$$svg"`"; \
		emoji="$${base//.svg}"; \
		echo "Generating $(EMOJI_PNG128)/$$emoji.png"; \
		rsvg-convert -w 128 -h 128 -f png "$$svg" -o "$(EMOJI_PNG128)/$$emoji.png"; \
	done


%.ttx: %.ttx.tmpl $(ADD_GLYPHS) $(EMOJI_PNG128)
	python $(ADD_GLYPHS) "$<" "$@" "$(EMOJI_PNG128)"

%.ttf: %.ttx
	@rm -f "$@"
	ttx "$<"

$(EMOJI).ttf: $(EMOJI).tmpl.ttf $(EMOJI_BUILDER) $(PUA_ADDER) $(EMOJI_PNG128)
	python $(EMOJI_BUILDER) -V $< "$@" $(EMOJI_PNG128)
	python $(PUA_ADDER) "$@" "$@-with-pua"
	mv "$@-with-pua" "$@"

clean:
	rm -f $(EMOJI).ttf $(EMOJI).tmpl.ttx $(EMOJI).tmpl.ttf
	rm -f -r $(EMOJI_PNG128)
	rm -f *.pyc
