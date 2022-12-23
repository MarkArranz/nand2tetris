# Logic Gates

Given `Nand`, build the following gates:

 Elementary Logic Gates

* `Not`
* `And`
* `Or`
* `Xor`
* `Mux`
* `DMux`

16-bit Variants

* `Not16`
* `And16`
* `Or16`
* `Mux16`

Multi-way Variants

* `Or8Way`
* `Mux4Way16`
* `Mux8Way16`
* `DMux4Way`
* `DMux8Way`

## Primitive/Foundational Logic Gates

### NAND

#### API

    Chip Name:  Nand
    Input:      a, b
    Output:     out

#### Function

    if ((a == 1) and (b == 1)) then
        out = 0
    else
        out = 1

#### Truth Table

|a|b|out|
|:-:|:-:|:-:|
|0|0|1|
|0|1|1|
|1|0|1|
|1|1|0|

## Elementary Logic Gates

* `Not`
* `And`
* `Or`
* `Xor`
* `Mux`
* `DMux`

### NOT

#### API

    Chip Name:  Not
    Input:      in
    Output:     out

#### Function

    if (in == 0) then
        out = 1
    else
        out = 0

#### Truth Table

| in | out |
|----|-----|
|  0 |  1  |
|  1 |  0  |

#### Implementation

Given:

* `Nand`

Then:

    NOT x
    <=> NOT (x AND x) [via Idempotency Law]
    <=> x NAND x [via Sheffer Stroke]

### AND

#### API

    Chip Name:  And
    Input:      a, b
    Output:     out

#### Function

    if ((a == 1) and (b == 1)) then
        out = 1
    else
        out = 0

#### Truth Table

|a|b|out|
|:-:|:-:|:-:|
|0|0|0|
|0|1|0|
|1|0|0|
|1|1|1|

#### Implementation

Given:

* `Nand`
* `Not`

Then:

    a AND b
    <=> NOT (a OR b) [via De Morgan's Law]
    <=> NOT (NOT (a AND b)) [via De Morgan's Law]
    <=> NOT (a NAND b) [via Sheffer Stroke]

### OR (Inclusive OR)

#### API

    Chip Name:  Or
    Input:      a, b
    Output:     out

#### Function

    if ((a == 0) and (b == 0)) then
        out = 0
    else
        out = 1

#### Truth Table

|a|b|out|
|:-:|:-:|:-:|
|0|0|0|
|0|1|1|
|1|0|1|
|1|1|1|

#### Implementation

Given:

* `Nand`
* `Not`
* `And`

Then:

    a OR b
    <=> (NOT (NOT a)) OR b [via Involution Law]
    <=> (NOT (NOT a)) OR (NOT (NOT b)) [via Involution Law]
    <=> NOT ((NOT a) AND (NOT b)) [via De Morgan's Law]
    <=> (NOT a) NAND (NOT b) [via Sheffer Stroke]

### XOR (Exculsive OR)

#### API

    Chip Name:  Xor
    Input:      a, b
    Output:     out

#### Function

    if (a != b) then
        out = 1
    else
        out = 0

#### Truth Table

|a|b|out|
|:-:|:-:|:-:|
|0|0|0|
|0|1|1|
|1|0|1|
|1|1|0|

#### Implementation

Given `Xor` is true only when:

    a = 0 AND b = 1
    OR
    a = 1 AND b = 0

Then:

    a XOR b
    <=> ((NOT a) AND b) OR (a AND (NOT b))

### Mux (Multiplexer)

#### API

    Chip Name:  Mux
    Input:      a, b, sel
    Output:     out

#### Function

    if (sel == 0) then
        out = a
    else
        out = b

#### Truth Table

|sel|out|
|:-:|:-:|
|0|a|
|1|b|

|a|b|sel|out|
|:-:|:-:|:-:|:-:|
|0|0|0|0|
|0|1|0|0|
|1|0|0|1|
|1|1|0|1|
|0|0|1|0|
|0|1|1|1|
|1|0|1|0|
|1|1|1|1|

#### Implementation

Given `mux` is true only when:

    a = 1 AND sel = 0
    OR
    b = 1 AND sel = 1

Then:

    mux(a, b, sel)
    <=> (a AND (NOT sel)) OR (b AND sel)

### DMux (Demultiplexer)

#### API

    Chip Name:  DMux
    Input:      in, sel
    Output:     a, b

#### Function

    if (sel == 0) then
        {a, b} = {in, 0}
    else
        {a, b} = {0, in}

#### Truth Table

|sel|a|b|
|:-:|:-:|:-:|
|0|in|0|
|1|0|in|

#### Implementation

Given 'dmux' is true for `a` only when:

    sel = 0 AND in = 1

and is true for `b` only when:

    sel = 1 AND in = 1

Then:

For `a`:

    dmux(sel, in) <=> (NOT sel) AND in

For `b`:

    dmux(sel, in) <=> sel AND in

## 16-bit Variants

* `Not16`
* `And16`
* `Or16`
* `Mux16`

### Not16

#### API

    Chip Name:  Not16
    Input:      in[16]
    Output:     Out[16]

#### Function

    for i = 0..15
        out[i] = Not(in[i])
