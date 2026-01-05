# SILFF
Hi! This is a my first project/repo on Github!

## What's SILFF
`SILFF` stands for Simple Interpreted Language For Fun. And how his name says, this is very basic interpreter writed in python

## features
Theres no many features in SILFF, but here is a list of them (with examples!)
### 1. variable declaration
just a simple variable declaration
```
var some_var = 5;
```
### 2. variables reassing
you can reassing every variable you want, and there's no type checker, so you can modify the type
```
some_var = "hello!";
```
### 3. binary operators
you have the common binary operators like +, -, /, *, <, >, <=, >=, == and !=

also, there's a simple precedence of the operators (that mean the * and / will be executed first than + and -)
```
var x = 5;
var y = 25;
var z = x * y / 25;
```
### 4. conditional statments
with the comparition operators you can compare values, and using the `if-else` statment you can make decitions
in your code based on a `true` or `false` value
```
var a = 2;
if a < 5 {
  var a = 8;
}else{
  // this is a comment
}
```
### 5. `print` and `read` statment
the print statment allows you to print values to the terminal, every expretion (like 2+2) can be show

the read statment allows you to read from the terminal, and store the value. also, the read statment takes an string to print
in the terminal and take the input
```
var a = read "enter a number: ";
print a; // it shows the value of a
```
### 6. the `nothing` operator
The `nothing` operator does exactly nothing, and you can use it for... right, nothing

The reason that i added this is for purely fun :)
```
var a = 6;
if a < 10 {
  nothing // does nothing
}
```
## Performance
As an ast-walk interpreter, this is not the fastest thing ever. and is writed in pyhton, an interpreted language,
so you can imagine the performance. 
Also, i don't used sofisticaded algorithms or similar. for the lexer i used the regex motor from the std of python,
and has a bad performance (not the regex engine, my lexer implementation).
I used recursive descend parser, and finally i walk my AST to run the code

## Executing
Because this intepreters is written in python, you can run a simply executable. for running a program 
with this interpreter, you need to follow tis steps:

* open the terminal and run the following command to copy the project: `$ git clone https://github.com/Santiago-Lopez-25/SILFF.git`
  this will copy the repo into a directory called SILFF
* next, navigate to the directory with: `$ cd SILFF`
* after that, in the same directory, create a file and write something like `print "hello world";`, save it
* and the final step: run the following: `$ python main.py [file]`, replacing `[file]`with the name
  of the file you just created
