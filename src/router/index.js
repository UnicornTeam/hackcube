import Vue from 'vue';
import Router from 'vue-router';
import Wifi from '@/views/Wifi/Wifi';
import NFC from '@/views/NFC/NFC';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Wifi',
      component: Wifi,
    },
    {
      path: '/nfc',
      name: 'NFC',
      component: NFC,
    },
  ],
});
