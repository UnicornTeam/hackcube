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
          <h4>Read</h4>
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
          <h4>Write</h4>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="writeSwitch" @change="onSwitch" size="25px"/>
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
          <h4>Simulate</h4>
        </b-col>
        <b-col cols="3">
          <van-switch v-model="simulateSwitch" @change="onSwitch" size="25px"/>
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
      onSwitch() {
        // TODO: Check which item's JAM is true and do more thing.
        // TODO: Check is wifi list or client list's item
        // TODO: Check if read switch
        // TODO: Add more check
        for (const item of this.items) {
          if (item.JAM === true) {
            console.log(item.Index);
          }
        }
      },
    },
  };
</script>

<style scoped>

</style>
