<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube Wifi Manage</h1>
    <h3 class="text-center">Security Risk Detection on 2.4Ghz 5Ghz Devices</h3>
    <br/>
    <b-container>
      <b-row >
        <b-col cols="5" style="padding-left: 0;">
          <h5>WiFi List</h5>
        </b-col>
        <b-col cols="1"></b-col>
        <b-col cols="4" style="padding-right: 4px;">
          <Select v-model="channel" size="small" placeholder="Channel" filterable>
            <Option v-for="item in channelList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </b-col>
        <b-col cols="1">
          <b-button size="sm" variant="primary" v-if="scanStatus==='off'" @click="onClickScan">Scan</b-button>
          <b-button size="sm" variant="danger" v-if="scanStatus==='on'" @click="onClickScan">Stop</b-button>
        </b-col>
      </b-row>
    </b-container>
    <div>
      <b-table :items="ap_items" :fields="fields" :per-page="apPerPage" :current-page="apCurrentPage">
        <div slot="JAM" slot-scope="data">
          <van-switch v-model="ap_items[(apCurrentPage-1) * apPerPage + data.index].JAM"
                      @change="onSwitch('ap_block', ap_items[(apCurrentPage-1) * apPerPage + data.index].BSSID,
                      data.index, ap_items[(apCurrentPage-1) * apPerPage + data.index].JAM)" />
        </div>
      </b-table>
      <b-pagination align="center" v-if="ap_items.length" size="sm" :total-rows="ap_items.length" v-model="apCurrentPage" :per-page="apPerPage">
      </b-pagination>
      <Spin fix v-if="apSpinShow"></Spin>
    </div>
    <br/><br/>

    <!-- Client list -->
    <h5>Client List</h5>
    <div>
      <b-table :items="sta_items" :fields="fields2" :per-page="staPerPage" :current-page="staCurrentPage">
        <div slot="JAM" slot-scope="data">
          <van-switch v-model="sta_items[(staCurrentPage-1) * staPerPage + data.index].JAM"
                      @change="onSwitch('sta_block', sta_items[(staCurrentPage-1) * staPerPage + data.index].MAC,
                      data.index, sta_items[(staCurrentPage-1) * staPerPage + data.index].JAM)" />
        </div>
      </b-table>
      <Spin fix v-if="staSpinShow"></Spin>
    </div>
    <b-pagination align="center" v-if="sta_items.length" size="sm" :total-rows="sta_items.length" v-model="staCurrentPage" :per-page="staPerPage">
    </b-pagination>
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
      apSpinShow: false,
      staSpinShow: false,
      scanStatus: 'off',
      fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
      ap_items: [],
      fields2: ['MAC', 'BSSID', 'RSSI', 'JAM'],
      sta_items: [],
      channel: 6,
      defaultChannel: 6,
      channelList: [],
      apPerPage: 6,
      apCurrentPage: 1,
      staPerPage: 6,
      staCurrentPage: 1,
    };
  },
  methods: {
    onSwitch(api, value, index, isOpen) {
      this.$timer.stop('fetchWifiList');
      const action = isOpen ? 'on' : 'off';
      axios
        .get(`${process.env.BACKEND_HOST}/${api}/${value}/${action}`)
        .then((response) => {
          const result = response.data;
          this.$Message.success(result.message);
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    onClickScan() {
      // send request with action to backend
      this.scanStatus = this.scanStatus === 'on' ? 'off' : 'on';
      const channel =
        this.channel === null ? this.defaultChannel : this.channel;
      axios
        .get(
          `${process.env.BACKEND_HOST}/wifi_scan/${this.scanStatus}/${channel}`,
        )
        .then(() => {
          if (this.scanStatus === 'on') {
            this.$timer.start('fetchWifiList');
            this.$Message.info('Start scan WiFi.');
            this.apSpinShow = true;
            this.staSpinShow = true;
          } else if (this.scanStatus === 'off') {
            this.$timer.stop('fetchWifiList');
            this.$Message.info('Stop scan WiFi.');
          }
        })
        .catch((err) => {
          if (err.response) {
            this.$Message.error(err.response.data.message);
          } else {
            this.$Message.error('Request fail');
          }
        });
    },
    fetchWifiList() {
      if (this.scanStatus === 'on') {
        const apiList = ['ap_list', 'sta_list'];
        for (const api of apiList) {
          axios
            .get(`${process.env.BACKEND_HOST}/${api}`, {
              validateStatus(status) {
                return status < 400;
              },
            })
            .then((response) => {
              const result = response.data;
              if (response.status === 304) {
                this.apSpinShow = false;
                this.staSpinShow = false;
                return;
              }
              // this.$Message.success('Fetch wifi list success.');
              if (api === 'ap_list') {
                this.ap_items = result[result.data_key];
                this.apSpinShow = false;
              } else {
                this.sta_items = result[result.data_key];
                this.staSpinShow = false;
              }
            })
            .catch((err) => {
              this.apSpinShow = false;
              this.staSpinShow = false;
              if (err.response) {
                this.$Message.error(err.response.data.message);
              } else {
                this.$Message.error('Request fail');
              }
            });
        }
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
    // TODO: Save the final fresh wifi list when leave page
    // TODO: And restore it when back to this page.
    this.getChannelList();
  },
  timers: {
    fetchWifiList: { time: 3000, autostart: false, repeat: true },
  },
};
</script>

<style scoped>
</style>
