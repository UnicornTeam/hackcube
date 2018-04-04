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
          <b-button size="sm" variant="primary" v-if="!apList[((apCurrentPage-1) * apPerPage) + data.index].JAM"
                    @click="onClickJAM('ap_block', data.index)">
            Run</b-button>
          <b-button size="sm" variant="danger" v-if="apList[((apCurrentPage-1) * apPerPage) + data.index].JAM"
                    @click="onClickJAM('ap_block', data.index)">
            Stop</b-button>
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
          <b-button size="sm" variant="primary" v-if="!staList[((staCurrentPage-1) * staPerPage) + data.index].JAM"
                    @click="onClickJAM('sta_block', data.index)">
            Run</b-button>
          <b-button size="sm" variant="danger" v-if="staList[((staCurrentPage-1) * staPerPage) + data.index].JAM"
                    @click="onClickJAM('sta_block', data.index)">
            Stop</b-button>
        </div>
      </b-table>
      <Spin fix v-if="staSpinShow"></Spin>
    </div>
    <b-pagination align="center" v-if="staCount" size="sm" :total-rows="staCount" v-model="staCurrentPage" :per-page="staPerPage">
    </b-pagination>
  </div>
</template>

<script>

import CubeNav from '@/components/CubeNav';
import axios from 'axios';
import { mapState, mapGetters, mapActions } from 'vuex';

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
    ...mapActions('WIFI', ['getAPList', 'getSTAList', 'getStarted', 'setScanStatus', 'setChannel',
      'setAPSpinShow', 'setSTASpinShow', 'changeAPJAMByIndex', 'changeSTAJAMByIndex']),
    onClickJAM(api, index) {
      let actualIndex;
      let value;
      let isRunning;
      this.setScanStatus('off');
      this.$timer.stop('fetchWifiList');
      if (api === 'ap_block') {
        actualIndex = ((this.apCurrentPage - 1) * this.apPerPage) + index;
        value = this.apList[actualIndex].BSSID;
        isRunning = this.apList[actualIndex].JAM;
        this.changeAPJAMByIndex(actualIndex);
      } else if (api === 'sta_block') {
        actualIndex = ((this.staCurrentPage - 1) * this.staPerPage) + index;
        value = this.staList[actualIndex].MAC;
        isRunning = this.staList[actualIndex].JAM;
        this.changeSTAJAMByIndex(actualIndex);
      } else {
        this.$message.error('Please input the right api');
        return;
      }
      const action = isRunning ? 'off' : 'on';
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
    controlScan(status, channel) {
      axios
        .get(
          `${process.env.BACKEND_HOST}/wifi_scan/${status}/${channel}`,
        )
        .then(() => {
          if (status === 'on') {
            this.$timer.start('fetchWifiList');
            this.$Message.info('Start scan WiFi.');
            this.setAPSpinShow(true);
            this.setSTASpinShow(true);
          } else if (status === 'off') {
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
    onClickScan() {
      // send request with action to backend
      this.setScanStatus(this.scanStatus === 'on' ? 'off' : 'on');
      const channel = this.channel === null ? this.defaultChannel : this.channel;
      this.controlScan(this.scanStatus, channel);
    },
    fetchWifiList() {
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
      // eslint-disable-next-line no-restricted-syntax
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
    this.getChannelList();
  },
  timers: {
    fetchWifiList: { time: 3000, autostart: false, repeat: true },
  },
  computed: {
    ...mapState(
      'WIFI',
      ['apList',
        'staList',
        'apSpinShow',
        'staSpinShow',
        'scanStatus',
      ]),
    ...mapGetters('WIFI', ['staCount', 'apCount']),
  },
  beforeRouteLeave(to, from, next) {
    this.setScanStatus('off');
    this.controlScan('off', this.channel);
    next();
  },
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
