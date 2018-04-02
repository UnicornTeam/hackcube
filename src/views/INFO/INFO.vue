<template>
  <div class="board">
    <cube-nav/>

    <h1 class="text-center">Cube Status Manage</h1>
    <h3 class="text-center">显示Cube设备状态</h3>
    <br/>
    <h5 class="text-center">电量</h5>
    <b-progress :value="energyPercent"
                variant="dark"
    ></b-progress>
    <br/>
    <h5 class="text-center">硬盘</h5>
    <b-progress :value="storePercent"
                variant="dark"
    ></b-progress>
    <br/><br/>

    <!-- TODO: 上传预览，上传进度 -->
    <h5>上传arduino固件</h5>
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

    <Input v-model="updateLog" type="textarea" :autosize="{minRows: 4,maxRows: 10}" placeholder="Upload log..." disabled></Input>

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
      onRead(file, content) {
        console.log(file);
        console.log(content);
        console.log(Buffer.from(file.content, 'base64').toString('utf-8'));
        // TODO: Send result to backend
        // TODO: Add upload success prompt
      },
      fetchEnergyStatus() {
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
              this.$Message.success('Update finish.');
              return;
            }
            this.updateLog = result[result.data_key];
          })
          .catch((err) => {
            console.log(err.response);
            this.$Message.error('Call process fail');
          });
      },
      // TODO: Deal with onClick logic.
      onClick() {
        if (this.uploadedFilePath) {
          axios
          .post(`${process.env.BACKEND_HOST}/update_firmware`, { uploadedFilePath: this.uploadedFilePath })
          .then((response) => {
            console.log(response.data);
            const result = response.data;
            this.$Message.success(result.message);
            // todo: start interval to fetch log
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
        // todo: how to get file name of file, then set uploadedFilePath
        // todo: send command with uploadedFilePath
        this.uploadedFilePath = `/root/user_file/arduino/${file.name}`;
        this.$Message.success(`Upload ${file.name} success`);
      },
      onUploadError(error, file, fileList) {
        console.error(error, file, fileList);
        console.log(fileList.name);
        this.$Message.error(`Upload ${fileList.name} fail`);
      },
    },
    created() {
      // TODO: 初始化数据
      console.log(`items is: ${this.items}`);
    },
    timers: {
      fetchUpdateLog: { time: 3000, autostart: false, repeat: true },
      fetchEnergyStatus: { time: 3 * 1000, autostart: true, repeat: false },
    },
  };
</script>

<style scoped>

</style>
