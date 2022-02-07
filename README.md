# Aegis Tetris node

Powered by [gym-tetris](https://github.com/Kautenja/gym-tetris)

## Environment
TODO

## Usage
POST an action number (0..5) to `/` to step the environment; returns:
```js
{
  obs: <nd-to-json encoded game board>,
  done: false, //true if environment reset
  reward: 1.0 //reward of current step
  // info: {...} //jk, info is broken currently
}
```
Action integers represent: 0=noop, 1=a, 2=b, 3=right, 4=left, 5=down

## Notes
- the env auto-resets

## TODO
- env vars
- fix info dict (coerce values in info to json friendly types)
- add route for reset
- support saving videos using monitor
