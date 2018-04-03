<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube Status Manage</h1>
    <h3 class="text-center">Display Cube device status</h3>
    <br/>
    <h5 class="text-center">Electricity</h5>
    <b-progress :value="energyPercent"
                variant="dark"
    ></b-progress>
    <br/>
    <h5 class="text-center">Hard driver</h5>
    <b-progress :value="storePercent"
                variant="dark"
    ></b-progress>
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
      <Button type="ghost" @click="onClick">Submit</Button>
    </div>

    <br/>

    <Input v-model="updateLog" type="textarea" :autosize="{minRows: 4,maxRows: 10}" placeholder="Upload log..."></Input>

  </div>
</template>

<script>
  import CubeNav from '@/components/CubeNav';
  import axios from 'axios';

  export default {
    name: 'INFO',
    components: {
      CubeNav,
    },
    data() {
      return {
        uploadHost: process.env.UPLOAD_API,
        updateLog: '',
        energyPercent: 78,
        storePercent: 30,
        extraDataPie: { type: 'INFO-Pie' },
        extraDataArdu: { type: 'INFO-Ardu' },
        uploadedFilePath: '',
      };
    },
    methods: {
      fetchStorageStatus() {
        axios
          .get(`${process.env.BACKEND_HOST}/hd_info`)
          .then((response) => {
            console.log(response.data);
            const result = response.data;
            this.storePercent = result[result.data_key];
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Query energy status fail.');
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
            console.log(response.data);
            const result = response.data;
            if (response.status === 304) {
              this.$timer.stop('fetchUpdateLog');
              this.$Message.info('Update finish.');
              return;
            }
            this.updateLog = result[result.data_key];
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Call process fail');
          });
      },
      onClick() {
        if (this.uploadedFilePath) {
          axios
          .post(`${process.env.BACKEND_HOST}/update_firmware`, { uploadedFilePath: this.uploadedFilePath })
          .then((response) => {
            console.log(response.data);
            const result = response.data;
            this.$Message.success(result.message);
            this.$timer.start('fetchUpdateLog');
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Call process fail');
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
        console.error(error, file, fileList);
        console.log(fileList.name);
        this.$Message.error(`Upload ${fileList.name} fail`);
      },
    },
    timers: {
      fetchUpdateLog: { time: 3000, autostart: false, repeat: true },
      fetchStorageStatus: { time: 0, autostart: true, repeat: false },
    },
  };
</script>

<style scoped>

</style>
