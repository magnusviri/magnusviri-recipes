# magnusviri-recipes

[AutoPkg](https://github.com/autopkg/autopkg) recipes maintained by [github.com/magnusviri](https://github.com/magnusviri).

	autopkg repo-add https://github.com/magnusviri/magnusviri-recipes.git

This includes my com.github.magnusviri.processors/VariableFromPath.py processor.

- [My autopkg notes](http://magnusviri.com/autopkg-notes.html)

## Auditing

Audit everything

	find RecipeRepos/com.github.magnusviri.magnusviri-recipes/ -name '*.recipe' -exec autopkg audit {} ';'

[prepare for autopkg recipe auditing/](https://scriptingosx.com/2016/11/prepare-for-autopkg-recipe-auditing/)
