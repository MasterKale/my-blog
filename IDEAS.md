# Ideas for future posts

- ~~Skipping CI jobs on Gitlab~~
  - ~~https://docs.gitlab.com/ee/ci/yaml/README.html#skipping-jobs~~
- Setting tags on jobs to force use of shared runners
  - https://about.gitlab.com/2016/04/05/shared-runners/ > "The tags"
  - Can use shared runners for Docker jobs, then deploy using private
- Deploying static site on private hosting
  - Build with shared runner, deploy with private runner (specify which using tags)
  - Make sure to set artifact property on build job, will download artifact to private runner
    before running deploy script