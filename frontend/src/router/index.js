import { createRouter, createWebHistory } from 'vue-router'

// Pages
import Home from '../pages/Home.vue'
import GlobalMap from '../pages/GlobalMap.vue'
import GlobalControlRoom from '../pages/GlobalControlRoom.vue'
import GlobalReplay from '../pages/GlobalReplay.vue'
import GlobalArchive from '../pages/GlobalArchive.vue'
import GlobalStoryboards from '../pages/GlobalStoryboards.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/map', component: GlobalMap },
  { path: '/control', component: GlobalControlRoom },
  { path: '/replay', component: GlobalReplay },
  { path: '/archive', component: GlobalArchive },
  { path: '/storyboards', component: GlobalStoryboards }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
