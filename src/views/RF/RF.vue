<template>
  <div class="board">
    <cube-nav/>
    <b-alert :show="showARFAlert" variant="primary" dismissible>
      <h4 class="alert-heading">RF</h4>
      <p>
        In frequency {{latest_arf_item.freq}} found protocol: {{latest_arf_item.protocol}}, data: {{latest_arf_item.data}} signal.<a href="#content">Learn More.</a>
      </p>
    </b-alert>

    <b-alert :show="showCRFAlert" variant="primary" dismissible>
      <h4 class="alert-heading">RF</h4>
      <p>
        In frequency {{latest_crf_item.freq}} found protocol: {{latest_crf_item.protocol}}, data: {{latest_crf_item.data}} signal.<a href="#content">Learn More.</a>
      </p>
    </b-alert>

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
    <!--<div id='content'>-->
      <b-table responsive :items="rfItems" :fields="fields_show">
        <div slot="playback" slot-scope="data">
          <b-button size="sm" variant="primary" @click="onClick(data.index)">Run</b-button>
        </div>
      </b-table>
    <!--</div>-->

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

    <b-table responsive :items="tpmsItems" :fields="fields_input">
      <div slot="voltage" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].voltage" type="text"></b-form-input>
      </div>
      <div slot="pressure" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].pressure" type="text"></b-form-input>
      </div>
      <div slot="temperature" slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].temperature" type="text"></b-form-input>
      </div>
      <div slot='valve' slot-scope="data">
        <b-form-input v-model="tpmsItems[data.index].valve" type="text"></b-form-input>
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

    <b-progress :value="70" variant="danger" :animated="animate" class="mb-3"/>

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
        latest_nfc_item: '',
        showNFCAlert: false,
        latest_arf_item: '',
        showARFAlert: false,
        latest_crf_item: '',
        showCRFAlert: false,
        snifferSwitch: true,
        tpmsSwitch: false,
        attackSwitch: false,
        // if continue animate
        animate: true,
        fields_show: ['data', 'freq', 'protocol', 'modulation', 'playback'],
        fields_input: ['ID', 'voltage', 'pressure', 'temperature', 'valve'],
        rfItems: [],
        tpmsItems: [
          { ID: '20959185', voltage: '', pressure: '', temperature: '', valve: '' },
          { ID: 'eb107f85', voltage: '', pressure: '', temperature: '', valve: '' },
          { ID: 'F0FB2385', voltage: '', pressure: '', temperature: '', valve: '' },
          { ID: '2093ef85', voltage: '', pressure: '', temperature: '', valve: '' },
        ],
      };
    },
    methods: {
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
            console.log(result);
            if (response.status === 304) {
              return;
            }
            this.latest_nfc_item = result[result.data_key];
            this.showNFCAlert = true;
            this.$Message.success('Detect new nfc data.');
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Fetch nfc data fail.');
          });
      },
      serialSend(parameter) {
        axios
          .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
          .then((response) => {
            const result = response.data;
            console.log(result);
            this.$Message.success('Execute success.');
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Execute fail.');
          });
      },
      fetchRFItem() {
        const dataAPIs = ['arf', 'crf'];
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
              console.log(result);
              if (response.status === 304) {
                return;
              }
              const dataKey = result.data_key;
              that.$Message.success(`Detect new ${dataKey} data.`);
              const isExist = that.rfItems.indexOf(result[dataKey]) !== -1;
              if (isExist) {
                return;
              }
              that.rfItems.unshift(result[dataKey]);
              if (dataKey === 'arf_item') {
                that.latest_arf_item = result[dataKey];
                that.showARFAlert = true;
              } else if (dataKey === 'crf_item') {
                that.latest_crf_item = result[dataKey];
                that.showCRFAlert = true;
              }
            })
            .catch((err) => {
              console.log(err.response);
              that.$Message.error(`Fetch ${api} data fail.`);
            });
        }
      },
      fetchAllRFItems() {
        const dataAPIs = ['arf', 'crf'];
        const that = this;
        for (const api of dataAPIs) {
          axios
          .get(`${process.env.BACKEND_HOST}/all_rf_item/${api}`)
          .then((response) => {
            const result = response.data;
            // todo: write test code
            console.log(result);
            const dataKey = result.data_key;
            // todo: add Transition animation
            that.$Message.success(`Detect new ${dataKey} data.`);
            that.rfItems = that.rfItems.concat(result[dataKey]);
          })
          .catch((err) => {
            console.log(err.response);
            that.$Message.error(`Fetch ${api} data fail.`);
          });
        }
      },
      onSwitch(switchType) {
        console.log(switchType);
        switch (switchType) {
          case 'sniffer':
            if (this.snifferSwitch) {
              this.$timer.start('fetchRFItem');
              this.$message.info('Start detect new RF item.');
            } else {
              this.$timer.stop('fetchRFItem');
              this.$message.info('Stop detect new RF item.');
            }
            break;
          case 'tpms':
            if (!this.tpmsSwitch) {
              return;
            }
            for (const item of this.tpmsItems) {
              // todo: write test code
              if (!item.voltage && !item.pressure && !item.temperature && !item.valve) {
                console.log('continue tpmsItem');
                // this.$Message.error('You need input one or more.');
                return;
              }
              const parameter = `t${item.ID}${item.voltage}${item.pressure}${item.temperature}${item.valve}`;
              // this.serialSend(parameter);
              const that = this;
              setTimeout(() => {
                that.serialSend(parameter);
                that.$Message.success(`Success put ${parameter}`);
              }, 700);
            }
            this.$Message.success('Send all valid item to process!');
            break;
          case 'attack':
            // 暂不实现
            break;
          default:
            break;
        }
      },
      onClick(index) {
        console.log(index);
        const item = this.rfItems[index];
        const parameter = `"rfreq:${item.freq};protocol:${item.protocol};modulation:${item.modulation};data:${item.data}"`;
        this.serialSend(parameter);
      },
    },
    created() {
      if (this.snifferSwitch) {
        this.$timer.start('fetchAllRFItems');
        this.$timer.start('fetchRFItem');
        this.$timer.start('fetchNFCData');
      }
    },
    timers: {
      fetchAllRFItems: { time: 3000, autostart: false, repeat: false },
      fetchRFItem: { time: 3000, autostart: false, repeat: true },
      fetchNFCData: { time: 3000, autostart: false, repeat: true },
    },
  };
</script>

<style scoped>

</style>
