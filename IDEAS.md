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
- Writing vue-router route guards that depend on app state located within a Vuex store
  - Just `import store from '@/store;' as usual and access the store from within guard methods!
- Autofocus inputs on page load in VueJS
  - use `mounted()` lifecycle method and a `ref=""` attribute:
  ```
  <input type="text" ref="usernameEntry">

  mounted() {
    // This will autofocus the input when the component is displayed
    this.$refs.usernameEntry.focus();
  }
  ```