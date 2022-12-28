# Memory Chips

Given as a primitive chip:

* Data Flip-Flops (DFF)

Create the following chips:

* Bit (1-bit register)
* Register (16-bit register)
* RAM8 & RAM64
* PC (Counter)

## Bit (1-bit register)

Stores and emits a 1-bit value until instructured to load a new value.

### API

    Chip Name:  Bit (1-bit register)
    Input:      in, load
    Output:     out

### Function

    if load(t) then out(t+1) = in(t)
    else            out(t+1) = out(t)

### Implementation

The `if...else` behavior of the `Bit` chip calls for the use of a `Mux` so we can select how we want `out(t+1)` to behave. Since we select based on the `load` bit, it can act as our selector.

    Bit(in, load) => out
    <=> Mux(a=?, b=?, sel=load) => muxOut
        ...

From the function definition, we see that when `load` is True, then we want to return `in`.

    Bit(in, load) => out
    <=> Mux(a=?, b=in sel=load) => muxOut
        ...

We need a way to store the previous `out` value for one clock cycle. That's where the `DFF` chip comes into play. We can use the `DFF` chip to capture the previous `out` variable and route it into the `Mux` chip's `in` input.

    Bit(in, load) => out
    <=> Mux(a=dffOut, b=in sel=load) => muxOut
        DFF(in=muxOut) => dffOut
        ...

To complete the implementation, we also need the `DFF` chip to route it's output to the `Bit` chip's out pin.

    Bit(in, load) => out
    <=> Mux(a=dffOut, b=in sel=load) => muxOut
        DFF(in=muxOut) => dffOut
                       => out
NOTE: The `Bit` register is the only chip in the Hack architecture that uses a `DFF` gate directly; all the higher-level memory devices in the computer use `DFF` chips indirectly, by virtue of using `Register` chips made of `Bit` chips.

## Register (16-bit)

Stores and emits a 16-bit value until instructed to load a new value.

### API

    Chip Name:  Register (16-bit register)
    Input:      in[16], load
    Output:     out[16]

### Function

    if load(t) then out(t+1) = in(t)
    else            out(t+1) = out(t)
Comment: "=" is a 16-bit operation.

### Implementation

This one is rather straightforward. We can use our newly created `Bit` register for each of the 16 bits that this `Register` chip needs.

    Register(in[16], load) => out[16]
    <=> Bit(in=in[0], load=load, out[0])
        Bit(in=in[1], load=load, out[1])
        ...
        Bit(in=in[15], load=load, out[15])

## RAM8 & RAM64 (RAM _n_)

A RAM chip, consisting of _n_ 16-bit `Register` chips that can be selected and manipulated separately.

### API

    Chip Name:  RAMn
    Input:      in[16], load, address[k]
    Output:     out[16]
NOTE: _k_ = log2(_n_)

### Function

`out` emits the value stored at the memory location (register) specified by `address`.

If `load == 1`, then the memory location specified by `address` is set to the value of `in`.

The loaded value will be emitted by `out` from the next time step onward.

### Implementation

The RAM implementation must ensure that the access time to any register in the RAM will be nearly instantaneous.

For the `RAM8` chip, we can utilize a `Mux8Way16` gate to select 1 of 8 different `Register` chips to read from.

    RAM8(in[16], load, address[3]) => out
    <=> Register(in, load) => reg0
        Register(in, load) => reg1
        ...
        Register(in, load) => reg7

        Mux8Way16(a=reg0, b=reg1,..., h=reg7, sel=address) => out

In order to properly write to one of these 8 `Register` chips, we need to select which of the 8 to write to given the `address` input. We can use a `DMux8Way` to figure out which of the 8 `Register` chips to write `in` to when `load` is 1.

    RAM8(in[16], load, address[3]) => out
    <=> DMux8Way(in=load, sel=address, a=load0, b=load1, ..., h=load7)

        Register(in=in, load=load0) => reg0
        Register(in=in, load=load1) => reg1
        ...
        Register(in=in, load=load7) => reg7

        Mux8Way16(a=reg0, b=reg1,..., h=reg7, sel=address) => out
