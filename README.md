# tf_mpc

A basic MPC sum implementation. 

## Introduction

This project aims at achieving a secured sum of 
two secret values. 

### Implementation strategy

Let's assume two parties _Alice_ and _Stephanie_ 
both holds a __secret value__, respectively `a` and `s`. 
A third agent, _Bob_, 
wants to know the __sum of the two secret values__, 
ie. `a + s`.
While _Alice_ and _Stephanie_ agree on sharing with
_Bob_ the sum of their respective values, they __do not
want to disclose the individual value__ of their secret.

The idea behind this implementation is the __generation
of randomness__: let's assume, without loss of generality,
that _Alice_ generates a random value `r`. She
sends it to _Stephanie_, without letting _Bob_ 
intercept it. Then, both _Alice_ and _Stephanie_ do
some calculation to __encrypt__ their secret values:
_Alice_ calculates `a + r` and _Stephanie_ `s - r`.
These encrypted values are sent to _Bob_, which can
eventually recover the desired value by summing:
`(a + r) + (s - r) = a + s`.

### Terminology
The two agents
that holds secret values are called __slaves__. The
one in charge of generating the random tensor used
for encryption is called the __slave leader__. 
The slaves send their encrypted secret values to
the __master__. 

With the example names given in the previous paragraph,
_Alice_ is the _slave leader_, _Stephanie_ a slave and
_Bob_ the master.

### Implementation note

__Python__ is used as implementation language, but it 
should be easily portable. The communication is done
via __websockets__, a Python implementation of the WebSocket protocol, a high level protocol built on top of TCP. All the calculations
are done using __Tensorflow__.

## Requirements

- Python 3.8+
- Tensorflow 2.2+
- websockets 8.1+

## Usage

```bash
./run.sh
```

_Note:_ this basic example sums two secrets contained
in files `slave.py` and `slave_leader.py` and 
prints it.
