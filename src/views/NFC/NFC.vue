<template>
  <div style="margin: 10px">
    <cube-nav/>

    <h1 class="text-center">Cube NFC Manage</h1>
    <h3 class="text-center">对工作在125Khz, 13.5Mhz的卡片进行安全风险检测</h3>
    <br/>
    <!-- Read List -->
    <b-container>
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Read</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="readSwitch" @change="onSwitch" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-table :items="items" :fields="fields">
      <div slot="WRITE" slot-scope="data">
        <van-switch v-model="items[data.index].WRITE" @change="onSwitch" size="25px"/>
      </div>
      <div slot="BLAST" slot-scope="data">
        <van-switch v-model="items[data.index].BLAST" @change="onSwitch" size="25px"/>
      </div>
      <div slot="SIMULATE" slot-scope="data">
        <van-switch v-model="items[data.index].SIMULATE" @change="onSwitch" size="25px"/>
      </div>
    </b-table>

    <!-- Write List -->
    <b-container style="margin-top: 15px">
      <b-row align-h="between">
        <b-col cols="4">
          <h5>Write</h5>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="writeSwitch" @change="onSwitch('write')" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-container>
      <b-row>
        <b-col cols="4">
          <!-- TODO: Check if only need input one vid ? -->
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
          <van-switch v-model="simulateSwitch" @change="onSwitch('simulate')" size="25px"/>
        </b-col>
      </b-row>
    </b-container>

    <b-container fluid>
      <b-row>
        <b-col cols="4">
          <!-- TODO: Check if only need input one vid ? -->
          <b-form-input v-model="simulateVid"
                        type="text"
                        placeholder="VID">
          </b-form-input>
        </b-col>
        <b-col cols="8" style="padding-left: 0">
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
        readSwitch: false,
        // TODO: Confirm if necessary to disable input when false
        writeSwitch: false,
        simulateSwitch: false,
        writeVid: null,
        writeId: null,
        simulateVid: null,
        simulateId: null,
        fields: ['VID', 'ID', 'WRITE', 'BLAST', 'SIMULATE'],
        items: [
          { Index: 0, VID: '050', ID: '000279080', WRITE: false, BLAST: false, SIMULATE: false },
        ],
      };
    },
    methods: {
      onSwitch(switchType) {
        switch (switchType) {
          case 'write':
            if (!(this.writeVid && this.writeId)) {
              this.$Message.error('请输入ID和VID');
              this.writeSwitch = !this.writeSwitch;
            } else if (!(isValidIds(this.writeVid, this.writeId))) {
              this.$Message.error('请输入规范的ID和VID');
              this.writeSwitch = !this.writeSwitch;
            } else {
              const parameter = `nw${this.writeVid}${this.writeId}`;
              axios
                .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
                .then((response) => {
                  const result = response.data;
                  console.log(result);
                  this.$Message.success('Execute success.');
                })
                .catch((err) => {
                  console.log(err);
                  this.$Message.error('Execute fail.');
                });
            }
            break;
          case 'simulate':
            if (!(this.simulateVid && this.simulateId)) {
              this.$Message.error('请输入ID和VID');
              this.simulateSwitch = !this.simulateSwitch;
            } else if ((isValidIds(this.simulateVid, this.simulateId))) {
              this.$Message.error('请输入规范的ID和VID');
              this.writeSwitch = !this.simulateSwitch;
            } else {
              const parameter = `ns${this.simulateVid}${this.simulateId}`;
              axios
                .get(`${process.env.BACKEND_HOST}/serial_send/${parameter}`)
                .then((response) => {
                  const result = response.data;
                  console.log(result);
                  this.$Message.success('Execute success.');
                })
                .catch((err) => {
                  console.log(err);
                  this.$Message.error('Execute fail.');
                });
            }
            break;
          default:
            break;
        }
      },
    },
    created() {
      // TODO: 初始化数据
      console.log(`items is: ${this.items}`);
    },
  };
</script>

<style scoped>

</style>
