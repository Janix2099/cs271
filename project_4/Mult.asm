// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R2
    M=0     // R2 set to 0
    @i
    M=0     // i to 0 for the counter

(LOOP)
    @i
    D=M     // D = i
    @R0
    D=D-M   // D = i - R0
    @END
    D;JGE   // If i >= R0, terminate loop

    @R1
    D=M     // D = R1
    @R2
    M=D+M   // R2 = R2 + R1

    @i
    M=M+1   // i = i + 1 (Increment counter)
    @LOOP
    0;JMP

(END)
    @END
    0;JMP
