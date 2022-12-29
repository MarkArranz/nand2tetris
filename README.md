# **From Nand to Tetris**: Building a Modern Computer From First Principles

This repository contains my code for implementing each of the projects from Noam Nisan's and Shimon Schocken's _The Elements of Computing Systems, Second Edition_.

## Overview

> "The Nand to Tetris journey entails twelve hardware and software construction projects. The general direction of development across these projects, as well as the book’s table of contents, imply a bottom-up journey: we start with elementary logic gates and work our way upward, leading to a high-level, object-based programming language.”

\- Excerpt From
_The Elements of Computing Systems, Second Edition_

### Hardware

The hardware platform is based on a set of about thirty logic gates and chips. Every one of these gates and chips, including the topmost computer architecture, will be built using a _Hardware Description Language_, HDL, and simulated on a software-based harware simulator.

### Software

The software stack that will include an assembler, a virtual machine, and a compiler. These can be written in any programming language.

### Repo Struture

The repo is separated into two main directories, `projects` and `tools`. Implemented code lives in `projects` while the files contained in `tools` are used to run the code.
