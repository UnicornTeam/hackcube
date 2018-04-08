import axios from 'axios';
import apis from './api';

export default {
  getAPList: () => axios
      .get(`${process.env.BACKEND_HOST}/${apis.WIFI.GET_AP_LIST}`, {
        validateStatus(status) {
          return status < 400;
        },
      }),
  getSTAList: () => axios
    .get(`${process.env.BACKEND_HOST}/${apis.WIFI.GET_STA_LIST}`, {
      validateStatus(status) {
        return status < 400;
      },
    }),
};
