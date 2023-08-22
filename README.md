# Briar Website

## Installation

Run the following inside your Hugo site folder:

```
$ git clone https://code.briarproject.org/briar/website.git
```

## Prerequisites

Make sure to have hugo 0.93.1 installed to run the commands below,
otherwise you may encounter errors. Obtain that version from here:

https://github.com/gohugoio/hugo/releases/tag/v0.93.1

## Install

Test page with local hugo webserver:

```
./test.py
```

Generate static hugo pages:

```
./build.py
```

## Content Types

### Hiring

Used for hirings. Hiring posts are listed on the homepage.

Run `hugo new hiring/<post-name>.md` to create a post.

### News

Used for blog posts. Blog posts are listed on the homepage.

Run `hugo new news/<post-name>.md` to create a post.

### Page

Used for site pages.

Run `hugo new page/<page-name>.md` to create a page.
