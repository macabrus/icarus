# Icarus - [Learning to Fly!](https://www.youtube.com/watch?v=nVhNCTH8pDs)

The ```emitter``` is a module for multicasting data from RPI, while the ```monitor``` is written in java and is used for monitoring drone status.

```experiment``` contains scripts used while still developing.

Project is built by executing ```./build```, deployed to drone with ```./deploy``` and finally executed on both PC and RPI by executing ```./run``` in project root.

Individual modules are runnable if they contain appropriate ```./build && ./run```, such as module ```monitor```.