# zm
Zero Make - make done easy

zm mimics make by storing buildrules and builds a simple dependency graph.

A simple example:

```bash
echo -e "int sum(int a, int b)\n{\n\treturn a+b;\n}" > foo.c

echo -e "#include<stdio.h>\n\nextern int sum(int a, int b);\n\nint main(void)\n{\n\tprintf(\"sum %i\", sum(1,2));\n}\n" > bar.c

zm -c bar.c
zm -c foo.c
zm bar.o foo.o
```

change any file and rebuild a.out by:

```bash
zm
```

generate corresponding makefile by:

```bash
zm --make
```

```make
bar.o:	bar.c
	gcc -c bar.c

foo.o:	foo.c
	gcc -c foo.c

a.out:	bar.o foo.o
	gcc bar.o foo.o
```

To remove object files:

```bash
zm --clean
```

Purge database (.zm.pickle):

```bash
zm --purge
```
