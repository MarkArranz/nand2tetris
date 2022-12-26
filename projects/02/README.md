# Adders & the Arithmetic Logic Unit (ALU)

* Half-adder
* Full-adder
* Adder
* Incrementer
* Arithmetic Logic Unit (ALU)

## The _Half-adder_ Chip

Designed to add two bits.

### Interface

#### API

    Chip Name:  HalfAdder
    Input:      a, b
    Output:     sum, carry

#### Function

    sum     = LSB of a + b
    carry   = MSB of a + b

LSB: Least Significant Bit

MSB: Most Significant Bit

#### Truth Table

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

### Interface

#### API

    Chip Name:  FullAdder
    Input:      a, b, c
    Output:     sum, carry

#### Function

    sum     = LSB of a + b + c
    carry   = MSB of a + b + c

#### Truth Table

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

### Interface

#### API

    Chip Name:  Add16
    Input:      a[16], b[16]
    Output:     out[16]

#### Function

Adds two 16-bit numbers. The overflow bit is ignored.

### Implementation

Starting from the LSBs to the MSBs, add the bits together in addition to any carry value that exists.

    Adder(a[16], b[16]) => out[16]
    <=> HalfAdder(a[0], b[0]) => out[0], carry0
        FullAdder(a[1], b[1], carry0) => out[1], carry1
        ...
        FullAdder(a[15], b[15], carry14) => out[15], carry15 // ignored carry value

## The _Incrementer_ Chip

### Interface

#### API

    Chip Name:  Inc16
    Input:      in[16]
    Output:     out[16]

#### Function

    out = in + 1
The overflow bit is ignored.

### Implementation

We can just use our new `Add16` chip.

    Inc16(in) => out
    <=> Add16(a=in, b[0]=true) => out

## The _ALU_

### Interface

#### API

#### Function

#### Truth Table

### Implementation
