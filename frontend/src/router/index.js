import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../components/GlobalSystemGrid.vue")
  },
  {
    path: "/map",
    name: "map",
    component: () => import("../pages/GlobalMap.vue")
  },
  {
    path: "/replay",
    name: "replay",
    component: () => import("../pages/GlobalReplay.vue")
  },
  {
    path: "/archive",
    name: "archive",
    component: () => import("../pages/GlobalArchive.vue")
  },
  {
    path: "/storyboards",
    name: "storyboards",
    component: () => import("../pages/GlobalStoryboards.vue")
  },
  {
    path: "/control-room",
    name: "control-room",
    component: () => import("../pages/GlobalControlRoom.vue")
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../components/GlobalSystemGrid.vue")
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
