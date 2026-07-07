# Planetary Physics Sim

A 2D physics playground built with Pygame where all 8 planets of the solar system bounce, collide, and interact using real relative masses — you can grab any planet and fling it across the screen.

![gameplay demo](demo.gif)
<!-- replace demo.gif with your own screen recording or GIF -->

## What it does

- **Gravity** pulls every planet toward the floor, and they bounce off the floor, ceiling, and side walls.
- **Elastic collisions** between planets are calculated using real 2D collision physics (mass, velocity, and a restitution coefficient per planet), so heavier planets barely budge when a lighter one hits them.
- **Drag and throw** — click and hold a planet to pick it up, move your mouse to drag it around, and let go to fling it. Release velocity is calculated from your recent mouse movement, so a fast flick throws it fast.
- **Each planet has its own physics personality**, loosely based on its real characteristics:
  - Rocky planets (Mercury, Mars) bounce sharply with low friction
  - Venus has a thick atmosphere, so it bounces less and drags more
  - Gas/ice giants (Jupiter, Saturn, Uranus, Neptune) are springier and slicker, with the windiest ones starting already in motion
- **Live mass readout** in the top-right corner, color-matched to each planet.
- **Starfield background** for atmosphere.

## Tech

- Python 3
- [Pygame](https://www.pygame.org/) (or `pygame-ce`, the community fork, for newer Python versions)

## Running it

```bash
pip install pygame-ce
python main.py
```

## Controls

| Action | Effect |
|---|---|
| Click + hold a planet | Pick it up |
| Drag while holding | Move the planet with your mouse |
| Release | Throw it, with velocity based on how fast you were dragging |

## What I built myself

The core loop, collision math, drag-and-throw velocity tracking, per-planet physics tuning, and visual polish (shading, starfield, mass labels) were all written and tuned by hand — this isn't a copy of a tutorial project.

## Possible next steps

- Procedurally generated planet textures (craters, bands, terrain)
- Sound effects on collision
- Orbit mode / gravity wells between planets instead of just floor gravity
