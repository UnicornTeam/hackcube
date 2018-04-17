<template>
  <div class="board">
    <cube-nav/>
    <div v-for="latest_crf_item in latest_crf_items" >
      <b-alert show variant="primary" dismissible>
        <h4 class="alert-heading">RF</h4>
        <p>
          In frequency {{latest_crf_item.freq}} found prot: {{latest_crf_item.prot}}, data: {{latest_crf_item.data}} signal.<u @click="clickRF">Learn More.</u>
        </p>
      </b-alert>
    </div>
    <b-alert :show="showNFCAlert" variant="success" dismissible>
      <h4 class="alert-heading">NFC</h4>
      <p>
        Found NFC card ID: {{latest_nfc_item.ID}}, <u @click="clickNFC">Learn More.</u>
      </p>
    </b-alert>
    <h1 class="text-center">Cube Status Manage</h1>
    <h3 class="text-center">Display Cube device status</h3>
    <br/>
    <h5 class="text-center">Electricity</h5>
    <b-progress :value="energyPercent"
                variant="dark"
    ></b-progress>
    <br/>
    <h5 class="text-center">Storage</h5>
    <b-progress :value="storage.percent"
                variant="dark"
    ></b-progress>
    <div>
      <p class="alignleft">Used: {{storage.used}}GB</p>
      <p class="alignright">Free: {{storage.free}}GB</p>
      <div style="clear: both;"></div>
    </div>

    <br/><br/>

    <h5>Upload arduino firmware</h5>
    <Upload
      :data="extraDataArdu"
      :on-success="onUploadSuccess"
      :on-error="onUploadError"
      :action="uploadHost">
      <Button type="ghost" icon="ios-cloud-upload-outline">Upload</Button>
    </Upload>

    <div class="text-center">
      <van-button :loading="spinShow" @click="onClick">Submit</van-button>
      <!--<Button type="ghost" >Submit</Button>-->
    </div>
    <br/>
    <div>

      <Input readonly v-model="updateLog" type="textarea" :autosize="{minRows: 6,maxRows: 14}" placeholder="Upload log..."></Input>
    </div>

  </div>
</template>

<script>
  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';
  import AxiosMixin from '../axios-mixin';

  export default {
    name: 'INFO',
    components: {
      CubeNav,
    },
    mixins: [AxiosMixin],
    data() {
      return {
        spinShow: false,
        uploadHost: process.env.UPLOAD_API,
        updateLog: '',
        energyPercent: 78,
        storage: {
          percent: 50,
          used: 10,
          free: 10,
        },
        extraDataPie: { type: 'INFO-Pie' },
        extraDataArdu: { type: 'INFO-Ardu' },
        uploadedFilePath: '',
        latest_crf_items: [],
        showNFCAlert: false,
        latest_nfc_item: '',
      };
    },
    methods: {
      fetchStorageStatus() {
        axios
          .get(`${process.env.BACKEND_HOST}/hd_info`)
          .then((response) => {
            const result = response.data;
            this.storage = result[result.data_key][0];
          })
          .catch((err) => {
            if (err.response) {
              this.$Message.error(err.response.data.message);
            } else {
              this.$Message.error('Request fail');
            }
          });
      },
      getEnergyProgress() {
        const that = this;
        axios
          .get(`${process.env.BACKEND_HOST}/energy_status`)
          .then((response) => {
            const result = response.data;
            // todo: write test code
            const dataKey = result.data_key;
            that.energyPercent = parseInt(result[dataKey], 0);
            if (that.energyPercent === 100) {
              that.$timer.stop('getEnergyProgress');
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
      fetchUpdateLog() {
        axios
          .get(`${process.env.BACKEND_HOST}/update_firmware_log`, {
            validateStatus(status) {
              return status < 400; // Reject only if the status code is greater than or equal to 400
            },
          })
          .then((response) => {
            const result = response.data;
            if (response.status === 304) {
              return;
            }
            this.spinShow = false;
            this.updateLog = result[result.data_key];
          })
          .catch((err) => {
            this.spinShow = false;
            if (err.response) {
              this.$Message.error(err.response.data.message);
            } else {
              this.$Message.error('Request fail');
            }
          });
      },
      onClick() {
        if (this.uploadedFilePath) {
          this.spinShow = true;
          this.$timer.start('fetchUpdateLog');
          axios
          .post(`${process.env.BACKEND_HOST}/update_firmware`, { uploadedFilePath: this.uploadedFilePath })
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
        } else {
          this.$Message.error('Please upload file before submit!');
        }
      },
      onUploadSuccess(response, file) {
        this.uploadedFilePath = `/root/user_file/INFO/arduino/${file.name}`;
        this.$Message.success(`Upload ${file.name} success`);
      },
      onUploadError(error, file, fileList) {
        this.$Message.error(`Upload ${fileList.name} fail`);
      },
    },
    timers: {
      fetchUpdateLog: { time: 1000, autostart: false, repeat: true },
      fetchStorageStatus: { time: 0, autostart: true, repeat: false },
      getEnergyProgress: { time: 100, autostart: true, repeat: false },
      fetchCRFItems: { time: 3200, autostart: true, repeat: true },
      fetchNFCData: { time: 3000, autostart: true, repeat: true },
    },
  };
</script>

<style>
  .alignleft {
    float: left;
  }
  .alignright {
    float: right;
  }
</style>
