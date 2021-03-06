# Intro to HPC 

This lesson is focused on teaching the basics of high-performance computing (HPC).

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fhpc-carpentry%2Fhpc-intro%2Fbadge%3Fref%3Dgh-pages&style=flat)](https://actions-badge.atrox.dev/hpc-carpentry/hpc-intro/goto?ref=gh-pages)

## Topic breakdown and todo list

The lesson outline and rough breakdown of topics by lesson writer is in
[lesson-outline.md](lesson-outline.md). The topics there will be initially generated by the lesson
writer, and then reviewed by the rest of the group once complete.

## Using this material

1. Follow the instructions found in the [Software Carpentry example lesson source](
   https://github.com/carpentries/lesson-example/) to create a repository for your lesson.

2. Create the required host-specific code snippets as a subdirectory of
   [_includes/snippets_library](_includes/snippets_library). These snippets provide inputs and
   outputs that are host-specific and that are included automatically when the lesson website is
   built.
    
   1. Code snippets are in files named `snippet_name.snip` and are included automatically
      when the lesson is built. For example, if the `snippet_name` was `login_output`,
      then the snippet file would be called `login_output.snip`.
   2. Code snippets are placed in subdirectories that are named according to the episode they
      appear in. For example, if the snippet is for episode 12, then it will be in a 
      subdirectory called `12`.
   3. In the episodes source, snippets are included using [Liquid](
      https://shopify.github.io/liquid/) scripting  `include` statements. For example, the first
      snippet in episode 12 is included using `{% include /snippets/12/info.snip %}`.
      
3. Edit `_config_settings.yml` in your snippets folder. These options set such things as the address
   of the host to login to, definitions of the command prompt, and scheduler names.
   
4. Add your snippet directory name to the GitHub Actions configuration file,
   [.github/workflows/test_and_build.yml](.github/workflows/test_and_build.yml).

5. To test your build, please set the environment variable `SITE_CONFIG` to the relative path of
   the configuration file in your snippets folder:
   `export SITE_CONFIG=_includes/snippets_library/Site_Cluster_scheduler/_config_options.yml`.

Please contribute any configurations you create for your local systems back into the 
HPC Carpentry snippets library.

## Lesson writing instructions

This is a fast overview of the Software Carpentry lesson template. This won't cover lesson style or
formatting.

For a full guide to the lesson template, see the
[Software Carpentry example lesson](http://carpentries.github.io/lesson-example/).

### Lesson structure

Software Carpentry lessons are generally episodic, with one clear concept for each episode
([example](http://swcarpentry.github.io/r-novice-gapminder/)).

An episode is just a markdown file that lives under the `_episodes` folder. Here is a link to a
[markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) with most
markdown syntax. Additionally, the Software Carpentry lesson template uses several extra bits of
formatting- see here for a [full guide](
https://carpentries.github.io/lesson-example/04-formatting/index.html). The most significant change
is the addition of a YAML header that adds metadata (key questions, lesson teaching times, etc.)
and special syntax for code blocks, exercises, and the like.

Episode names should be prefixed with a number of their section plus the number of their episode
within that section. This is important because the Software Carpentry lesson template will auto-post
our lessons in the order that they would sort in. As long as your lesson sorts into the correct
order, it will appear in the correct order on the website.

### Publishing changes to Github + the Github pages website

The lesson website is viewable at
[https://hpc-carpentry.github.io/hpc-intro/](https://hpc-carpentry.github.io/hpc-intro/)

The lesson website itself is auto-generated from the `gh-pages` branch of this repository. Github
pages will rebuild the website as soon as you push to the Github `gh-pages` branch. Because of this
`gh-pages` is considered the "master" branch.

### Previewing changes locally

Obviously having to push to Github every time you want to view your changes to the website isn't
very convenient. To preview the lesson locally, run `make serve`. You can then view the website at
`localhost:4000` in your browser. Pages will be automatically regenerated every time you write to
them.

Note that the autogenerated website lives under the `_site` directory (and doesn't get pushed to
Github).

This process requires Ruby, Make, and Jekyll. You can find setup instructions
[here](http://carpentries.github.io/lesson-example/setup.html).

## Example lessons

A couple links to example SWC workshop lessons for reference:

* [Example Bash lesson](https://github.com/swcarpentry/shell-novice)
* [Example Python lesson](https://github.com/swcarpentry/python-novice-inflammation)
* [Example R lesson](https://github.com/swcarpentry/r-novice-gapminder) (uses R markdown files
  instead of markdown)


