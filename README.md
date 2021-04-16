# magnusviri-recipes

[AutoPkg](https://github.com/autopkg/autopkg) recipes maintained by [github.com/magnusviri](https://github.com/magnusviri).

	autopkg repo-add https://github.com/magnusviri/magnusviri-recipes.git

This includes my com.github.magnusviri.processors/VariableFromPath.py processor.

The rest of this file is my AutoPkg notes.

## Various notes of mine

Getting png files from icns files:

	sips -s format png "path/to/file.icns" --out "path/to/file.png"

Getting the identifier for [CodeSignatureVerifier](https://github.com/autopkg/autopkg/wiki/Using-CodeSignatureVerification):

	codesign --display -r- --deep -v /path/to/.appBundle

## Auditing

Audit everything

	find RecipeRepos/com.github.magnusviri.magnusviri-recipes/ -name '*.recipe' -exec autopkg audit {} ';'

https://scriptingosx.com/2016/11/prepare-for-autopkg-recipe-auditing/