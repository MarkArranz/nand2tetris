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

### And16

#### API

    Chip Name:  And16
    Input:      a[16], b[16]
    Output:     out[16]

#### Function

    for i = 0..15
        out[i] = And(a[i], b[i])

### Or16

#### API

    Chip Name:  Or16
    Input:      a[16], b[16]
    Output:     out[16]

#### Function

    for i = 0..15
        out[i] = Or(a[i], b[i])

### Mux16

#### API

    Chip Name:  Mux16
    Input:      a[16], b[16], sel
    Output:     out[16]

#### Function

    for i = 0..15
        if (sel == 0) then
            out[i] = a[i]
        else
            out[i] = b[i]

## Multi-way Variants

* `Or8Way`
* `Mux4Way16`
* `Mux8Way16`
* `DMux4Way`
* `DMux8Way`

### Or8Way

An _m_-way Or gate outputs 1 when at least on of its _m_ input bits is 1, and 0 otherwise.

#### API

    Chip Name:  Or8Way
    Input:      in[8]
    Output:     out

#### Function

    out = Or(in[0], in[1],...,in[7])

### Mux4Way16

An _m_-way _n_-bit multiplexer selects one of its _m_ _n_-bit inputs, and outputs it to its _n_-bit output. The selection is specified by a set of _k_ selection bits, where `k = log2(m)`.

#### API

    Chip Name:  Mux4Way16
    Input:      a[16], b[16], c[16], d[16], sel[2]
    Output:     out[16]

#### Function

    if (sel == 00, 01, 10, or 11) then
        out = a, b, c, or d

In other words:

    switch (sel):
        case 00: out = a
        case 01: out = b
        case 10: out = c
        case 11: out = d

#### Truth Table

|sel[1]|sel[0]|out|
|:-:|:-:|:-:|
|0|0|a|
|0|1|b|
|1|0|c|
|1|1|d|

#### Implementation

Given the value of `sel[0]`, you reduce the possible `out` values by 1/2, from 4 to 2:

    SELECT(a OR b)

and:

    SELECT(c OR d)

Therefore:

    MUX(a, b, sel[0])

and:

    MUX(c, d, sel[0])

Given the value of `sel[1]`, you further reduce the possible `out` values by 1/2, from 2 to 1:

    SELECT(
        MUX(a, b, sel[0])
        OR MUX(c, d, sel[0])
    )

Therefore:

    Mux4Way16(a[16], b[16], c[16], d[16], sel[2])
    <=> Mux16(
            Mux16(a[16], b[16], sel[0]),
            Mux16(c[16], d[16], sel[0]),
            sel[1]
        )

### Mux8Way16

#### API

    Chip Name:  Mux8Way16
    Input:      a[16], b[16], c[16], d[16],
                e[16], f[16], g[16], h[16], sel[3]
    Output:     out[16]

#### Function

    if (sel == 000, 001, 010,... or 111) then
        out = a, b, c, ...or h

#### Truth Table

|sel[2]|sel[1]|sel[0]|out|
|:-:|:-:|:-:|:-:|
|0|0|0|a|
|0|0|1|b|
|0|1|0|c|
|0|1|1|d|
|1|0|0|e|
|1|0|1|f|
|1|1|0|g|
|1|1|1|h|

#### Implementation

Following a similar pattern to `Mux4Way16`, we can split the possible outputs into two groups, reducing our options from 8 to 2. By using the first two bits of `sel` and our newly created `Mux4Way16` gate, we get:

    Mux4Way16(a, b, c, d, sel[0..1])

...and...

    Mux4Way16(e, f, g, h, sel[0..1])

Now that we only two selections to choose from, we can use `Mux16` and the third bit of `sel` to end up with only one channel selection:

    Mux8Way16(a, b, c, d, e, f, g, h, sel[3])
    <=> Mux16(
            Mux4Way16(a, b, c, d, sel[0..1]),
            Mux4Way16(e, f, g, h, sel[0..1]),
            sel[2]
        )

### DMux4Way

### DMux8Way
