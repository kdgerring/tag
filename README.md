
"""
Usage: 
  tag.py [-v|-q] tags <file>           
  tag.py [-v|-q] get <tagexpr>        
  tag.py [-v|-q] set <file> <tagexpr>
  tag.py -h | --help
  tag.py --version
  
Options:
  -h, --help     Show this help message and exit                           
  -v, --verbose  If set, make the application emit DEBUG log statements.   
  -q, --quiet    If set, make the application silent except for errors.    

Commands:
  set   Process the tagexpr and set the file to have matching tags.
  get   Process the tagexpr and find all matching files.
  tags  Given a file, return the set of tags for that file.

Tagexprs:
  A tag expression, or tagexpr, is a query statement that allows the user to
  precisely specify which tags to match in a query. An expression follows this
  grammar:

    <expr> := [<tag>]
    <tag> := <mustHaveTag> | <mustNotHaveTag> | <canHaveTag>
    <mustHaveTag> := "+" <tagstring>
    <mustNotHaveTag> := "-" <tagstring>
    <canHaveTag> := <tagstring>

  A <tagstring> is any arbitrary string of characters. An example expression is
  "+foo -bar baz", which only matches files that have a "foo" tag, do not have
  a "bar" tag, and may have a "baz" tag. In set, "+tag" and "tag" both mean to 
  add that tag to the file, while "-tag" means to remove that tag from the 
  file.
"""
