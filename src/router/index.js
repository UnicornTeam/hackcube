import Vue from 'vue';
import Router from 'vue-router';
import Hello from '@/components/Hello';
import CubeNav from '@/components/CubeNav';
import Wifi from '@/views/Wifi/Wifi';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello,
    },
    {
      path: '/cubenav',
      name: 'Navbar',
      component: CubeNav,
    },
    {
      path: '/wifi',
      name: 'Wifi',
      component: Wifi,
    },
  ],
});
