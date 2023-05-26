# Example Training Text Directory

This directory provides example training data for The Mangler that users could pick from when generating their own text. However, as you might be able to see, there is nothing really here. That is because you need to put your own training data here.

To do so, simply copy any .txt files you fancy into this directory. You will also need to create a file named `metadata.yml` in this directory, which contains details about the training data, such as the text's title/name or tags. The file should be structured in the following manner:

```yml
examples:
  file name without extension here:
    title: <text/work title here>
    author: <author name here, not required>
    lang: <text language here>
    tags:
      - some tag
      - another tag
```

For every file you include in this directory, a description should be present in `metadata.yml`, otherwise The Mangler will not load the file. In the following example, the directory contains `doll.txt` and `macbeth.txt`:

```yml
examples:
  doll:
    title: Lalka
    author: Bolesław Prus
    lang: Polish
    tags:
      - novel
      - book

  macbeth:
    title: The Tragedy of Macbeth
    author: William Shakespeare
    lang: English
    tags:
      - play
      - book
```

This data can later be retrieved via the `examples` API endpoint.
