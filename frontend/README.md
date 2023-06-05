# The Mangler Frontend

This is the frontend for Mangler. This is a website-based client made with the Bootstrap framework.
Uses Pug as the template language and TypeScript for program logic.

## Building

This is intended to be run as part of the Mangler app in Docker. The `Dockerfile.build` file provides instructions for Docker to build the client and save the built files to the `frontend` volume. The `build.sh` script serves as the entrypoint for npm to build the client.

## Functionality

The client allows the user to submit files used for training or use already-provided examples, and generate text based on those files. It makes it straight-forward to set the text generator's parameters. The client leverages the Mangler API to fulfill text generation requests and presents the results in a readable way.
