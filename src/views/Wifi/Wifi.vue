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
      <b-table :items="apList" :fields="fields" :per-page="apPerPage" :current-page="apCurrentPage">
        <div slot="JAM" slot-scope="data">
          <van-switch v-model="apList[(apCurrentPage-1) * apPerPage + data.index].JAM"
                      @change="onSwitch('ap_block', apList[(apCurrentPage-1) * apPerPage + data.index].BSSID,
                      data.index, apList[(apCurrentPage-1) * apPerPage + data.index].JAM)" />
        </div>
      </b-table>
      <b-pagination align="center" v-if="apCount" size="sm" :total-rows="apCount" v-model="apCurrentPage" :per-page="apPerPage">
      </b-pagination>
      <Spin fix v-if="apSpinShow"></Spin>
    </div>
    <br/><br/>

    <!-- Client list -->
    <h5>Client List</h5>
    <div>
      <b-table :items="staList" :fields="fields2" :per-page="staPerPage" :current-page="staCurrentPage">
        <div slot="JAM" slot-scope="data">
          <van-switch v-model="staList[(staCurrentPage-1) * staPerPage + data.index].JAM"
                      @click="onClickSwitch"
                      @input="onInputSwitch"
                      @change="onSwitch('sta_block', staList[(staCurrentPage-1) * staPerPage + data.index].MAC,
                      data.index, staList[(staCurrentPage-1) * staPerPage + data.index].JAM)" />
        </div>
      </b-table>
      <Spin fix v-if="staSpinShow"></Spin>
    </div>
    <b-pagination align="center" v-if="staCount" size="sm" :total-rows="staCount" v-model="staCurrentPage" :per-page="staPerPage">
    </b-pagination>
  </div>
</template>

<script>
/* eslint-disable no-restricted-syntax */

import CubeNav from '@/components/CubeNav';
import axios from 'axios';
import { mapState, mapGetters, mapActions } from 'vuex';
import { Dialog } from 'vant';

export default {
  name: 'Wifi',
  components: {
    CubeNav,
  },
  data() {
    return {
      fields: ['SSID', 'BSSID', 'RSSI', 'JAM'],
      fields2: ['MAC', 'BSSID', 'RSSI', 'JAM'],
      defaultChannel: 6,
      channelList: [],
      apPerPage: 6,
      staPerPage: 6,
      channel: 6,
      apCurrentPage: 1,
      staCurrentPage: 1,
    };
  },
  methods: {
    ...mapActions('WIFI', ['getAPList', 'getSTAList', 'getStarted', 'setScanStatus', 'setChannel', 'setAPSpinShow', 'setSTASpinShow']),
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
      this.setScanStatus(this.scanStatus === 'on' ? 'off' : 'on');
      const channel = this.channel === null ? this.defaultChannel : this.channel;
      axios
        .get(
          `${process.env.BACKEND_HOST}/wifi_scan/${this.scanStatus}/${channel}`,
        )
        .then(() => {
          if (this.scanStatus === 'on') {
            this.$timer.start('fetchWifiList');
            this.$Message.info('Start scan WiFi.');
            this.setAPSpinShow(true);
            this.setSTASpinShow(true);
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
      // console.log(this.getAPList);
      this.getAPList().catch((err) => {
        if (err.response) {
          this.$Message.error(err.response.data.message);
        } else {
          this.$Message.error('Request fail');
        }
      });
      this.getSTAList().catch((err) => {
        if (err.response) {
          this.$Message.error(err.response.data.message);
        } else {
          this.$Message.error('Request fail');
        }
      });
    },
    getChannelList() {
      const channelList = [];
      const numList = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 40, 44, 48,
        52, 56, 60, 64, 100, 104, 108, 112, 115, 120, 124, 128, 132,
        136, 140, 149, 153, 157, 161, 165,
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
    onInputSwitch(checked) {
      Dialog.confirm({
        title: '提醒',
        message: '是否切换开关？',
      }).then(() => {
        console.log('I am been input!', checked);
      });
    },
    onClickSwitch() {
      Dialog.confirm({
        title: '提醒',
        message: '被点击了！',
      }).then(() => {
        console.log('I am been click!');
      });
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
  computed: {
    ...mapState(
      'WIFI',
      ['apList',
        // 'staList',
        'apSpinShow',
        'staSpinShow',
        'scanStatus',
      ]),
    ...mapGetters('WIFI', ['staCount', 'apCount']),
    staList: {
      get() {
        return this.$store.state.WIFI.staList;
      },
      set(value) {
        console.log(value);
        // this.$store.commit('updateMessage', value);
      },
    },
  },
  // watch: {
  //   staList: {
  //     handler(val, oldVal) {
  //       console.log('a thing changed');
  //       console.log(val, oldVal, val === oldVal);
  //     },
  //     deep: true,
  //   },
  // },
};
</script>

<style>
  td[aria-colindex] {
    overflow: hidden!important;
    text-overflow:ellipsis!important;
    white-space: nowrap!important;
    max-width: 6em;
    padding-right: 4px;
    padding-left: 4px;
    text-align:center;
    vertical-align:middle;
  }
</style>
