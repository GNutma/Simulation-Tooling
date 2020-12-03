globals [target]
turtles-own [speed]

to setup
  clear-all
  ask patches [setup-road]
  setup-turtles
  set target turtle 0
  ask target [set color red]
  reset-ticks
end

to setup-turtles
  make-turtles 0 amount-of-cars world-width / amount-of-cars
  set-default-shape turtles "car"
end

to setup-road ;; patch procedure
  if pycor < 1 and pycor > -1 [set pcolor grey]
end

to make-turtles [x-pos amount step]
  if amount <= 0 [stop]
  create-turtles 1 [
    set color white
    setxy x-pos 0
    set heading 90
    set speed max-speed
  ]
  make-turtles x-pos + step amount - 1 step
end

to go
  move-turtles
  tick
end

to move-turtles
  ask turtles [
    forward 1
  ]
end
