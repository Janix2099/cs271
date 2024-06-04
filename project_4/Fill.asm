// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

@LOOP
0;JMP    // Infinite loop to start

(LOOP)
    @KBD
    D=M         // D = keyboard character
    @DRAW_BLACK
    D;JNE
    
    @SCREEN
    D=A         
    @8192
    D=D+A       // D = End address of screen
    @i
    M=D         // i = End address of screen
    
(CLEAR_LOOP)
    @i
    D=M-1       // D = i - 1
    M=D         // i = i - 1
    @DONE_CLEAR
    D;JLT       // If i < 0, done clearing
    
    @i
    A=M         // A = i (current screen address)
    M=0         // Set current screen pixel to white (0)
    @CLEAR_LOOP
    0;JMP       // Repeat until screen is cleared
    
(DONE_CLEAR)
    @LOOP
    0;JMP       // Restart main loop

(DRAW_BLACK)
    @SCREEN
    D=A         // D = SCREEN base address
    @8192
    D=D+A       // D = End address of screen
    @i
    M=D         // i = End address of screen
    
(BLACK_LOOP)
    @i
    D=M-1       // D = i - 1
    M=D         // i = i - 1
    @DONE_BLACK
    D;JLT       // If i < 0, done blackening
    
    @i
    A=M         // A = i (current screen address)
    M=-1        // Set current screen pixel to black (-1)
    @BLACK_LOOP
    0;JMP       // Repeat until screen is blackened
    
(DONE_BLACK)
    @LOOP
    0;JMP       // Restart main loop
