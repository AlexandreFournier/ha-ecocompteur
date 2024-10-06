#!/bin/bash

podman run \
	--network=host \
	--volume $(pwd)/custom_components:/config/custom_components \
	ghcr.io/home-assistant/home-assistant:latest
