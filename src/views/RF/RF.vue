<template>
  <div class="board">
    <cube-nav/>
    <div v-for="latest_arf_item in latest_arf_items" >
      <b-alert show variant="primary" dismissible>
        <h4 class="alert-heading">RF</h4>
        <p>
          In frequency {{latest_arf_item.freq}} found prot: {{latest_arf_item.prot}}, data: {{latest_arf_item.data}} signal.<a href="#content">Learn More.</a>
        </p>
      </b-alert>
    </div>
  <div v-for="latest_crf_item in latest_crf_items" >
    <b-alert show variant="primary" dismissible>
      <h4 class="alert-heading">RF</h4>
      <p>
        In frequency {{latest_crf_item.freq}} found prot: {{latest_crf_item.prot}}, data: {{latest_crf_item.data}} signal.<a href="#content">Learn More.</a>
      </p>
    </b-alert>
  </div>
    <b-alert :show="showNFCAlert" variant="success" dismissible>
      <h4 class="alert-heading">NFC</h4>
      <p>
        Found NFC card ID: {{latest_nfc_item.ID}}, <u @click="clickNFC">Learn More.</u>
      </p>
    </b-alert>
    <h1 class="text-center">Cube RF Manage</h1>
    <h3 class="text-center">Security Risk Detection on 433Mhz,315Mhz Devices</h3>
    <br/><br/>
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Sniffer</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="snifferSwitch" @change="onSwitch('sniffer')" ></van-switch>
        </b-col>
      </b-row>
    </b-container>
    <div>
      <b-table id="break-word-list" :items="rfItems" :fields="fields_show" :per-page="sniffPerPage" :current-page="sniffCurrentPage">
        <div slot="play" slot-scope="data">
          <b-button type="default" size="sm" variant="primary" @click="onClick(data.index)">Run</b-button>
        </div>
      </b-table>
      <b-pagination align="center" v-if="rfItems.length" size="sm" :total-rows="rfItems.length" v-model="sniffCurrentPage" :per-page="sniffPerPage">
      </b-pagination>
      <div>
        <van-loading type="spinner" color="black" v-if="!rfItems.length&&snifferSwitch" id="aligncenter" />
        <div style="clear: both;"></div>
      </div>
      <!--<Spin fix v-if="spinShow"></Spin>-->
    </div>

    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>TPMS</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="tpmsSwitch" @change="onSwitch('tpms')" />
        </b-col>
      </b-row>
    </b-container>

    <b-table id="break-word-list" responsive :items="tpmsItems" :fields="fields_input">
      <div slot="VOL" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].VOL" type="text"></b-form-input>
      </div>
      <div slot="PRESS" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].PRESS" type="text"></b-form-input>
      </div>
      <div slot="TEMP" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].TEMP" type="text"></b-form-input>
      </div>
      <div slot='VALVE' slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].VALVE" type="text"></b-form-input>
      </div>
    </b-table>


    <!-- Attack -->
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Attack</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="attackSwitch" @change="onSwitch('attack')" />
        </b-col>
      </b-row>
    </b-container>

    <b-progress :value="attackProgress" variant="danger" :animated="animate" class="mb-3"/>
    <Select size="large" v-model="protocol" placeholder="Protocol">
      <Option value="PT224X">PT224X</Option>
      <Option value="PT226X" disabled>PT226X</Option>
      <!--<Option v-for="item in protocolList" :value="item.value" :key="item.value">{{ item.label }}</Option>-->
    </Select>
    <br/><br/>
    <b-container>
      <b-row align-h="between">
        <b-col cols="6" style="padding-left: 0">
          <b-form-input v-model="attackValueLeft" type="text"></b-form-input>
        </b-col>
        <b-col cols="6" style="padding-right: 0">
          <b-form-input v-model="attackValueRight" type="text"></b-form-input>
        </b-col>
      </b-row>
    </b-container>
    <br/><br/>

    <Row type="flex" justify="center" class="code-row-bg">
        <Col span="4">
          <div v-finger:touch-start="sendDirection.bind(this, ['w', 1])"
               v-finger:long-tap="sendDirection.bind(this, ['w', 1])"
               v-finger:touch-end="sendDirection.bind(this, ['w', 0])">
            <van-button type="default">&and;</van-button>
          </div>
        </Col>
    </Row>

    <Row type="flex" justify="space-between" class="code-row-bg">
      <Col span="1"></Col>
      <Col span="4">
        <div v-finger:touch-start="sendDirection.bind(this, ['a', 1])"
             v-finger:long-tap="sendDirection.bind(this, ['a', 1])"
             v-finger:touch-end="sendDirection.bind(this, ['a', 0])">
          <van-button type="default" id="rotateLeft">&and;</van-button>
        </div>
      </Col>
      <Col span="4">
        <div v-finger:touch-start="sendDirection.bind(this, ['d', 1])"
             v-finger:long-tap="sendDirection.bind(this, ['d', 1])"
             v-finger:touch-end="sendDirection.bind(this, ['d', 0])">
          <van-button type="default" id="rotateRight">&and;</van-button>
        </div>
      </Col>
      <Col span="1"></Col>
    </Row>
    <!--<a @mouseover="sendDirection(this, ['s', 1])" @mouseup="sendDirection(this, ['s', 1])">S</a>-->
    <Row type="flex" justify="center" class="code-row-bg">
      <Col span="4">
        <div v-finger:touch-start="sendDirection.bind(this, ['s', 1])"
             v-finger:long-tap="sendDirection.bind(this, ['s', 1])"
            v-finger:touch-end="sendDirection.bind(this, ['s', 0])">
          <van-button type="default">&or;</van-button>
        </div>
      </Col>
    </Row>
    <br/><br/>
  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';
  import router from '@/router';

  export default {
    name: 'RF',
    components: {
      CubeNav,
    },
    data() {
      return {
        attackProgress: 0,
        sniffPerPage: 10,
        sniffCurrentPage: 1,
        attackValueLeft: '1755',
        attackValueRight: '17a5',
        spinShow: true,
        protocol: 'PT224X',
        latest_nfc_item: '',
        showNFCAlert: false,
        latest_arf_items: [],
        latest_crf_items: [],
        snifferSwitch: true,
        tpmsSwitch: false,
        attackSwitch: false,
        // if continue animate
        animate: true,
        fields_show: ['data', 'freq', 'prot', 'MOD', 'play'],
        fields_input: ['ID', 'VOL', 'PRESS', 'TEMP', 'VALVE'],
        rfItems: [],
        tpmsItems: [
          { ID: '20959185', VOL: 'a0', PRESS: '20', TEMP: '60', VALVE: '08' },
          { ID: 'eb107f85', VOL: 'a0', PRESS: '20', TEMP: '60', VALVE: '08' },
          { ID: 'F0FB2385', VOL: 'a0', PRESS: '20', TEMP: '60', VALVE: '08' },
          { ID: '2093ef85', VOL: 'a0', PRESS: '20', TEMP: '60', VALVE: '08' },
        ],
        protocolList: [
          {
            value: 'PT226X',
            label: 'PT226X',
            disabled: true,
          },
          {
            value: 'PT224X',
            label: 'PT224X',
            disabled: false,
          },
        ],
      };
    },
    methods: {
      sendDirection(values) {
        const direction = values[0];
        const value = values[1];
        axios
          .get(`${process.env.BACKEND_HOST}/send_direction/${direction}/${value}`)
          .catch((err) => {
            if (err.response) {
              this.$Message.error(err.response.data.message);
            } else {
              this.$Message.error('Request fail');
            }
          });
      },
      clickNFC() {
        router.push({
          path: '/nfc',
          name: 'NFC',
          params: {
            latest_nfc_item: this.latest_nfc_item,
          },
        });
      },
      fetchNFCData() {
        axios
          .get(`${process.env.BACKEND_HOST}/nfc_item`, {
            validateStatus(status) {
              return status < 400; // Reject only if the status code is greater than or equal to 400
            },
          })
          .then((response) => {
            const result = response.data;
            if (response.status === 304) {
              return;
            }
            this.latest_nfc_item = result[result.data_key];
            this.showNFCAlert = true;
            this.$Message.info(result.message);
          })
          .catch((err) => {
            if (err.response) {
              this.$Message.error(err.response.data.message);
            } else {
              this.$Message.error('Request fail');
            }
          });
      },
      serialSend(parameter, isAlert) {
        axios
          .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
          .then((response) => {
            const result = response.data;
            if (isAlert === true) {
              this.$Message.success(result.message);
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
      fetchRFItem() {
        const dataAPIs = ['crf'];
        const that = this;
        for (const api of dataAPIs) {
          axios
            .get(`${process.env.BACKEND_HOST}/rf_item/${api}`, {
              validateStatus(status) {
                return status < 400; // Reject only if the status code is greater than or equal to 400
              },
            })
            .then((response) => {
              const result = response.data;
              // todo: write test code
              if (response.status === 304) {
                return;
              }
              const dataKey = result.data_key;
              if (result[dataKey].length > 0) {
                that.$Message.success(result.message);
              }
              for (const item of result[dataKey]) {
                that.rfItems.unshift(item);
              }
              // todo: change as for item of them :display notice
              if (dataKey === 'arf_item') {
                that.latest_arf_items = result[dataKey];
              } else if (dataKey === 'crf_item') {
                that.latest_crf_items = result[dataKey];
              }
            })
            .catch((err) => {
              if (err.response) {
                this.$Message.error(err.response.data.message);
              } else {
                this.$Message.error('Request fail');
              }
            });
        }
      },
      fetchAllRFItems() {
        this.spinShow = true;
        const dataAPIs = ['crf'];
        const that = this;
        for (const api of dataAPIs) {
          axios
          .get(`${process.env.BACKEND_HOST}/all_rf_item/${api}`)
          .then((response) => {
            const result = response.data;
            // todo: write test code
            const dataKey = result.data_key;
            // todo: add Transition animation
            that.$Message.success(result.message);
            // for (const item of result[dataKey]) {
            //   that.rfItems.add(item);
            // }
            that.rfItems = that.rfItems.concat(result[dataKey]);
            this.spinShow = false;
          })
          .catch((err) => {
            this.spinShow = false;
            if (err.response) {
              this.$Message.error(err.response.data.message);
            } else {
              this.$Message.error('Request fail');
            }
          });
        }
      },
      getAttackProgress() {
        const that = this;
        axios
          .get(`${process.env.BACKEND_HOST}/attack_status`)
          .then((response) => {
            const result = response.data;
            // todo: write test code
            const dataKey = result.data_key;
            that.attackProgress = parseInt(result[dataKey], 0);
            if (that.attackProgress === 100) {
              that.$timer.stop('getAttackProgress');
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
      onSwitch(switchType) {
        // let parameter = '';
        switch (switchType) {
          case 'sniffer':
            if (this.snifferSwitch) {
              this.$timer.start('fetchRFItem');
              this.$Message.info('Start detect new RF item.');
            } else {
              this.$timer.stop('fetchRFItem');
              this.$Message.info('Stop detect new RF item.');
            }
            break;
          case 'tpms':
            if (!this.tpmsSwitch) {
              return;
            }
            for (const item of this.tpmsItems) {
              // todo: write test code
              if (!item.VOL && !item.PRESS && !item.TEMP && !item.VALVE) {
                return;
              }
              const parameter = `t${item.ID}${item.VOL}${item.PRESS}${item.TEMP}${item.VALVE}`;
              const that = this;
              setTimeout(() => {
                that.serialSend(parameter, true);
                that.$Message.success(`Success put ${parameter}`);
              }, 700);
            }
            this.$Message.success('Send all valid item to process!');
            break;
          case 'attack':
            if (!this.attackSwitch) {
              this.attackProgress = 0;
              this.$timer.stop('getAttackProgress');
              return;
            }
            if (!this.attackValueLeft && this.attackValueRight) {
              this.$Message.error('Please input at least on parameter.');
              this.attackSwitch = false;
              return;
            }
            if (this.protocol === 'PT224X') {
              const parameter = `rc2start${this.attackValueLeft}end${this.attackValueRight}`;
              this.serialSend(parameter, false);
            } else if (this.protocol === 'PT224X') {
              const parameter = `rc1start${this.attackValueLeft}end${this.attackValueRight}`;
              this.serialSend(parameter, false);
            } else {
              this.$Message.error('Please select right protocol.');
              return;
            }
            this.$timer.start('getAttackProgress');
            break;
          default:
            break;
        }
      },
      onClick(index) {
        const actualIndex = ((this.sniffCurrentPage - 1) * this.sniffPerPage) + index;
        const item = this.rfItems[actualIndex];
        const parameter = `"rfreq:${item.freq};protocol:${item.prot};modulation:${item.MOD};data:${item.data}"`;
        this.serialSend(parameter, true);
      },
    },
    created() {
      if (this.snifferSwitch) {
        this.$timer.start('fetchRFItem');
        this.$timer.start('fetchNFCData');
      }
    },
    timers: {
      fetchAllRFItems: { time: 0, autostart: true, repeat: false },
      fetchRFItem: { time: 3000, autostart: false, repeat: true },
      fetchNFCData: { time: 3000, autostart: false, repeat: true },
      getAttackProgress: { time: 400, autostart: false, repeat: true },
    },
  };
</script>

<style>
  #break-word-list td[aria-colindex] {
    max-width: 6em;
    word-wrap: break-word;
    padding-right: 4px;
    padding-left: 4px;
    text-align:center;
    vertical-align:middle;
  }
  td[aria-colindex] > div {
    width: 3.8em;
  }

  .code-row-bg {
    padding-top: 1.2em;
  }

  .btn-outline-primary {
    width: 2.8em;
    height: 2.6em;
    font-size: 1.5em;
    text-align: center;
    display: inline-block;
  }

  #rotateRight {
    /* Safari */
    -webkit-transform: rotate(90deg);
    /* Firefox */
    -moz-transform: rotate(90deg);
    /* IE */
    -ms-transform: rotate(90deg);
    /* Opera */
    -o-transform: rotate(90deg);
    /* Internet Explorer */
    filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=1);
  }
  #rotateLeft {
    /* Safari */
    -webkit-transform: rotate(-90deg);
    /* Firefox */
    -moz-transform: rotate(-90deg);
    /* IE */
    -ms-transform: rotate(-90deg);
    /* Opera */
    -o-transform: rotate(-90deg);
    /* Internet Explorer */
    filter: progid:DXImageTransform.Microsoft.BasicImage(rotation=3);
  }
</style>
