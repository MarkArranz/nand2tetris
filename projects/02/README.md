# Adders & the Arithmetic Logic Unit (ALU)

* Half-adder
* Full-adder
* Adder
* Incrementer
* Arithmetic Logic Unit (ALU)

## The _Half-adder_ Chip

Designed to add two bits.

### API

    Chip Name:  HalfAdder
    Input:      a, b
    Output:     sum, carry

### Function

    sum     = LSB of a + b
    carry   = MSB of a + b

LSB: Least Significant Bit

MSB: Most Significant Bit

### Truth Table

a|b|carry|sum
:-:|:-:|:-:|:-:
0|0|0|0
0|1|0|1
1|0|0|1
1|1|1|0

### Implementation

We can address `carry` and `sum` one at a time since they are two separate outputs.

For `carry`, the _half-adder_'s DNF reads like an `AND` gate:
a|b|carry
:-:|:-:|:-:
0|0|0
0|1|0
1|0|0
1|1|1

For `sum`, the _half-adder_'s DNF reads like an `XOR` gate:
a|b|sum
:-:|:-:|:-:
0|0|0
0|1|1
1|0|1
1|1|0

Therefore:

    HalfAdder(a, b) => sum, carry
    <=> XOR(a, b) => sum
        AND(a, b) => carry

## The _Full-adder_ Chip

Designed to add three bits.

### API

    Chip Name:  FullAdder
    Input:      a, b, c
    Output:     sum, carry

### Function

    sum     = LSB of a + b + c
    carry   = MSB of a + b + c

### Truth Table

a|b|c|carry|sum
:-:|:-:|:-:|:-:|:-:|
0|0|0|0|0|
0|0|1|0|1|
0|1|0|0|1|
0|1|1|1|0|
1|0|0|0|1|
1|0|1|1|0|
1|1|0|1|0|
1|1|1|1|1|

### Implementation

We already have a _half-adder_ that can add two bit together. We can use that to add `a` and `b`, then add the sum of `a` & `b` to `c` to get the final `sum`.

    HalfAdder(a, b) => sumAB, firstCarry
    HalfAdder(sumAB, c) => sumAll, secondCarry

We can then use the `carry` values from each _half-adder_ operation into a final _half-adder_ operation to calculate the final `carry` value.

    HalfAdder(firstCarry, secondCarry) => sumOfCarries, ignoredCarry

This may be overkill, however, since we don't care about the `carry` value of this final operation, only the `sum`. So we can save extra cycles by just using the `Xor` from the _half-adder_ that is responsible for caluclating the `sum` value.

    HalfAdder(firstCarry, secondCarry) => sumOfCarries, thirdCarry
    <=> Xor(firstCarry, secondCarry) => sumOfCarries
        And(firstCarry, secondCarry) => thirdCarry

Therefore:
    FullAdder(a, b, c) => sum, carry
    <=> HalfAdder(a, b) => sumAB, firstCarry
        HalfAdder(sumAB, c) => sumAll, secondCarry
        Xor(firstCarry, secondCarry) => sumOfCarries

        sum = sumAll
        carry = sumOfCarries

## The _Adder_ Chip

Computers represent integer numbers using a fixed word size like 8, 16, 32, or 64 bits. _Adder_ chips are responsible for adding two such _n_-bit numbers.

### API

    Chip Name:  Add16
    Input:      a[16], b[16]
    Output:     out[16]

### Function

Adds two 16-bit numbers. The overflow bit is ignored.

### Implementation

Starting from the LSBs to the MSBs, add the bits together in addition to any carry value that exists.

    Adder(a[16], b[16]) => out[16]
    <=> HalfAdder(a[0], b[0]) => out[0], carry0
        FullAdder(a[1], b[1], carry0) => out[1], carry1
        ...
        FullAdder(a[15], b[15], carry14) => out[15], carry15 // ignored carry value

## The _Incrementer_ Chip

### API

    Chip Name:  Inc16
    Input:      in[16]
    Output:     out[16]

### Function

    out = in + 1
The overflow bit is ignored.

### Implementation

We can just use our new `Add16` chip.

    Inc16(in) => out
    <=> Add16(a=in, b[0]=true) => out

## The _ALU_

### API

    Chip Name:  ALU
    Input:      x[16], y[16],   // Two 16-bit data inputs
                zx,             // Zero the x input
                nx,             // Negate the x input
                zy,             // Zero the y input
                ny,             // Negate the y input
                f,              // if f==1 out=add(x,y) else out=and(x,y)
                no              // Negate the output
    Output:     out[16],        // 16-bit output
                zr,             // if out==0 zr=1 else zr=0
                ng              // if out<0 ng=1 else ng=0

### Function

    if zx x=0                   // 16-bit zero constant
    if nx x=!x                  // Bit-wise negation
    if zy y=0                   // 16-bit zero constant
    if ny y=!y                  // Bit-wise negation
    if f out=x+y                // Integer two's complement addition
    else out=x&y                // Bit-wise And
    if no out=!out              // Bit-wise negation
    if out==0 zr=1 else zr=0    // 16-bit equality comparison
    if out<0 ng=1 else ng=0     // Two's complement comparison
The overflow bit is ignored.

### Truth Table

zx|nx|zy|ny|f|no|out
:-:|:-:|:-:|:-:|:-:|:-:|:-:
1|0|1|0|1|0|0
1|1|1|1|1|1|1
1|1|1|0|1|0|-1
0|0|1|1|0|0|x
1|1|0|0|0|0|y
0|0|1|1|0|1|!x
1|1|0|0|0|1|!y
0|0|1|1|1|1|-x
1|1|0|0|1|1|-y
0|1|1|1|1|1|x+1
1|1|0|1|1|1|y+1
0|0|1|1|1|0|x-1
1|1|0|0|1|0|y-1
0|0|0|0|1|0|x+y
0|1|0|0|1|1|x-y
0|0|0|1|1|1|y-x
0|0|0|0|0|0|x&y
0|1|0|1|0|1|x\|y

### Implementation

Address each of the input control bits one at a time.

#### zx: Zero the x input

Function:

    if zx == 1 then x = 0 else x = x

Implementation:

    Mux16(a=x, b[0]=false, sel=zx) => zxOut

#### nx: Negate the x input

Function:

    if nx == 1 then x = !x else x = x

Implementation:

    Not16(in=x) => notX
    Mux16(a=zxOut, b=notX, sel=nx) => nxOut

#### zy: Zero the y input

Function:

    if (zy == 1) then y = 0 else y = y

Implementation:

    Mux16(a=y, b[0]=false, sel=zy) => zyOut

#### ny: Negate the y input

Function:

    if (ny == 1) then y = !y else y = y

Implementation:

    Not16(in=y) => notY
    Mux16(a=zyOut, b=notY, sel=ny) => nyOut

#### f: if f==1 out=add(x,y) else out=and(x,y)

Function:

    if (f == 1) then out = add(x,y) else out = and(x,y)

Implementation:

    And16(a=nxOut, b=nyOut) => andXY
    Add16(a=nxOut, b=nyOut) => addXY
    Mux16(a=andXY, b=addXY, sel=f) => fOut

#### no: Negate the output

Function:

    if (no == 1) then out = !out else out = out

Implementation:

    Not16(in=fOut) => notFOut
    Mux16(a=fOut, b=notFOut, sel=no) => out
