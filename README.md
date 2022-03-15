# lift
An easy-to-use container builder


## Why?

Creating Dockerfiles can be a bit tiresome


## What this doesn't do

- Multi-stage builds


## How to use


Write a YAML file

```yaml
metadata:
  repo: localhost:5001
  name: file-manager
  tags:
  - latest
spec:
  base: alpine ## alpine or debian  
  user:
    - uid: 1000
      create: yes
      name: eend
      password: something
  packages:
    - dbus-x11
    - faenza-icon-theme
    - thunar
    - ttf-open-fonts
  command: >
    #!/bin/sh
    DISPLAY=x11:0.0 dbus-launch thunar
```
