<template>
  <nav class="nav">
    <div class="title">Observatory</div>
    <div class="links">
      <router-link to="/">Home</router-link>
      <router-link to="/map">Map</router-link>
      <router-link to="/replay">Replay</router-link>
      <router-link to="/control">Control Room</router-link>
      <router-link to="/archive">Archive</router-link>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #161b22;
  padding: 1rem 2rem;
  border-bottom: 1px solid #30363d;
}

.title {
  font-size: 1.2rem;
  font-weight: bold;
}

.links a {
  margin-left: 1rem;
  color: #e6edf3;
  text-decoration: none;
}

.links a.router-link-active {
  font-weight: bold;
}
</style>
