// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// NOTES:
// Screen is 512px wide x 256px deep
//
// Memory Map is stored in an 8K memory block of 16-bit words
// Starting at @SCREEN (16384, or 0x4000)
//
// Row is made up of 32 16-bit words (32*16=512)

// PSEUDOCODE:
// min = SCREEN - 1
// max = SCREEN + 8192 // (256 * 32)
// location = min
//
// LOOP
//  if (KBD != 0) goto KEYDOWN
//  goto KEYUP
//
// KEYDOWN
//  if (location == max) goto LOOP
//  location = location + 1
//  RAM[location] = -1
//  goto LOOP
//
// KEYUP
//  if (location == min) goto LOOP
//  location = location - 1
//  RAM[location] = 0
//  goto LOOP

// **HACK ASSEMBLY LANGUAGE**

    // min = SCREEN - 1
    @SCREEN
    D=A
    @min
    M=D-1

    // max = SCREEN + 8192 // (256 * 32)
    @SCREEN
    D=A
    @8192   // (256 rows * 32 words per row)
    D=D+A
    @max
    M=D

    // location = min
    @min
    D=M
    @location
    M=D

(LOOP)
    // if (KBD != 0) goto KEYDOWN
    @KBD
    D=M
    @KEYDOWN
    D;JNE
    
    // goto KEYUP
    @KEYUP
    0;JMP

(KEYDOWN)
    // if (location == max) goto LOOP
    @location
    D=M
    @max
    D=D-M
    @LOOP
    D;JEQ

    // location = location + 1
    @location
    M=M+1

    // RAM[location] = -1
    @location
    A=M
    M=-1

    // goto LOOP 
    @LOOP
    0;JMP

(KEYUP)
    // if (location == min) goto LOOP
    @location
    D=M
    @min
    D=D-M
    @LOOP
    D;JEQ

    // location = location - 1
    @location
    M=M-1

    // RAM[location] = 0
    @location
    A=M
    M=0

    // goto LOOP
    @LOOP
    0;JMP
