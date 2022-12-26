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

### Interface

#### API

#### Function

#### Truth Table

### Implementation

## The _Adder_ Chip

### Interface

#### API

#### Function

#### Truth Table

### Implementation

## The _Incrementer_ Chip

### Interface

#### API

#### Function

#### Truth Table

### Implementation

## The _ALU_

### Interface

#### API

#### Function

#### Truth Table

### Implementation
