#!/usr/bin/env bash
set -euo pipefail

CONTAINER=ur3
IMAGE=${IMAGE:-osrf/ros:humble-desktop-full}
WS=$HOME/projects/ur3_ws
SRC=$HOME/projects/UR3_with_Robotiq_gripper_85

# Let the container's root user draw on your X server.
xhost +local:docker

# Already running? Just open another shell in it.
if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null)" = "true" ]; then
  docker exec -it "$CONTAINER" bash
# Exists but stopped? Restart it, keeping anything installed inside.
elif docker inspect "$CONTAINER" >/dev/null 2>&1; then
  docker start "$CONTAINER" >/dev/null
  docker exec -it "$CONTAINER" bash
else
  # First run: create it.
  docker run -it \
    --name "$CONTAINER" \
    --net=host \
    --ipc=host \
    --shm-size=2g \
    -e DISPLAY="$DISPLAY" \
    -e QT_X11_NO_MITSHM=1 \
    -e LIBGL_ALWAYS_SOFTWARE=0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --device /dev/dri \
    -v "$WS":/root/ur3_ws \
    -v "$SRC":/root/ur3_src:ro \
    -w /root/ur3_ws \
    "$IMAGE" bash
fi

# The container runs as root, so anything it creates in the bind-mounted
# workspace lands on the host owned by root. Hand it back to you every
# time your shell in the container exits, so your host editor can write too.
sudo chown -R "$(id -u):$(id -g)" "$WS"
