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
