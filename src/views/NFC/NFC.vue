<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube NFC Manage</h1>
    <h3 class="text-center">Safety Risk Detection for Cards Working at 125Khz, 13.5Mhz.</h3>
    <br/>
    <!-- Read List -->
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Read</h5>
        </b-col>
        <b-col cols="2">
          <van-switch v-model="readSwitch" @change="onSwitchRead" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="WRITE" slot-scope="data">
        <van-switch v-model="items[data.index].WRITE" @change="onSwitchAction('nw', items[data.index].WRITE, items[data.index].VID, items[data.index].ID)" size="25px"/>
      </div>
      <div slot="SIMULATE" slot-scope="data">
        <van-switch v-model="items[data.index].SIMULATE" @change="onSwitchAction('ns', items[data.index].SIMULATE, items[data.index].VID, items[data.index].ID)" size="25px"/>
      </div>
    </b-table>

    <!-- Write List -->
    <b-container style="margin-top: 15px">
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Write</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="writeSwitch" @change="onSwitchAction('nw', writeSwitch)" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row>
        <b-col cols="4">
          <b-form-input v-model="writeVid"
                        type="text"
                        placeholder="VID">
          </b-form-input>
        </b-col>
        <b-col cols="8">
          <b-form-input v-model="writeId"
                        type="text"
                        placeholder="ID">
          </b-form-input>
        </b-col>
      </b-row>
    </b-container>

    <!-- Simulate List -->
    <b-container style="margin-top: 15px">
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Simulate</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="simulateSwitch" @change="onSwitchAction('ns', simulateSwitch)" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-container fluid>
      <b-row>
        <b-col cols="4">
          <b-form-input v-model="simulateVid"
                        type="text"
                        placeholder="VID">
          </b-form-input>
        </b-col>
        <b-col cols="8">
          <b-form-input v-model="simulateId"
                        type="text"
                        placeholder="ID">
          </b-form-input>
        </b-col>
      </b-row>
    </b-container>

  </div>
</template>

<script>
  /* eslint-disable no-restricted-syntax */

  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';

  function isValidIds(Vid, Id) { return /^\w+$/.test(Vid) && /^\w+$/.test(Id); }
  export default {
    name: 'NFC',
    components: {
      CubeNav,
    },
    data() {
      return {
        switchSize: '25px',
        readSwitch: true,
        // TODO: Confirm if necessary to disable input when false
        writeSwitch: false,
        simulateSwitch: false,
        writeVid: null,
        writeId: null,
        simulateVid: null,
        simulateId: null,
        fields: ['VID', 'ID', 'WRITE', 'SIMULATE'],
        items: [
          { VID: '050', ID: '000279080', WRITE: false, SIMULATE: false },
        ],
      };
    },
    methods: {
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
            this.items = [result[result.data_key]];
            this.$Message.info('Detect new nfc data.');
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
      onSwitchRead(checked) {
        if (checked) {
          this.$timer.start('fetchNFCData');
        } else {
          this.$timer.stop('fetchNFCData');
        }
      },
      onSwitchAction(actionType, isOpen, VID, ID) {
        if (!isOpen) {
          return;
        }

        if (VID && ID) {
          const parameter = `${actionType}${VID}${ID}`;
          this.serialSend(parameter);
          return;
        }
        switch (actionType) {
          case 'nw':
            if (!(this.writeVid && this.writeId)) {
              this.$Message.error('Please input ID and VID');
              this.writeSwitch = !this.writeSwitch;
            } else if (!(isValidIds(this.writeVid, this.writeId))) {
              this.$Message.error('Please input the right ID and VID');
              this.writeSwitch = !this.writeSwitch;
            } else {
              const parameter = `${actionType}${this.writeVid}${this.writeId}`;
              this.serialSend(parameter);
            }
            break;
          case 'ns':
            if (!(this.simulateVid && this.simulateId)) {
              this.$Message.error('Please input the right ID and VID');
              this.simulateSwitch = !this.simulateSwitch;
            } else if (!(isValidIds(this.simulateVid, this.simulateId))) {
              this.$Message.error('Please input the right ID and VID');
              this.simulateSwitch = !this.simulateSwitch;
            } else {
              const parameter = `${actionType}${this.simulateVid}${this.simulateId}`;
              this.serialSend(parameter);
            }
            break;
          default:
            this.$Message.error('Please input the right API');
            break;
        }
      },
    },
    created() {
      if (this.readSwitch) {
        this.$timer.start('fetchNFCData');
      } else {
        this.$timer.stop('fetchNFCData');
      }

      if (this.$route.params.latest_nfc_item) {
        this.items = [this.$route.params.latest_nfc_item];
      }
    },
    timers: {
      fetchNFCData: { time: 3000, autostart: false, repeat: true },
    },
  };
</script>

<style scoped>

</style>
