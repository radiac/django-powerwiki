FROM node:12.18.3-slim

# Default to watching
# Override with:
#   docker run -e NPM_ENV=dev container_name
ENV FRONTEND_MODE watch

# Leave the entrypoint to npm install each time, so it goes into the project volume
CMD ["/project/docker/frontend/run.sh"]
