# Memory Chips

Given as a primitive:

    * data flip-flops (DFF)

Create the following chips:

* Bit (1-bit register)
* Register (16-bit register)
* RAM8
* RAM64
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
