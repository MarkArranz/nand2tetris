# Memory Chips (continued)

Create the following memory chips:

* RAM512
* RAM4K
* RAM16K

## RAM512, RAM4K, RAM16K (RAM _n_)

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

For the `RAM512`, `RAM4K`, and `RAM16K` chips, we apply the same pattern we used when implementing the `RAM64` chip.

For `RAM512`, we get:

    RAM512(in[16], load, address[9]) => out
    <=> DMux8Way(in=load, sel=address[0..2])
            => { load0, load1, ..., load7 }

        RAM64(in=in, load=load0, address=address[3..8]) => ram0
        RAM64(in=in, load=load1, address=address[3..8]) => ram1
        ...
        RAM64(in=in, load=load7, address=address[3..8]) => ram7

        Mux8Way16(
            a=ram0, b=ram1, ..., h=ram7,
            sel=address[0..2]) => out

For `RAM4K`, we get:

    RAM4K(in[16], load, address[12]) => out
    <=> DMux8Way(in=load, sel=address[0..2])
            => { load0, load1, ..., load7 }

        RAM512(in=in, load=load0, address=address[3..11]) => ram0
        RAM512(in=in, load=load1, address=address[3..11]) => ram1
        ...
        RAM512(in=in, load=load7, address=address[3..11]) => ram7

        Mux8Way16(
            a=ram0, b=ram1, ..., h=ram7,
            sel=address[0..2]) => out

For `RAM16K`, we get:

    RAM16K(in[16], load, address[14]) => out
    <=> DMux4Way(in=load, sel=address[0..1])
            => { load0, load1, load2, load3 }

        RAM4K(in=in, load=load0, address=address[2..13]) => ram0
        RAM4K(in=in, load=load1, address=address[2..13]) => ram1
        RAM4K(in=in, load=load2, address=address[2..13]) => ram2
        RAM4K(in=in, load=load3, address=address[2..13]) => ram3

        Mux4Way16(
            a=ram0, b=ram1, c=ram2, d=ram3
            sel=address[0..1]) => out
