<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube Wifi Manage</h1>
    <h3 class="text-center">对工作在2.4Ghz 5Ghz设备进行安全风险检测</h3>
    <br/>
    <b-container>
      <b-row >
        <b-col cols="4">
          <h5>WiFi List</h5>
        </b-col>
        <b-col cols="1"></b-col>
        <b-col cols="4" style="padding-right: 4px;">
          <Select v-model="channel" size="small" placeholder="Channel" filterable>
            <Option v-for="item in channelList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </b-col>
        <b-col cols="1">
          <b-button size="sm" variant="success" @click="onClickScan">Scan</b-button>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items[data.index].JAM"
                    @change="onSwitch('ap_block', items[data.index].BSSID, data.index, items[data.index].JAM)" />
      </div>
    </b-table>


    <!-- Client list -->
    <h5>Client List</h5>
    <b-table :items="items2" :fields="fields2">
      <div slot="JAM" slot-scope="data">
        <van-switch v-model="items2[data.index].JAM"
                    @change="onSwitch('sta_block', items2[data.index].MAC, data.index, items2[data.index].JAM)" />
      </div>
    </b-table>
  </div>
</template>

<script>
/* eslint-disable no-restricted-syntax */

import CubeNav from '@/components/CubeNav';
import axios from 'axios';

export default {
  name: 'Wifi',
  components: {
    CubeNav,
  },
  data() {
    return {
      scanStatus: 'off',
      fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
      items: [
        {
          Index: 0,
          SSID: '360WIFI-XX',
          BSSID: '11:22:33:44:55:66',
          RSSI: '-80',
          JAM: false,
        },
        {
          Index: 1,
          SSID: '360WIFI-X2',
          BSSID: '11:22:33:44:55:66',
          RSSI: '-94',
          JAM: false,
        },
        {
          Index: 2,
          SSID: '360WIFI-X3',
          BSSID: '11:22:33:44:55:66',
          RSSI: '-81',
          JAM: false,
        },
      ],
      fields2: ['NAME', 'MAC', 'RSSI', 'JAM'],
      items2: [
        {
          Index: 0,
          NAME: 'iPhone',
          MAC: '11:22:33:44:55:66',
          RSSI: '522',
          JAM: false,
        },
        {
          Index: 1,
          NAME: 'Android',
          MAC: '11:22:33:44:55:66',
          RSSI: '94',
          JAM: false,
        },
        {
          Index: 2,
          NAME: 'iPhone',
          MAC: '11:22:33:44:55:66',
          RSSI: '101',
          JAM: false,
        },
      ],
      channel: null,
      defaultChannel: 6,
      channelList: [],
    };
  },
  methods: {
    onSwitch(api, value, index, isOpen) {
      console.log(api, value, index, isOpen);
      const action = isOpen ? 'on' : 'off';
      axios
        .get(`${process.env.BACKEND_HOST}/${api}/${value}/${action}`)
        .then((response) => {
          console.log(response.data);
          const result = response.data;
          this.$Message.success(result.message);
        })
        .catch((err) => {
          console.log(err.response);
          this.$Message.error('Call process fail');
        });
    },
    onClickScan() {
      // send request with action to backend
      this.scanStatus = this.scanStatus === 'on' ? 'off' : 'on';
      const channel = this.channel === null ? this.defaultChannel : this.channel;
      axios
        .get(`${process.env.BACKEND_HOST}/wifi_scan/${this.scanStatus}/${channel}`)
        .then((response) => {
          const result = response.data;
          console.log(result);
          this.$Message.success(result.message);
          if (this.scanStatus === 'on') {
            this.$timer.start('fetchWifiList');
          } else if (this.scanStatus === 'off') {
            this.$timer.stop('fetchWifiList');
          }
        })
        .catch((err) => {
          console.log(err.response);
          this.$Message.error(err);
        });
    },
    fetchWifiList() {
      if (this.scanStatus === 'on') {
        axios
          .get(`${process.env.BACKEND_HOST}/ap_list`)
          .then((response) => {
            const result = response.data;
            console.log(result);
            // this.$Message.success('Fetch wifi list success.');
            this.items = result[result.data_key];
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Fetch wifi list fail.');
          });
      }
    },
    getChannelList() {
      const channelList = [];
      const numList = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        36,
        40,
        44,
        48,
        52,
        56,
        60,
        64,
        100,
        104,
        108,
        112,
        115,
        120,
        124,
        128,
        132,
        136,
        140,
        149,
        153,
        157,
        161,
        165,
      ];
      for (const num of numList) {
        const channel = {
          value: num,
          label: num,
        };
        channelList.push(channel);
      }
      this.channelList = channelList;
    },
  },
  created() {
    // TODO: 初始化数据
    // TODO: Save the final fresh wifi list when leave page
    // TODO: And restore it when back to this page.
    console.log(`items is: ${this.items}`);
    this.getChannelList();
  },
  timers: {
    fetchWifiList: { time: 3000, autostart: false, repeat: true },
  },
};
</script>

<style scoped>
</style>
