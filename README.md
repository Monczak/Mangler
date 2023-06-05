# The Mangler

This is a web app for mangling text. It is a procedural, Markov chain-based text generator for experimental generation of nonsense.

Developed as a final project for WUST's Scripting Languages lab class.

## Running and building

The Mangler leverages Docker Compose to run all of its services. To start the app, you can use the provided utilities:

```
./up  (or ./compose up)
```

The `./up` script is a shorthand for `./compose up`.

The `--build` flag can be passed to this command if the images are not already built or not up to date. Using `docker-compose` by itself is not recommended, as these utilities automatically setup vital environment variables used for the image building process. The `./compose` script uses `docker-compose` internally and functions identically to that utility.

### Scaling workers

To scale text generation workers, you can pass the `--scale textgen-worker=x` argument to `./compose` or `./up`, where x is the number of workers. You can do the same with backend workers, just pass `--scale backend-worker=x` instead.

### Rebuilding the frontend

If need be during development, a utility for rebuilding the frontend and restarting the backend service automatically is also provided. Invoking `./rebuild-frontend` does everything for you.


